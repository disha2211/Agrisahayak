from app.core.registry import model_registry
from app.core.services import service_registry


class Retriever:

    def __init__(self):

        self.embedding = model_registry.get(
            "embedding"
        )

        self.db = service_registry.get(
            "vector_store"
        )

    def retrieve(

        self,

        query,

        k=5,

    ):

        embedding = self.embedding.embed(
            query
        )

        results = self.db.collection.query(

            query_embeddings=[embedding],

            n_results=k,

        )

        return results