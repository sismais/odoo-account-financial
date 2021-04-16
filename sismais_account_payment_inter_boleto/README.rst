Banco Inter - Integração com API
================================

.. raw:: html

   <p align="center">

Introdução \| Funcionalidades \| Roadmap \| Instalação \| Suporte \|
Créditos

.. raw:: html

   </p>

Para dúvidas acesse: `Suporte Sismais
Tecnologia <https://www.maxproerp.com.br/suporte>`__

Introdução
----------

Este módulo adiciona ao SismaisERP funcionalidades de emissão, baixa e
reconhecimentos de boletos pagos do banco Inter.


Funcionalidades
---------------

-  Emissão de boletos bancários manual dentro da fatura
-  Emissão de boletos bancários manual ao criar uma fatura recorrente
   manualmente (contract.contract)
-  Emissão de boletos bancários automatico ao gerar uma fatura
   recorrente (contract.contract)
-  Baixa e boleto manual dentro da fatura
-  Download do PDF do boleto emitido (Função disponível dentro da
   fatura)
-  Atualização de boleto bancário dentro da fatura
-  Envio do PDF do boleto por email (Função disponível dentro da fatura)

As funções que estão disponíveis dentro da fatura (Faturamento ->
Clientes - Fatura) ficam no menu ação, na parte superior.


Instalação e Configuração
-------------------------

Dependencias
~~~~~~~~~~~~

Para a correta funcionalidade desse módulo, ele depende de outros
modulos. São eles:

- account `(GitHub) <https://github.com/odoo/odoo/tree/adc97120c94e3a0e8325a40fb0664faa16036f74/addons/account>`__
- mail `(GitHub) <https://github.com/odoo/odoo/tree/adc97120c94e3a0e8325a40fb0664faa16036f74/addons/mail>`__
- contract `(GitHub) <https://github.com/OCA/contract/tree/12.0/contract>`__

Além de depender de outros módulos, também depende das seguintes
bibliotecas Python:

- erpbrasil.bank.inter `(GitHub) <https://github.com/erpbrasil/erpbrasil.bank.inter>`__
    ``pip install erpbrasil.bank.inter``

- febraban `(GitHub) <https://github.com/starkbank/febraban-python>`__
    ``pip install febraban``

Instalação
~~~~~~~~~~

1 - Acesse sua pasta de modulos: ``cd /opt/sismaiserp/addons`` -
Diretório exemplo

2 - Realize um clone desse diretorio ou baixe e extraia dentro da pasta
de módulos

3 - No SismaisERP, acesso (Configurações - > Ativar modo desenvolvedor),
vá em aplicativos e em seguida clique em Atualizar Aplicativos

4 - Nesse momento, se tudo ocorreu bem, o modulo já estará disponível.
Pesquisa por banco Inter e em seguida, clique em instalar

Nesse momento, o modulo já está instalado em sua Base.

Configuração
~~~~~~~~~~~~

Após realizar a instalação do módulo, será acrescentado uma aba em
(Faturamento -> Configurações -> Contas Bancárias)

1 - Crie uma nova conta bancária e informe os dados de sua conta Inter
corretamente. Vá na aba Boleto Bancário e realize as seguintes
configurações:

- Na aba configurações, faça upload do seu certificado Inter e também da chave (Key) que é disponibilizado para contas PJ no internet banking do Inter.
- Na aba Taxas/Prazo, informe sua taxas de juros, multa e desconto.
- Na aba Informações/Mensagens, informe as instruções que serão impressas no corpo do boleto para o caixa e o pagador.

2 - Crie um novo diário em (Faturamento -> Configurações -> Diário) com os seguintes dados:

- Nome do Diário: Banco Inter
- Tipo: Banco
- Aba Lançamentos de Diário:
    - Código Abreviado: Inter
    - Próximo Número: 1
    - Conta de Débito padrão: 1.1.3 Banco Inter
    - Conta Crédito padrão: 1.1.3 Banco Inter
- Aba Conta Bancária:
    - Informe os dados de sua conta Inter

Nesse momento, se a instalação e os dados foram informados corretamente,
já estamos pronto a operar com boleto Inter.

Suporte
-------

Esse modulo de integração com a API do banco Inter é desenvolvido e
mantido pela Sismais Tecnologia.

Caso tenha dúvida, problema ou sugestões na instalação, configuração
e/ou utilização do módulo, entre em contato com suporte da Sismais
Tecnologia

Telefone: 77 3086-8870

E-Mail: suporte@maxproerp.com.br

Suporte: https://www.maxproerp.com.br/suporte


Créditos
--------

**"Um jogador que torna o seu time excelente é mais valioso que um
excelente jogador."**

Este repositório é construído com base no excelente trabalho feito por
essas pessoas.

Contribuidores
~~~~~~~~~~~~~~

`Sismais Tecnologia LTDA <https://github.com/sismais/>`__

`Ricardo Cássio <https://github.com/ricardocassio>`__

`Maicon Saraiva <https://github.com/maiconsaraiva>`__




