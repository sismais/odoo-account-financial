import logging
from datetime import datetime

_logger = logging.getLogger(__name__)

from odoo import api, fields, models, _


class RecurringInvoice(models.Model):
    """
    Model faz a extenção do model de recorrencia da OCA (contract.contract) para adicionar funções para gerar boleto
    automaticamente junto com a fatura recorrente.
    """

    _inherit = 'contract.contract'

    boleto_inter = fields.Boolean(string="Boleto automatico", default=True,)

    @api.multi
    def recurring_create_invoice(self):
        """
        Função utilizada para gerar fatura recorrente manualmente. Ela foi extendida, para no momento da geração
        Se tiver marcado a opção gerar boleto, o boleto será gerado


        """
        result = super(RecurringInvoice, self).recurring_create_invoice()
        if self.boleto_inter:  # Se no formulário da fatura recorrente estiver marcado para emitir boleto, entra no if.
            result.action_gerar_boleto()

    @api.multi
    def cron_recurring_create_invoice(self):
        """
        Função utilizada para gerar fatura recorrente. Ela foi extendida para que, no momento da fatura recorrente,
        Se tiver marcado gerar boleto automatico no contrato, então o boleto será gerado.
        """
        result = super(RecurringInvoice, self).cron_recurring_create_invoice(date_ref=None)
        if True:  # Se no formulário da fatura recorrente estiver marcado para emitir boleto, entra no if.
            result.action_gerar_boleto()
            print(result.id)



