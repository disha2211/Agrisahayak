from app.rag.retriever import Retriever
from app.tools.base import BaseTool


class KnowledgeRetrievalTool(BaseTool):

    name = "knowledge_retrieval"

    description = (
                    "Search the agricultural knowledge base for "
                "authoritative information about crop diseases, "
                "disease symptoms, disease treatment, pesticides, "
                "fungicides, crop management, and agricultural "
                "recommendations. MUST be used when the farmer "
                "asks what treatment or management is recommended "
                "for a crop disease."
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