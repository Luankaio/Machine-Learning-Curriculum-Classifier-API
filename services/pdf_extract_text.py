import pdftotext

class PdfExtractText:
    def extract_text_from_pdf(pdf_path):
        with open(pdf_path, "rb") as f:
            pdf = pdftotext.PDF(f)
        
        text = "\n\n".join(pdf)

        return text    
