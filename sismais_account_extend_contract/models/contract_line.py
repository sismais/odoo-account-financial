import logging
import json

from lxml import etree

_logger = logging.getLogger(__name__)

from odoo import api, fields, models, exceptions, _


class ContractLine(models.Model):

    _inherit = 'contract.line'

    account_id = fields.Many2one(
        comodel_name='account.account',
        string='Conta',
        ondelete='cascade'
    )


    @api.model
    def fields_view_get(self, view_id=None, view_type=None, toolbar=False, submenu=False):
        """
        A função fields_view_get declarada dentro de models.Model, ela é chamada quando o XML da view é carregado. Com ela,
        podemos fazer alterações em menus form e tree atravez do contexto passado. Podemos remover campos, alterar atributos
        etc..
        """

        res = super(ContractLine, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)

        if not self.env.context.get('show_the_column', False) and view_type == 'tree':
            doc = etree.formstring(res['arch'])
            for field in doc.xpath('//field[@name="price_unit"]'):
                field.set('invisible', '1')
                modifiers = json.loads(field.get('modifiers', '{}'))
                modifiers['tree_invisible'] = False
                modifiers['column_invisible'] = False
                modifiers['position'] = 'after'
                modifiers['sum'] = 'Valor Total Dos Serviços'
                field.set('modifiers', json.dumps(modifiers))
            res['arch'] = etree.tostring(doc)
        return res