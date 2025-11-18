from src.Config import config
from zamzar import ZamzarClient
from zamzar.pagination import after

client = ZamzarClient(config.zamzar_api_key)


# 获取所有可转化的模式
def retrieve_formate() :
    # Retrieve information about a single format
    print("pdfs can be converted to:")
    pdf = client.formats.find("pdf")
    if pdf.targets:
        for target in pdf.targets:
            print(f" - {target.name} ({target.credit_cost} credits)")


def pdf_to_markdown(pdf_path : str) :
    client.convert(pdf_path, 
                target_format='md', 
                source_format='pdf', 
                options={                
                    "ocr": "true"
                }).store('./').delete_all_files()



