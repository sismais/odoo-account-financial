from odoo import fields, models, api


class AccountJournalBank(models.Model):

    _inherit = 'account.journal'

    emite_boleto = fields.Boolean(string="Boleto Bancário", default=False,)

    #  Campos utilizados para autenticação na API Inter
    bank_inter_cert = fields.Binary(string='Certificado do Banco Inter')
    bank_inter_key = fields.Binary(string='Chave(Key) do Banco Inter')

    #  Campos utilizados para mensagens e instruções no boleto
    local_pagamento = fields.Char('Local de Pgamento', size=70)
    instrucao1 = fields.Char('Instrução 1 ', size=70)
    instrucao2 = fields.Char('Instrução 2 ', size=70)
    instrucao3 = fields.Char('Instrução 3 ', size=70)
    instrucao4 = fields.Char('Instrução 4 ', size=70)

    #  Campos utilizados para taxas (Juros, multas e descontos)
    # multa
    codigo_multa = fields.Selection([
        ('NAOTEMMULTA', 'Não tem multa'),
        ('VALORFIXO', 'Valor Fixo'),
        ('PERCENTUAL', 'Percentual')],
        string='Tipo da Multa')

    dia_carencia_multa = fields.Integer(string='Qtde. dias p/ cobrança da multa')
    taxa_multa = fields.Float(string='Taxa de Multa (%)')
    valor_multa = fields.Float(string='Valor da Multa (R$)')

    # Juros
    codigo_mora = fields.Selection([
        ('VALORDIA', 'Valor ao dia'),
        ('TAXAMENSAL', 'Taxa mensal'),
        ('ISENTO', 'Não há Juros')],
        string='Tipo de Juros')

    dia_carencia_mora = fields.Integer(string='Qtde. dias p/ cobrança da juros')
    taxa_mora = fields.Float(string='Taxa de Juros (%)')
    valor_mora = fields.Float(string='Valor do Juros (R$)')

    # Campos computados (Não é armazenado no bano de dados, uso para fazer verificações no XML
    hide_multa = fields.Integer(string='Hide', compute="_onchange_trata_multa_in_fontend")
    hide_juros = fields.Integer(string='Hide', compute="_onchange_trata_juros_in_fontend")

    # Abaixo metodos onchange, para habilitar, desabilitar e tornar campos obrigatorios.
    @api.onchange('codigo_multa')
    def _onchange_trata_multa_in_fontend(self):
        if self.codigo_multa == 'NAOTEMMULTA':
            self.hide_multa = 1
        elif self.codigo_multa == 'VALORFIXO':
            self.hide_multa = 2
        elif self.codigo_multa == 'PERCENTUAL':
            self.hide_multa = 3

    @api.onchange('codigo_mora')
    def _onchange_trata_juros_in_fontend(self):
        if self.codigo_mora == 'ISENTO':
            self.hide_juros = 1
        elif self.codigo_mora == 'VALORDIA':
            self.hide_juros = 2
        elif self.codigo_mora == 'TAXAMENSAL':
            self.hide_juros = 3



