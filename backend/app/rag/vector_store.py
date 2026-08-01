import chromadb

from app.core.logger import logger


class VectorStore:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path="knowledge_base/chroma"
        )

        self.collection = self.client.get_or_create_collection(
            name="agrisahayak"
        )
       

        logger.success(
            "ChromaDB initialized."
        )

    def add_documents(
    self,
    filename,
    chunks,
    embeddings,
):

        ids = []

        metadatas = []

        for i in range(len(chunks)):

            ids.append(
                f"{filename}_{i}"
            )

            metadatas.append({

                "filename": filename,

                "chunk": i,

            })

        self.collection.add(

            ids=ids,

            documents=chunks,

            embeddings=embeddings,

            metadatas=metadatas,

        )

    def reset(self):

        self.client.delete_collection(
            "agrisahayak"
        )

        self.collection = self.client.get_or_create_collection(

            "agrisahayak"

        )