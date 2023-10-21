from pathlib import Path
from file_scraper import FileScraper

def main():
    scraper = FileScraper()
    code = input("Digite o código de acesso: ")
    #code = '321465'
    
    response = scraper.login(code)

    if response is not None and response.status_code == 200:
        print("Login bem-sucedido.")
        scraper.scrape_files(response)

        data_frame = scraper.create_dataframe()
        print("Dados extraídos:")
        print(data_frame)

        download_option = input("Deseja fazer o download dos dados extraídos? (S/N): ")
        if download_option.upper() == "S":
            download_directory = Path("downloads")
            download_directory.mkdir(parents=True, exist_ok=True)
            scraper.download_extracted_file(download_directory, data_frame)
            print(f"Arquivo baixados para a pasta '{download_directory}'")

        download_option = input("Deseja fazer o download dos arquivos? (S/N): ")
        if download_option.upper() == "S":
            download_directory = Path("downloads")
            download_directory.mkdir(parents=True, exist_ok=True)
            scraper.download_files(download_directory)
            print(f"Arquivos baixados para a pasta '{download_directory}'")

if __name__ == "__main__":
    main()
