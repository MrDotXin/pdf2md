import html
from docling.document_converter import DocumentConverter
converter = DocumentConverter()


def convert(pdf_path : str, output_path: str) :
    result = converter.convert(pdf_path)
    docling_text = result.document.export_to_markdown()
    # unescape HTML entities
    print('?')
    docling_text = html.unescape(docling_text)
    # save to disk
    print(docling_text)
    with open(output_path, "w", encoding="utf-8") as myfile:
        myfile.write(docling_text)