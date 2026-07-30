from app.rag.loader import DocumentLoader

from app.rag.cleaner import TextCleaner

from app.rag.chunker import TextChunker


class KnowledgePipeline:

    def __init__(self):

        self.loader = DocumentLoader(

            "knowledge_base/raw"

        )

        self.cleaner = TextCleaner()

        self.chunker = TextChunker()

    def run(self):

        docs = self.loader.load_documents()

        processed = []

        for doc in docs:

            clean_text = self.cleaner.clean(

                doc["text"]

            )

            chunks = self.chunker.chunk(

                clean_text

            )

            processed.append({

                "filename":

                    doc["filename"],

                "chunks":

                    chunks

            })

        return processed