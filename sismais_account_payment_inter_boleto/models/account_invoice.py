import logging

_logger = logging.getLogger(__name__)

try:
    from erpbrasil.bank.inter.boleto import BoletoInter
    from erpbrasil.bank.inter.api import ApiInter
except ImportError:
    _logger.error("Biblioteca erpbrasil.bank.inter não instalada")

from odoo import api, fields, models, exceptions, _


class AccountInvoice(models.Model):

    _inherit = 'account.invoice'

    pdf_boletos_id = fields.Many2one(
        comodel_name='ir.attachment',
        string='PDF Boletos',
        ondelete='cascade'
    )

    boleto_emitido = fields.Boolean()

    @api.multi
    def action_send_boleto(self):
        """
        Abre uma janela para escrever um email com o boleto bancario emitido com uma mensagem padrão (Podendo personalizar)
        """

        if not self.pdf_boletos_id:
            raise exceptions.UserError('Ainda não existe um boleto gerado dessa fatura. Impossível enviar pdf '
                                           'de um boleto inexistente!')

        self.ensure_one()
        template = self.env.ref('sismais_account_payment_inter_boleto.email_template_boleto_invoice', True)
        compose_form = self.env.ref('mail.email_compose_message_wizard_form', False)
        ctx = dict(
            default_model='account.invoice',
            default_res_id=self.id,
            default_use_template=bool(template),
            default_template_id=template and template.id or False,
            default_composition_mode='comment',
            mark_invoice_as_sent=True,
            custom_layout="account.mail_template_data_notification_email_account_invoice",
            force_email=True
        )
        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }


