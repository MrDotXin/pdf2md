from pdfdeal import Doc2X
from src.Config import config

client = Doc2X(apikey=config.doc2x_api_key, debug=True, thread=5)


def convert(pdf_path : str, output_dir : str) :
    return client.pdf2file(
        pdf_file=pdf_path,
        output_path=output_dir,
        ocr=True
    )