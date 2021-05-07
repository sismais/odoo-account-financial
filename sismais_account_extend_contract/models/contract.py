import logging
import json

from datetime import datetime
from lxml import etree

_logger = logging.getLogger(__name__)

from odoo import api, fields, models, exceptions, _


class Contract(models.Model):
    _inherit = 'contract.contract',

    valor_total_contrato = fields.Float(string='Valor Total', compute='_list_tree_person')
    partner_city = fields.Char(string='Cidade', compute='_list_tree_person')
    partner_uf = fields.Char(string='UF', compute='_list_tree_person')
    partner_tipo = fields.Char(string='Tipo', compute='_list_tree_person')
    partner_parceiro = fields.Char(string='Parceiro', compute='_list_tree_person')
    data_inicio_contrato = fields.Date(string="Inicio do Contrato", compute='_list_tree_person')

    @api.one
    def _list_tree_person(self):
        #  Abaixo, faço um loop nas linhas do contrato e somo cada uma delas para apresentar o total na visao tree
        #  Na consulta por linha do contrato em contract.line, ordeno por data de inicio para pegar a data mais antiga
        #  E jogar na coluna Inicio do contrato.
        contract_line = self.env['contract.line'].search([('contract_id', '=', self.id)], order='date_start')
        if contract_line:
            self.data_inicio_contrato = contract_line[0].date_start
            for line in contract_line:
                self.valor_total_contrato += line.specific_price

        self.partner_city = self.partner_id.city
        self.partner_uf = self.partner_id.state_id.code
        self.partner_tipo = self.partner_id.tipo
        self.partner_parceiro = self.partner_id.parceiro_id.name

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False,
                        submenu=False):
        """
            A função fields_view_get declarada dentro de models.Model, ela é chamada quando o XML da view é carregado. Com ela,
            podemos fazer alterações em menus form e tree atravez do contexto passado. Podemos remover campos, alterar atributos
            etc..

            Abaixo estou ocultando campos padrão da visão tree do contrato do cliente e fornecedor para então adicionar novos
            campos.
        """
        res = super(Contract, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar,
            submenu=submenu)

        if not self.env.context.get('show_the_column', False) and view_type == 'tree':
            doc = etree.fromstring(res['arch'])
            for field in doc.xpath('//field[@name="name"]'):
                field.set('invisible', '0')
                modifiers = json.loads(field.get('modifiers', '{}'))
                modifiers['tree_invisible'] = False
                modifiers['column_invisible'] = False
                modifiers['position'] = 'after'
                field.set('modifiers', json.dumps(modifiers))
            for field in doc.xpath('//field[@name="code"]'):
                field.set('invisible', '1')
                modifiers = json.loads(field.get('modifiers', '{}'))
                modifiers['tree_invisible'] = True
                modifiers['column_invisible'] = True
                field.set('modifiers', json.dumps(modifiers))
            for field in doc.xpath('//field[@name="journal_id"]'):
                field.set('invisible', '1')
                modifiers = json.loads(field.get('modifiers', '{}'))
                modifiers['tree_invisible'] = True
                modifiers['column_invisible'] = True
                field.set('modifiers', json.dumps(modifiers))
            for field in doc.xpath('//field[@name="journal_id"]'):
                field.set('invisible', '1')
                modifiers = json.loads(field.get('modifiers', '{}'))
                modifiers['tree_invisible'] = True
                modifiers['column_invisible'] = True
                field.set('modifiers', json.dumps(modifiers))
            for field in doc.xpath('//field[@name="partner_id"]'):
                field.set('invisible', '1')
                modifiers = json.loads(field.get('modifiers', '{}'))
                modifiers['tree_invisible'] = True
                modifiers['column_invisible'] = True
                field.set('modifiers', json.dumps(modifiers))
            res['arch'] = etree.tostring(doc)
        return res

    @api.multi
    def recurring_create_invoice(self):
        """
        Função utilizada para gerar fatura recorrente manualmente. Ela foi extendida, para no momento da geração
        ela seta o planos de contas da linah do contrato na linha da fatura.


        """
        result = super(Contract, self).recurring_create_invoice()

        # Adicionamos a opção de informar o plano de contas na linha do contrato. Abaixo,  mudo o plano da fatura criada
        # para o plano da linah do contrato. Existe formas melhores de fazer isso, uma delas é extendendo o metodo
        # da recorrencia para ja puxa o plano na hora da criação da fatura. Mas como estava precisando com urgencia
        # fiz essa "GAMBI" que funciona bem.
        contract_line = self.env['contract.line'].search([('contract_id', '=', self.id)])
        for line in contract_line:
            if line.account_id:
                invoice_line = self.env['account.invoice.line'].search([('invoice_id', '=', result[0].id),
                                                                        ('product_id', '=', line.product_id.id)])
                invoice_line.account_id = line.account_id
        return result

    @api.one
    def _recurring_create_invoice(self, date_ref=False):
        """
        Função utilizada para gerar fatura recorrente. Ela foi extendida, para no momento da geração
        ela seta o planos de contas da linah do contrato na linha da fatura.
        """
        result = super(Contract, self)._recurring_create_invoice(date_ref=False)

        for res in result:

            # Adicionamos a opção de informar o plano de contas na linha do contrato. Abaixo,  mudo o plano da fatura criada
            # para o plano da linah do contrato. Existe formas melhores de fazer isso, uma delas é extendendo o metodo
            # da recorrencia para ja puxa o plano na hora da criação da fatura. Mas como estava precisando com urgencia
            # fiz essa "GAMBI" que funciona bem.
            contract_line = self.env['contract.line'].search([('contract_id', '=', self.id)])
            for line in contract_line:
                if line.account_id:
                    invoice_line = self.env['account.invoice.line'].search([('invoice_id', '=', res.id),
                                                                            ('product_id', '=', line.product_id.id)])
                    invoice_line.account_id = line.account_id
        return result