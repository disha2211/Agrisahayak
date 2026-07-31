import json

from pathlib import Path

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

        output_dir = Path("knowledge_base/processed")

        output_dir.mkdir(parents=True,exist_ok=True)
        
        for doc in processed:
            output_file = (output_dir/ f"{Path(doc['filename']).stem}.json")
            with open(output_file,"w",encoding="utf-8",) as f:
                json.dump(doc,f,indent=4,ensure_ascii=False,)

        return processed