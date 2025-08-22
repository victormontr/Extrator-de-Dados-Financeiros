## Extrator de Dados Financeiros
### 📖 Sobre o Projeto

Este projeto é uma aplicação de desktop com interface gráfica (GUI) desenvolvida em Python para extrair dados financeiros históricos de empresas listadas na B3 (Bolsa de Valores do Brasil).

A aplicação utiliza a biblioteca yfinance para buscar os dados e permite ao usuário salvar as informações em arquivos CSV ou XLSX, de forma organizada e simples.
Funcionalidades:

    Interface Gráfica Intuitiva: Uma GUI limpa e fácil de usar, construída com Tkinter.

    Busca por Ticker: Seleção da empresa a partir de uma lista completa de tickers da B3, com funcionalidade de autocompletar.

    Seleção de Período: Escolha das datas de início e fim da extração através de um seletor de calendário.

    Frequência de Dados: Opção de extrair dados com diferentes intervalos (diário, semanal, mensal, etc.).

    Exportação Flexível: Salva os dados históricos em formatos de planilha padrão: CSV (otimizado para o Brasil) e XLSX (Excel).

    Processamento Assíncrono: A busca de dados é executada em segundo plano (threading), evitando que a interface congele durante o download.

    Compatibilidade: Funciona nos principais sistemas operacionais (Windows, macOS e Linux).

### Para rodar basta baixar e executar StkExt.exe