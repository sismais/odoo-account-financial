{
    'name': 'Banco Inter - Integração com a API',
    'summary': """
        Integração com a API do Banco Inter""",
    'version': '12.0.1.0.0',
    'author': 'Sismais Tecnologia LTDA, Ricardo Cássio',
    'website': 'www.maxproerp.com.br',
    'depends': [
        'account',
        'mail',
        'contract',
    ],
    'data': [
        'views/account_journal_bank.xml',
        'views/account_invoice.xml',
        'views/contract_contract.xml',
        'views/mail_template.xml',
        'views/cron_verificar_pagamento.xml',

    ],
    'demo': [],
    "external_dependencies": {"python": [
        "erpbrasil.bank.inter",
    ]},
}