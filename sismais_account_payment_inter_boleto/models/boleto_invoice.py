import logging

from datetime import datetime, timedelta
from ..lib.biblioteca import caracteres_rm
from .arquivo_certificado import ArquivoCertificado

_logger = logging.getLogger(__name__)

try:
    from erpbrasil.bank.inter.boleto import BoletoInter
    from erpbrasil.bank.inter.api import ApiInter
except ImportError:
    _logger.error("Biblioteca erpbrasil.bank.inter não instalada")

try:
    from febraban.cnab240.user import User, UserAddress, UserBank
except ImportError:
    _logger.error("Biblioteca febraban não instalada")

try:
    from erpbrasil.base import misc
except ImportError:
    _logger.error("Biblioteca erpbrasil.base não instalada")

from odoo import api, fields, models, exceptions, _


class GenerateBoletoInvoice(models.Model):

    _inherit = 'account.invoice'

    nossonumero = fields.Char('Nosso Numero', size=30)  # Armazena o nosso numero do boleto
    boleto_codigo_baixa = fields.Selection([
        ('ACERTOS', 'ACERTOS'),
        ('PROTESTADO', 'PROTESTADO'),
        ('DEVOLUCAO', 'DEVOLUCAO'),
        ('PROTESTOAPOSBAIXA', 'PROTESTOAPOSBAIXA'),
        ('PAGODIRETOAOCLIENTE', 'PAGODIRETOAOCLIENTE'),
        ('SUBISTITUICAO', 'SUBISTITUICAO'),
        ('FALTADESOLUCAO', 'FALTADESOLUCAO'),
        ('APEDIDODOCLIENTE', 'APEDIDODOCLIENTE')],
        string='Codigo da Baixa')  # Em caso de baixas no boleto, armazena o codigo da baixa.

    def dados_boleto(self):
        journal = self.env['account.journal'].search([('code', '=', 'Inter')])
        dados = []
        myself = User(
            name=self.company_id.legal_name,
            identifier=misc.punctuation_rm(self.company_id.cnpj_cpf),
            bank=UserBank(
                bankId=journal.bank_account_id.bank_id.bic,
                branchCode=journal.bank_account_id.bra_number,
                accountNumber=journal.bank_account_id.acc_number,
                accountVerifier=journal.bank_account_id.acc_number_dig,
                bankName=journal.bank_account_id.bank_id.name
            ),
        )
        payer = User(
            name=self.partner_id.name,
            identifier=misc.punctuation_rm(self.partner_id.cnpj_cpf),
            email=self.partner_id.email,
            personType='FISICA' if self.partner_id.company_type == 'person' else 'JURIDICA',
            phone=caracteres_rm(self.partner_id.phone),
            address=UserAddress(
                streetLine1=self.partner_id.street,
                district=self.partner_id.district,
                city=self.partner_id.city_id.name,
                stateCode=self.partner_id.state_id.code,
                zipCode=misc.punctuation_rm(self.partner_id.zip),
                streetNumber=self.partner_id.number,
            )
        )

        slip = BoletoInter(
            sender=myself,
            amount=self.amount_total,
            payer=payer,
            issue_date=datetime.now(),
            identifier=misc.punctuation_rm(self.partner_id.cnpj_cpf),
            instructions=[
                journal.instrucao1,
                journal.instrucao2,
                journal.instrucao3,
                journal.instrucao4,
            ],
            multa=dict(
                codigoMulta=journal.codigo_multa,
                data=str(self.date_due + timedelta(days=journal.dia_carencia_multa)),
                valor=0 if journal.codigo_multa == 'PERCENTUAL' else journal.valor_multa,
                taxa=0 if journal.codigo_multa == 'VALORFIXO' else journal.taxa_multa
            ),
            mora=dict(
                codigoMora=journal.codigo_mora,
                data=str(self.date_due + timedelta(days=journal.dia_carencia_mora)),
                valor=0 if journal.codigo_mora == 'TAXAMENSAL' else journal.valor_mora,
                taxa=0 if journal.codigo_mora == 'VALORFIXO' else journal.taxa_mora
            ),
            due_date=self.date_due,
        )
        dados.append(slip)
        return dados

    def action_gerar_boleto(self):
        journal = self.env['account.journal'].search([('code', '=', 'Inter')])
        with ArquivoCertificado(journal, 'w') as (key, cert):
            self.api = ApiInter(
                cert=(cert, key),
                conta_corrente=journal.bank_account_id.acc_number + journal.bank_account_id.acc_number_dig
            )

            if self.pdf_boletos_id:
                raise exceptions.UserError(
                    'Já existe um boleto dessa fatura. Você pode utilizar a opção Download ou enviar por email. '
                    'Caso deseje de fato gerar um novo boleto, você pode usar a opção Atualizar Boleto, ele fará a baixa'
                    ' no banco Inter (Cancelamento) e emitirá um novo boleto!')

            if self.state == 'draft':
                raise exceptions.UserError(
                    'O status da fatura ainda é provisório. Valide a fatura para que então você '
                    'consiga gerar o boleto. Impossível gerar boletos para fatura com status Provisório!')

            data = self.dados_boleto()
            for item in data:
                # Se a fatura ainda não tiver boleto (Nosso numero), então gera.
                if not self.pdf_boletos_id:

                    if self.date_due < datetime.now().date():
                        raise exceptions.UserError(
                            'A data de vencimento da fatura é menor que a data de emissão do boleto'
                            ' (Data atual). Impossível gerar um boleto com a data de vencimento menor'
                            ' que a data de emissão!')

                    # Inclusão do boleto e envio para a API do Inter
                    # os dados do emitente e do pagador estão no dicionarios no inicio do codigo
                    resposta = self.api.boleto_inclui(item._emissao_data())

                    # Salva o nosso numero do boleto na respectiva fatura
                    self.nossonumero = resposta['nossoNumero']

                    # Seta a flag para true, indicando que foi emitido boleto dessa fatura
                    self.boleto_emitido = True

                    # Consultar a API do Inter para localizar e baixar o PDF do boleto gerado
                    # A pesquisa é feita pelo nossonumero e o boleto é codificado em base64
                    boleto_base64 = self.api.boleto_pdf(self.nossonumero)

                    self.pdf_boletos_id = self.env['ir.attachment'].create(
                        {
                            'name': (
                                    "Boleto %s" % self.display_name.replace('/', '-')),
                            'datas': boleto_base64,
                            'datas_fname': ("boleto_%s.pdf" %
                                            self.display_name.replace('/', '-')),
                            'type': 'binary'
                        }
                    )

    def action_consulta_boleto(self):
        """A implementar para ser usado na futura view do painel do boleto"""
        pass

    def action_baixa_boleto(self):
        """
        Essa função realiza operações de Baixa de boleto na API do banco inter. Ela disponibiliza uma janela com todas
        as opções de baixa. Ai escolher o codigo da baixa e clicar em salvar, a API do inter é chamada e enviado a
        requisição.
        """

        journal = self.env['account.journal'].search([('code', '=', 'Inter')])
        with ArquivoCertificado(journal, 'w') as (key, cert):
            self.api = ApiInter(
                cert=(cert, key),
                conta_corrente=journal.bank_account_id.acc_number + journal.bank_account_id.acc_number_dig
            )

            if not self.pdf_boletos_id:
                raise exceptions.UserError(
                    'Ainda não existe um boleto gerado dessa fatura. Impossível imprimir/baixar pdf '
                    'de um boleto inexistente!')

            if abs((self.date_invoice - datetime.now().date()).days) <= 2:
                raise exceptions.UserError(
                    'O boleto em questão tem menos de dois dias que foi emitido. É provavel que '
                    'ainda não esteja registrado. Aguarde pelo menos dois dias para realizar a baixa')

            # resposta = self.api.boleto_baixa(self.nossonumero, self.boleto_codigo_baixa)

            view_id = self.env.ref('sismais_account_payment_inter_boleto.baixa_boleto_invoice_form').id
            context = self._context.copy()
            return {
                'name': 'Baixa Boleto Inter',
                'view_type': 'form',
                'view_mode': 'tree',
                'views': [(view_id, 'form')],
                'res_model': 'account.invoice',
                'view_id': view_id,
                'type': 'ir.actions.act_window',
                'res_id': self.id,
                'target': 'new',
                'context': context,
            }

    def action_pdf_boleto(self):

        if not self.pdf_boletos_id:
            raise exceptions.UserError(
                'Ainda não existe um boleto gerado dessa fatura. Impossível imprimir/baixar pdf '
                'de um boleto inexistente!')

        boleto_id = self.pdf_boletos_id
        base_url = self.env['ir.config_parameter'].get_param(
            'web.base.url')
        download_url = '/web/content/%s/%s?download=True' % (
            str(boleto_id.id), boleto_id.name)

        return {
            "type": "ir.actions.act_url",
            "url": str(base_url) + str(download_url),
            "target": "new",
        }

    def baixa_recorrente_boleto(self):
        """
        O Odoo possui um proprio sistema de Cron, usarei ele para acionar essa função diariamente.
        O cron pode ser feito na propria interface do Odoo ou definida por XML, nesse caso, usuario um XML,
        Assim que o modulo for instalado, o cron será criado.
        """

        journal = self.env['account.journal'].search([('code', '=', 'Inter')])
        with ArquivoCertificado(journal, 'w') as (key, cert):
            self.api = ApiInter(
                cert=(cert, key),
                conta_corrente=journal.bank_account_id.acc_number + journal.bank_account_id.acc_number_dig
            )

            #  Data inicial usada na consulta de boleto no no formato string com hifen no lugar de ponto (AAAA-MM-DD)
            #  Uma data bem antiga para que qualquer boleto não pago, independente do tempo, venha no filtro.
            dt_inicial = '1990-01-01'

            #  Data final usada na consulta de boleto no no formato string com hifen no lugar de ponto (AAAA-MM-DD)
            dt_final = str(datetime.now().date()).replace('.', '-')

            resposta = self.api.boleto_consulta('PAGOS', dt_inicial, dt_final)
            for i in range(len(resposta['content'])):
                invoice = self.env['account.invoice'].search([('nossonumero', '=', resposta['content'][i]['nossoNumero'])])
                # invoice = self.env['account.invoice'].search([('nossonumero', '=', '00663999953')]) # usada para teste
                if invoice and invoice.state == 'open':
                    Payment = self.env['account.payment'].with_context(default_invoice_ids=[(4, invoice.id, False)])
                    payment = Payment.create({
                        'payment_date': datetime.now(),
                        'payment_method_id': 1,
                        'payment_type': 'inbound',
                        'partner_type': 'customer',
                        'partner_id': invoice.partner_id.id,
                        'amount': invoice.amount_total,
                        'journal_id': journal.id,
                        'company_id': invoice.company_id,
                        'currency_id': 6,
                        'payment_difference_handling': 'reconcile'
                    })
                    payment.post()

    def action_atualiza_boleto(self):
        """
        Essa função faz a atualização de boleto. Basicamente ela cancela o boleto atual e gera um novo boleto atualizado.
        Provavelmente existe formas melhores de realizar essa operação, porém na API do Banco Inter existe apenas 4 endpoint
        (Emissão, consulta, baixa e PDF), então o que encontrei no momento foi cancelar com a baixa e emitir um novo boleto.

        Essa operação pode ser cobrada por boletos gerados.
        """
        journal = self.env['account.journal'].search([('code', '=', 'Inter')])
        with ArquivoCertificado(journal, 'w') as (key, cert):
            self.api = ApiInter(
                cert=(cert, key),
                conta_corrente=journal.bank_account_id.acc_number + journal.bank_account_id.acc_number_dig
            )

            if not self.pdf_boletos_id:
                raise exceptions.UserError(
                    'Ainda não existe um boleto gerado dessa fatura. Impossível atualizar um '
                    'boleto inexistente!')

            if self.date < datetime.now().date() + timedelta(days=2):
                raise exceptions.UserError(
                    'O boleto em questão tem menos de dois dias que foi emitido. É provavel que '
                    'ainda não esteja registrado. Aguarde pelo menos dois dias para atualizá-lo')

            # Realiza a baixa do boleto atual
            resposta_baixa = self.api.boleto_baixa(self.nossonumero, 'SUBISTITUICAO')

            # Depois que realizo a baixo lá no Inter, eu apago a justificativa do banco de dados, porque la vai ta o nosso numero
            # do novo boleto, e ele nao foi baixado. Sei que não é a melhor forma, mas futuramente podemos criar uma tabela
            # somente para armazenar os boletos, inclusive para consultas, podemos fazer isso quando for fazer o painel de boleto.
            self.boleto_codigo_baixa = None

            # Na função de de geração de boleto, só é gerado, se não tiver pdf_boletos_id. Esse tratamento existe para
            # a pessoa não gerar duas vezes. POrém, só nosso caso de atualização, precisaremos, então seto como Null
            # e abaixo quando a função for chamada, será gerado normalmente. Eu poderia excluir o registro do boleot,
            # mas futuramente, pode ser que queremos exibi-los em consultas no peinel do boleto.
            self.pdf_boletos_id = None

            # Realiza a emissão do novo boleto
            self.action_gerar_boleto()
