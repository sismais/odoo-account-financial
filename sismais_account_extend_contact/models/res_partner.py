import logging

from odoo import api, fields, models, exceptions, _


class ResPartner(models.Model):

    _inherit = 'res.partner'

    segmento = fields.Selection([
        ('Alimentos e Bebidas','Alimentos e Bebidas'),
        ('Arte e Antiguidades', 'Arte e Antiguidades'),
        ('Artigos Religiosos', 'Artigos Religiosos'),
        ('Assinaturas e Revistas', 'Assinaturas e Revistas'),
        ('Automóveis e Veículos', 'Automóveis e Veículos'),
        ('Bebês e Cia', 'Bebês e Cia'),
        ('Blu-Ray', 'Blu-Ray'),
        ('Brindes / Materiais Promocionais', 'Brindes / Materiais Promocionais'),
        ('Brinquedos e Games', 'Brinquedos e Games'),
        ('Casa e Decoração', 'Casa e Decoração'),
        ('CDs', 'CDs'),
        ('Colecionáveis', 'Colecionáveis'),
        ('Compras Coletivas', 'Compras Coletivas'),
        ('Construção e Ferramentas', 'Construção e Ferramentas'),
        ('Cosméticos e Perfumaria', 'Cosméticos e Perfumaria'),
        ('Cursos e Educação', 'Cursos e Educação'),
        ('Discos de Vinil', 'Discos de Vinil'),
        ('DVDs', 'DVDs'),
        ('Eletrodomésticos', 'Eletrodomésticos'),
        ('Eletrônicos', 'Eletrônicos'),
        ('Emissoras de Rádio', 'Emissoras de Rádio'),
        ('Emissoras de Televisão', 'Emissoras de Televisão'),
        ('Empregos', 'Empregos'),
        ('Empresas de Telemarketing', 'Empresas de Telemarketing'),
        ('Esporte e Lazer', 'Esporte e Lazer'),
        ('Fitas K7 Gravadas', 'Fitas K7 Gravadas'),
        ('Flores, Cestas e Presentes', 'Flores, Cestas e Presentes'),
        ('Fotografia', 'Fotografia'),
        ('HD-DVD', 'HD-DVD'),
        ('Igrejas / Templos / Instituições Religiosas', 'Igrejas / Templos / Instituições Religiosas'),
        ('Indústria, Comércio e Negócios', 'Indústria, Comércio e Negócios'),
        ('Infláveis Promocionais', 'Infláveis Promocionais'),
        ('Informática', 'Informática'),
        ('Ingressos', 'Ingressos'),
        ('Instrumentos Musicais', 'Instrumentos Musicais'),
        ('Joalheria', 'Joalheria'),
        ('Lazer', 'Lazer'),
        ('LD', 'LD'),
        ('Livros', 'Livros'),
        ('MD', 'MD'),
        ('Moda e Acessórios', 'Moda e Acessórios'),
        ('Motéis', 'Motéis'),
        ('Música Digital', 'Música Digital'),
        ('Natal', 'Natal'),
        ('Negócios e Oportunidades', 'Negócios e Oportunidades'),
        ('Outros Serviços', 'Outros Serviços'),
        ('Outros Serviços de Avaliação', 'Outros Serviços de Avaliação'),
        ('Papelaria e Escritório', 'Papelaria e Escritório'),
        ('Páscoa', 'Páscoa'),
        ('Pet Shop', 'Pet Shop'),
        ('Saúde', 'Saúde'),
        ('Serviço Advocaticios', 'Serviço Advocaticios'),
        ('Serviço de Distribuição de Jornais / Revistas', 'Serviço de Distribuição de Jornais / Revistas'),
        ('Serviços Administrativos', 'Serviços Administrativos'),
        ('Serviços Artísticos', 'Serviços Artísticos'),
        ('Serviços de Abatedouros / Matadouros', 'Serviços de Abatedouros / Matadouros'),
        ('Serviços de Aeroportos', 'Serviços de Aeroportos'),
        ('Serviços de Agências', 'Serviços de Agências'),
        ('Serviços de Aluguel / Locação', 'Serviços de Aluguel / Locação'),
        ('Serviços de Armazenagem', 'Serviços de Armazenagem'),
        ('Serviços de Assessorias', 'Serviços de Assessorias'),
        ('Serviços de Assistência Técnica / Instalações ', 'Serviços de Assistência Técnica / Instalações '),
        ('Serviços de Associações', 'Serviços de Associações'),
        ('Serviços de Bancos de Sangue', 'Serviços de Bancos de Sangue'),
        ('Serviços de Bibliotecas', 'Serviços de Bibliotecas'),
        ('Serviços de Cartórios', 'Serviços de Cartórios'),
        ('Serviços de Casas Lotéricas', 'Serviços de Casas Lotéricas'),
        ('Serviços de Confecções', 'Serviços de Confecções'),
        ('Serviços de Consórcios', 'Serviços de Consórcios'),
        ('Serviços de Consultorias', 'Serviços de Consultorias'),
        ('Serviços de Cooperativas', 'Serviços de Cooperativas'),
        ('Serviços de Despachante', 'Serviços de Despachante'),
        ('Serviços de Engenharia', 'Serviços de Engenharia'),
        ('Serviços de Estacionamentos', 'Serviços de Estacionamentos'),
        ('Serviços de Estaleiros', 'Serviços de Estaleiros'),
        ('Serviços de Exportação / Importação', 'Serviços de Exportação / Importação'),
        ('Serviços de Geólogos', 'Serviços de Geólogos'),
        ('Serviços de joalheiros', 'Serviços de joalheiros'),
        ('Serviços de Leiloeiros', 'Serviços de Leiloeiros'),
        ('Serviços de limpeza', 'Serviços de limpeza'),
        ('Serviços de Loja de Conveniência', 'Serviços de Loja de Conveniência'),
        ('Serviços de Mão de Obra', 'Serviços de Mão de Obra'),
        ('Serviços de Órgão Públicos', 'Serviços de Órgão Públicos'),
        ('Serviços de Pesquisas', 'Serviços de Pesquisas'),
        ('Serviços de Portos', 'Serviços de Portos'),
        ('Serviços de Saúde / Bem Estar', 'Serviços de Saúde / Bem Estar'),
        ('Serviços de Seguradoras', 'Serviços de Seguradoras'),
        ('Serviços de Segurança', 'Serviços de Segurança'),
        ('Serviços de Sinalização', 'Serviços de Sinalização'),
        ('Serviços de Sindicatos / Federações', 'Serviços de Sindicatos / Federações'),
        ('Serviços de Traduções', 'Serviços de Traduções'),
        ('Serviços de Transporte', 'Serviços de Transporte'),
        ('Serviços de Utilidade Pública', 'Serviços de Utilidade Pública'),
        ('Serviços em Agricultura / Pecuária / Piscicultura', 'Serviços em Agricultura / Pecuária / Piscicultura'),
        ('Serviços em Alimentação', 'Serviços em Alimentação'),
        ('Serviços em Arte', 'Serviços em Arte'),
        ('Serviços em Cine / Foto / Som', 'Serviços em Cine / Foto / Som'),
        ('Serviços em Comunicação', 'Serviços em Comunicação'),
        ('Serviços em Construção', 'Serviços em Construção'),
        ('Serviços em Ecologia / Meio Ambiente', 'Serviços em Ecologia / Meio Ambiente'),
        ('Serviços em Eletroeletrônica / Metal Mecânica', 'Serviços em Eletroeletrônica / Metal Mecânica'),
        ('Serviços em Festas / Eventos', 'Serviços em Festas / Eventos'),
        ('Serviços em Informática', 'Serviços em Informática'),
        ('Serviços em Internet', 'Serviços em Internet'),
        ('Serviços em Jóias / Relógios / Óticas', 'Serviços em Jóias / Relógios / Óticas'),
        ('Serviços em Telefonia', 'Serviços em Telefonia'),
        ('Serviços em Veículos', 'Serviços em Veículos'),
        ('Serviços Esotéricos / Místicos', 'Serviços Esotéricos / Místicos'),
        ('Serviços Financeiros', 'Serviços Financeiros'),
        ('Serviços Funerários', 'Serviços Funerários'),
        ('Serviços Gerais', 'Serviços Gerais'),
        ('Serviços Gráficos / Editoriais', 'Serviços Gráficos / Editoriais'),
        ('Serviços para Animais', 'Serviços para Animais'),
        ('Serviços para Deficientes', 'Serviços para Deficientes'),
        ('Serviços para Escritórios', 'Serviços para Escritórios'),
        ('Serviços para Roupas', 'Serviços para Roupas'),
        ('Serviços Socias / Assistenciais', 'Serviços Socias / Assistenciais'),
        ('Sex Shop', 'Sex Shop'),
        ('Shopping Centers', 'Shopping Centers'),
        ('Tabacaria', 'Tabacaria'),
        ('Tarifas Bancárias', 'Tarifas Bancárias'),
        ('Tarifas Telefônicas', 'Tarifas Telefônicas'),
        ('Telefonia', 'Telefonia'),
        ('Turismo', 'Turismo')],
        string='Segmento')

    tipo = fields.Selection([
        ('cliente de parceiro', 'Cliente de Parceiro'),
        ('cliente direto local', 'Cliente Direto Local'),
        ('cliente direto internet', 'Cliente Direto Internet')],
        string='Tipo de Cliente')

    parceiro_id = fields.Many2one(
        comodel_name='res.partner',
        string='Parceiro',
        ondelete='cascade'
    )


    @api.onchange('tipo')
    def onchange_parceiro_in_partner(self):
        """
        Função necessária para garantir que o formulario não seja submetido com um parceiro, caso o cliente não tenha parceiro.
        Ex: Vamos supor que o usuário colocou o tipo como cliente de parceiro por engano e informou um parceiro qualquer
        então ele percebe que ta errado e muda o tipo para cliente direto. O input parceiro vai sumir da tela, mas
        ainda vai ta setado o parceiro por baixo dos panos, então quando ela salvar, é como se aquele cliente tivesse
        um parceiro atribuído e assim pode da erros em futuras analises.

        A função garante que toda vez que o campo tipo for alterado, ela limpa o campo parceiro
        """

        self.parceiro_id = None

