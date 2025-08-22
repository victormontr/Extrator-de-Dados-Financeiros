Extrator de Dados Financeiros
📖 Sobre o Projeto

Este projeto é uma aplicação de desktop com interface gráfica (GUI) desenvolvida em Python para extrair dados financeiros históricos de empresas listadas na B3 (Bolsa de Valores do Brasil).

A aplicação utiliza a biblioteca yfinance para buscar os dados e permite ao usuário salvar as informações em arquivos CSV ou XLSX, de forma organizada e simples.
✨ Funcionalidades

    Interface Gráfica Intuitiva: Uma GUI limpa e fácil de usar, construída com Tkinter.

    Busca por Ticker: Seleção da empresa a partir de uma lista completa de tickers da B3, com funcionalidade de autocompletar.

    Seleção de Período: Escolha das datas de início e fim da extração através de um seletor de calendário.

    Frequência de Dados: Opção de extrair dados com diferentes intervalos (diário, semanal, mensal, etc.).

    Exportação Flexível: Salva os dados históricos em formatos de planilha padrão: CSV (otimizado para o Brasil) e XLSX (Excel).

    Processamento Assíncrono: A busca de dados é executada em segundo plano (threading), evitando que a interface congele durante o download.

    Compatibilidade: Funciona nos principais sistemas operacionais (Windows, macOS e Linux).

🚀 Como Começar

Siga estas instruções para obter uma cópia local do projeto e executá-la.
Pré-requisitos

    Python 3.x instalado.

Instalação

    Clone o repositório:

    git clone https://seu-repositorio-aqui.git

    Navegue até o diretório do projeto e instale as dependências. É altamente recomendado usar um ambiente virtual (venv).

    # Crie e ative o ambiente virtual (opcional, mas recomendado)
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate

    # Instale as bibliotecas necessárias
    pip install pandas yfinance tkcalendar

Execução

    Certifique-se de que o arquivo Mapa Tickers B3.csv esteja no mesmo diretório do script principal, ou dentro de uma subpasta chamada Mapa.

    Execute o script principal:

    python nome_do_seu_arquivo.py

    A janela da aplicação será aberta. Preencha os campos e clique em "🔍 Buscar".

    Os arquivos serão salvos na pasta Meus Documentos/Dados financeiros Extraídos.

🔧 Solução de Problemas

    A busca não retorna dados: Verifique sua conexão com a internet. Tente atualizar a biblioteca yfinance com pip install --upgrade yfinance. O problema pode ser uma instabilidade temporária no servidor de dados.

    A formatação do arquivo CSV parece incorreta: A formatação foi ajustada no código para usar a vírgula (,) como separador decimal, o que é o padrão no Brasil. Se o problema persistir, pode ser uma configuração no seu programa de planilhas.

Desenvolvido por Victor Monteiro.