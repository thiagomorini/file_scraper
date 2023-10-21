import pytest
import requests
import os
from file_scraper import FileScraper
from pathlib import Path

@pytest.fixture
def fixture_response():
    scraper = FileScraper()
    response = scraper.login(321465)
    return response

@pytest.fixture
def fixture_data(fixture_response):
    scraper = FileScraper()
    scraper.scrape_files(fixture_response)
    return scraper.data

@pytest.fixture
def fixture_data_frame(fixture_data):
    scraper = FileScraper()
    scraper.data = fixture_data
    return scraper.create_dataframe()

def test_login(fixture_response):
    """Testa o método `login()`."""

    # Verifica se a resposta é um objeto `requests.Response`
    assert isinstance(fixture_response, requests.Response)

    # Verifica se o código de resposta é 200
    assert fixture_response.status_code == 200

def test_extract_text_from_pdf():
    """Testa o método `extract_text_from_pdf()`."""

    scraper = FileScraper()
    text = scraper.extract_text_from_pdf('https://simpleenergy.com.br/teste/arquivo1-321465.pdf')

    # Verifica se o texto não está vazio
    assert text != ""

def test_scrape_files(fixture_data):
    """Testa o método `scrape_files()`."""

    # Verifica se o atributo `data` não está vazio
    assert fixture_data != []

def test_download_extracted_file(fixture_data_frame):
    """Testa o método `download_extracted_file()`."""

    data_frame = fixture_data_frame
    download_directory = Path("downloads")
    download_directory.mkdir(parents=True, exist_ok=True)

    scraper = FileScraper()
    scraper.download_extracted_file(download_directory, data_frame)

    # Verifica se o arquivo foi baixado
    assert os.path.exists(download_directory / "dados.html")

def test_download_files(fixture_data):
    """Testa o método `download_files()`."""

    download_directory = Path("downloads")
    download_directory.mkdir(parents=True, exist_ok=True)

    scraper = FileScraper()
    scraper.data = fixture_data
    scraper.download_files(download_directory)

    # Verifica se os arquivos foram baixados
    for item in scraper.data:
        file_path = download_directory / item["File Name"]
        assert os.path.exists(file_path)

def test_create_dataframe(fixture_data_frame):
    """Testa o método `create_dataframe()`."""

    df = fixture_data_frame

    # Verifica se o DataFrame contém as colunas esperadas
    assert list(df.columns) == ["File Name", "File URL", "File Content"]
