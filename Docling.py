import logging
import time
import sys
from pathlib import Path
from docling.backend.docling_parse_backend import DoclingParseDocumentBackend
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    EasyOcrOptions,
    OcrMacOptions,
    PdfPipelineOptions,
    RapidOcrOptions,
    TesseractCliOcrOptions,
    TesseractOcrOptions,
)
from docling_core.types.doc import ImageRefMode
from docling.document_converter import DocumentConverter, PdfFormatOption

def main(input_doc_path):
    logging.basicConfig(level=logging.INFO)

    # Paths
    input_doc_path = Path(input_doc_path)
    output_dir = Path("scratch")

    # Pipeline options - DISABLE IMAGE PROCESSING
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = True
    pipeline_options.do_table_structure = True
    pipeline_options.table_structure_options.do_cell_matching = True
    pipeline_options.generate_page_images = False  # Disable page images
    pipeline_options.generate_picture_images = False  # Disable picture images

    # OCR options
    ocr_options = TesseractCliOcrOptions(force_full_page_ocr=True)
    pipeline_options.ocr_options = ocr_options

    # Document converter setup
    doc_converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )

    # Conversion and processing
    start_time = time.time()
    conv_res = doc_converter.convert(input_doc_path)

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    doc_filename = conv_res.input.file.stem

    # Create specific directory for markdown file inside scratch
    md_output_dir = output_dir / f"{doc_filename}-md"
    md_output_dir.mkdir(parents=True, exist_ok=True)

    # Export plain Markdown from document
    plain_md = conv_res.document.export_to_markdown()
    plain_md_filename = md_output_dir / f"{doc_filename}-plain.md"
    
    # Save only the plain markdown without images
    with plain_md_filename.open("w") as fp:
        fp.write(plain_md)

    # Logging completion
    end_time = time.time() - start_time
    logging.info(f"Document converted in {end_time:.2f} seconds.")
    logging.info(f"Markdown file saved at: {plain_md_filename}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python docling_script.py <path_to_pdf>")
        sys.exit(1)
    main(sys.argv[1])
