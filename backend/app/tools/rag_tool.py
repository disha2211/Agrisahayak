from app.rag.retriever import Retriever
from app.tools.base import BaseTool


class KnowledgeRetrievalTool(BaseTool):

    name = "knowledge_retrieval"

    description = (
        "Search the agricultural knowledge base for "
        "relevant information about crops, diseases, "
        "treatments, cultivation practices, and "
        "agricultural recommendations."
    )

    def __init__(self):

        self.retriever = Retriever()

    def run(
        self,
        query: str,
        k: int = 5,
    ):

        results = self.retriever.retrieve(
            query=query,
            k=k,
        )

        documents = results.get(
            "documents",
            [[]],
        )[0]

        metadatas = results.get(
            "metadatas",
            [[]],
        )[0]

        return {
            "query": query,
            "documents": documents,
            "metadata": metadatas,
        }