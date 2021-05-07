import logging

from odoo import api, fields, models, exceptions, _


class ResPartner(models.Model):

    _inherit = 'res.partner'

    segmento = fields.Selection([
        ('Supermercado', 'Supermercado'),
        ('Papelaria e Presentes', 'Papelaria e Presentes'),
        ('Materiais de Construção', 'Materiais de Construção'),
        ('Moda e Calçados', 'Moda e Calçados'),
        ('Móveis e Eletro', 'Móveis e Eletro'),
        ('Atacado', 'Atacado'),
        ('Indústria', 'Indústria'),
        ('Loja de Variedades', 'Loja de Variedades'),
        ('Agropecuária e Veterinária / Pet Shop', 'Agropecuária e Veterinária / Pet Shop'),
        ('Oficina e Motopeças (Motos)', 'Oficina e Motopeças (Motos)'),
        ('Oficina e Autopeças (carros)', 'Oficina e Autopeças (carros)'),
        ('Informática (Lojas e/ou Serviços)', 'Informática (Lojas e/ou Serviços)'),
        ('Tecnologia', 'Tecnologia'),
        ('Contabilidade', 'Contabilidade'),
        ('Consultoria', 'Consultoria'),
        ('Outros', 'Outros'),
        ('Oficina e Peças de Bicicletas', 'Oficina e Peças de Bicicletas'),
        ('Farmácia', 'Farmácia'),
        ('Salão de Beleza', 'Salão de Beleza'),
        ('Resturante / Bares / Lanchonetes / Pizzaria', 'Resturante / Bares / Lanchonetes / Pizzaria'),
        ('Padarias', 'Padarias'),
        ('Sacolão e HortiFruti', 'Sacolão e HortiFruti'),
        ('Serviços', 'Serviços'),
        ('Produtor Rural', 'Produtor Rural')],
        string='Segmento')

    tipo = fields.Selection([
        ('cliente_de_parceiro', 'Cliente de Parceiro'),
        ('cliente_direto_local', 'Cliente Direto Local'),
        ('cliente_direto_internet', 'Cliente Direto Internet'),
        ('parceiro', 'Parceiro')],
        string='Tipo de Cliente')

    parceiro_id = fields.Many2one(
        comodel_name='res.partner',
        string='Parceiro',
        ondelete='cascade'
    )


    @api.onchange('tipo')
    def onchange_parceiro_in_partner(self):
        """
        Força o responsável pelo clientes para Sismais Tecnologia caso seja um cliente direto e limpa o campo de parceir
        caso a pessoa escolha ou tipo, evitando assim possível erros.
        """

        if self.tipo == 'cliente_direto_local' or self.tipo == 'cliente_direto_internet':
            self.parceiro_id = self.company_id.id
        else:
            self.parceiro_id = None

