import requests
import pandas as pd
import pypdf
import os
import sys
import tempfile
from bs4 import BeautifulSoup

BASE_URL = "https://simpleenergy.com.br/teste/"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

class FileScraper:
    """
    Classe para raspar o conteúdo de arquivos de um site.

    Args:
        None

    Atributos:
        session: Um objeto `requests.Session`.
        data: Uma lista de dicionários, onde cada dicionário representa um arquivo. Cada dicionário tem as seguintes chaves:
            * `File Name`: O nome do arquivo.
            * `File URL`: A URL do arquivo.
            * `File Content`: O conteúdo do arquivo, como uma string.

     Métodos:
        login(code): Entra no site usando o código fornecido.
        extract_text_from_pdf(pdf_url): Extrai o texto de um arquivo PDF no URL fornecido.
        scrape_files(response): Raspa os arquivos do objeto `requests.Response` fornecido.
        download_extracted_file(path, data_frame): Baixa os dados extraídos para um arquivo no diretório fornecido.
        download_files(path): Baixa os arquivos do atributo `data` para o diretório fornecido.
        create_dataframe(): Cria um DataFrame do Pandas do atributo `data`.
    """

    def __init__(self):
        self.session = requests.Session()
        self.data = []

    def login(self, code):
        """
        Entra no site usando o código fornecido.

        Args:
            code: O código a ser usado para fazer login.

        Returns:
            Um objeto `requests.Response`.
        """

        try:
            response = self.session.get(BASE_URL, headers=HEADERS)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            form = soup.find('form', method='post')
            csrf_token = form.find('input', {'name': 'csrf'})['value']

            data = {
                'codigo': code,
                'csrf': csrf_token
            }

            response = self.session.post(BASE_URL, data=data, headers=HEADERS)
            response.raise_for_status()

            return response
        except requests.exceptions.RequestException as e:
            print(f"Erro de solicitação HTTP: {e}")
            sys.exit()

    def extract_text_from_pdf(self, pdf_url):
        """
        Extrai o texto de um arquivo PDF no URL fornecido.

        Args:
            pdf_url: O URL do arquivo PDF.

        Returns:
            Uma string contendo o texto do arquivo PDF.
        """
    
        try:
            response = self.session.get(pdf_url, headers=HEADERS)
            response.raise_for_status()

            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as pdf_file:
                pdf_file.write(response.content)
                pdf_file_name = pdf_file.name
            
            text = ""
            with open(pdf_file_name, 'rb') as pdf_file:
                pdf_reader = pypdf.PdfReader(pdf_file)
                for page_num in range(len(pdf_reader.pages)):
                    text += pdf_reader.pages[page_num].extract_text()

            # Excluindo o arquivo temporário após a extração
            os.remove(pdf_file_name)

            return text
        except (requests.exceptions.RequestException, pypdf.utils.PdfReadError, IOError) as e:
            print(f"Erro ao extrair texto do PDF: {e}")
            sys.exit()

    def scrape_files(self, response):
        """
        Raspa os arquivos do objeto `requests.Response` fornecido.

        Args:
            response: Um objeto `requests.Response`.

        Returns:
            None
        """

        soup = BeautifulSoup(response.content, 'html.parser')

        files = soup.find_all("a", href=True)

        for file in files:
            file_url = BASE_URL + file['href']
            file_name = file.text

            if file_name.endswith('.txt'):
                # Extrai o texto de arquivos txt
                file_content = self.session.get(file_url, headers=HEADERS).text
            elif file_name.endswith('.pdf'):
                # Extrai o texto de arquivos PDF
                file_content = self.extract_text_from_pdf(file_url)

            self.data.append({"File Name": file_name, "File URL": file_url, "File Content": file_content})

    def download_extracted_file(self, path, data_frame):
        """
        Baixa os dados extraídos para um arquivo no diretório fornecido.

        Args:
            path: Um objeto `Path` para o diretório onde o arquivo deve ser baixado.
            data_frame: Um DataFrame do Pandas contendo os dados extraídos.

        Returns:
            None
        """

        file_path = path / "dados.html"
        data_frame.to_html(file_path)

    def download_files(self, path):
        """
        Baixa os arquivos do atributo `data` para o diretório fornecido.

        Args:
            path: Um objeto `Path` para o diretório onde os arquivos devem ser baixados.

        Returns:
            None
        """

        for item in self.data:
            file_url = item["File URL"]

            try:
                response = self.session.get(file_url, headers=HEADERS)
                response.raise_for_status()

                file_path = path / item["File Name"]

                with open(file_path, "wb") as file:
                    file.write(response.content)
            except requests.exceptions.RequestException as e:
                print(f"Erro ao baixar arquivo: {e}")
                sys.exit()

    def create_dataframe(self):
        """
        Cria um DataFrame do Pandas do atributo `data`.

        Returns:
            Um DataFrame do Pandas contendo os dados extraídos.
        """

        df = pd.DataFrame(self.data)
        return df
