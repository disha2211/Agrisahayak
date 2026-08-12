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

    def schema(self):

        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": (
                                "The agricultural question "
                                "or topic to search for."
                            ),
                        },
                        "k": {
                            "type": "integer",
                            "description": (
                                "Number of relevant "
                                "documents to retrieve."
                            ),
                            "default": 10,
                        },
                    },
                    "required": ["query"],
                },
            },
        }


    def run(
        self,
        query: str,
        k: int = 10,
    ):
        k = int(k)
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