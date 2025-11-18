import pymupdf4llm
import pathlib


def convert(pdf_path : str, output_path: str):
    md_text = pymupdf4llm.to_markdown(pdf_path)
    # save to disk
    pathlib.Path(output_path).write_bytes(md_text.encode())