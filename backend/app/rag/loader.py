from pathlib import Path
import fitz


class DocumentLoader:

    def __init__(self, data_dir: str):

        self.data_dir = Path(data_dir)

    def load_documents(self):

        documents = []

        for pdf in self.data_dir.glob("*.pdf"):

            text = ""

            doc = fitz.open(pdf)

            for page in doc:

                text += page.get_text()

            documents.append({

                "filename": pdf.name,

                "text": text

            })

        return documents