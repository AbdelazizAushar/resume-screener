import fitz


def extract_text_from_pdf(file_bytes: bytes) -> str:
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")

        pages_text = []
        for page in doc:
            pages_text.append(page.get_text())

        doc.close()

        full_text = "\n".join(pages_text)
        cleaned_text = "\n".join(
            line.strip() for line in full_text.splitlines() if line.strip()
        )

        # because of image-based pdfs
        if len(cleaned_text) < 50:
            raise ValueError(
                "Could not extract text from this PDF. "
                "It may be a scanned document. "
                "Please paste your resume as text instead."
            )

        return cleaned_text

    except ValueError:
        raise
    except Exception as e:
        raise ValueError(f"Failed to read PDF: {str(e)}")
