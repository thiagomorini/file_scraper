# File Scraper

Projeto conceito.

## Descrição

O File Scraper é uma ferramenta desenvolvida em Python que permite extrair o conteúdo de arquivos de um site da web. Ele automatiza o processo de login, coleta arquivos de diferentes tipos (PDF e texto), e disponibiliza os dados extraídos em um formato amigável.

## Tecnologias utilizadas

- Python 3.11
- requests 2.31.0
- pandas 2.0.1
- pypdf 3.16.4
- beautifulsoup4 4.12.2
- pytest 7.4.2

## Como usar

Para usar o File Scraper, siga estas etapas:

1. Instale as dependências do projeto usando o comando ```pip install -r requirements.txt```.

2. Inicie o script principal usando o comando ```python main.py```.

3. Digite o código de acesso (321465 ou 98465).

4. O script raspará os arquivos do site e criará um DataFrame do Pandas com as informações de cada arquivo.

5. Você pode visualizar o DataFrame usando o comando ```print(scraper.create_dataframe())```.

6. Se desejar baixar os arquivos, digite "S" na resposta à pergunta "Deseja fazer o download dos arquivos? (S/N)".

Para executar os testes:

1. No terminal, use o comando ```pytest```.

## Contribuição

Você pode contribuir com o File Scraper de várias formas:

1. Reportando bugs e problemas no Github.
2. Fazendo pull requests com correções e novas funcionalidades.
3. Compartilhando o projeto e incentivando outros desenvolvedores a usá-lo.

## Licença
O File Scraper é distribuído sob a licença MIT.

## Contato
Você pode entrar em contato comigo sempre que tiver alguma dúvida ou sugestão de melhorias.
