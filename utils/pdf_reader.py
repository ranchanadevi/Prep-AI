from PyPDF2 import PdfReader

class PDFReader:
    @staticmethod
    def extract_text(file_path):
        """Extracts text from a PDF file."""
        text = ""
        try:
            reader = PdfReader(file_path)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        except Exception as e:
            print(f"Error reading PDF file {file_path}: {e}")
        return text.strip()
