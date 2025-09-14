# parsers/ingestion.py

import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import docx # <-- NEW IMPORT

MIN_TEXT_LENGTH_FOR_OCR_THRESHOLD = 100

def ingest_document(file_name: str, file_bytes: bytes) -> tuple[str, list[str]]:
    """
    Main ingestion function that dispatches to the correct parser based on file extension.
    """
    interpretation_log = [f"Starting ingestion for '{file_name}'."]
    
    file_ext = file_name.lower().split('.')[-1]

    if file_ext == 'pdf':
        try:
            raw_text, log = _extract_text_from_pdf(file_bytes)
            interpretation_log.extend(log)
            if len(raw_text) < MIN_TEXT_LENGTH_FOR_OCR_THRESHOLD:
                interpretation_log.append(f"Initial text length is below threshold. Attempting OCR.")
                raw_text_ocr, log_ocr = _ocr_pdf(file_bytes)
                interpretation_log.extend(log_ocr)
                return raw_text_ocr, interpretation_log
            return raw_text, interpretation_log
        except Exception as e:
            error_message = f"Failed to process PDF '{file_name}'. Error: {e}"
            interpretation_log.append(error_message)
            return "", interpretation_log

    # --- NEW LOGIC FOR DOCX ---
    elif file_ext == 'docx':
        try:
            raw_text, log = _extract_text_from_docx(file_bytes)
            interpretation_log.extend(log)
            return raw_text, interpretation_log
        except Exception as e:
            error_message = f"Failed to process DOCX '{file_name}'. Error: {e}"
            interpretation_log.append(error_message)
            return "", interpretation_log
    # --------------------------
            
    else:
        unsupported_message = f"Unsupported file type: '{file_name}'. This parser supports PDF and DOCX."
        interpretation_log.append(unsupported_message)
        return "", interpretation_log


def _extract_text_from_pdf(file_bytes: bytes) -> tuple[str, list[str]]:
    """Extracts text directly from a PDF document."""
    log = ["Attempting direct text extraction from PDF."]
    text = ""
    try:
        with fitz.open(stream=file_bytes, filetype="pdf") as doc:
            log.append(f"PDF has {len(doc)} pages.")
            for page in doc:
                text += page.get_text()
        log.append("Direct text extraction successful.")
    except Exception as e:
        log.append(f"Direct text extraction failed: {e}")
    return text, log


def _ocr_pdf(file_bytes: bytes) -> tuple[str, list[str]]:
    """Performs OCR on each page of a PDF document."""
    log = ["Falling back to full-page OCR."]
    text = ""
    try:
        with fitz.open(stream=file_bytes, filetype="pdf") as doc:
            log.append(f"Performing OCR on {len(doc)} pages.")
            for page in doc:
                pix = page.get_pixmap(dpi=300)
                img_bytes = pix.tobytes("png")
                image = Image.open(io.BytesIO(img_bytes))
                page_text = pytesseract.image_to_string(image)
                text += page_text + "\n\n--- Page Break ---\n\n"
            log.append("OCR processing completed.")
    except Exception as e:
        log.append(f"OCR processing failed: {e}")
    return text, log


# --- NEW FUNCTION FOR DOCX EXTRACTION ---
def _extract_text_from_docx(file_bytes: bytes) -> tuple[str, list[str]]:
    """Extracts text from a DOCX document."""
    log = ["Attempting text extraction from DOCX."]
    text = ""
    try:
        # python-docx needs a file-like object, so we use io.BytesIO
        doc = docx.Document(io.BytesIO(file_bytes))
        
        all_paragraphs = [p.text for p in doc.paragraphs]
        text = "\n".join(all_paragraphs)
        
        log.append(f"DOCX extraction successful. Found {len(all_paragraphs)} paragraphs.")
    except Exception as e:
        log.append(f"DOCX extraction failed: {e}")
    return text, log
# ----------------------------------------