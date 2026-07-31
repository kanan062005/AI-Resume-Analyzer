import fitz
import docx


class ResumeParser:

    @staticmethod
    def read_pdf(file_path):
        text = ""

        pdf = fitz.open(file_path)

        for page in pdf:
            text += page.get_text()

        pdf.close()

        return text


    @staticmethod
    def read_docx(file_path):

        document = docx.Document(file_path)

        text = []

        for para in document.paragraphs:
            text.append(para.text)

        return "\n".join(text)


    @staticmethod
    def extract_text(file_path):

        extension = file_path.split(".")[-1].lower()

        if extension == "pdf":
            return ResumeParser.read_pdf(file_path)

        elif extension == "docx":
            return ResumeParser.read_docx(file_path)

        else:
            raise ValueError("Only PDF and DOCX are supported.")