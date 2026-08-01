from sentence_transformers import SentenceTransformer

from app.core.config import settings
from app.core.logger import logger


class EmbeddingService:

    def __init__(self):

        logger.info(
            "Loading embedding model..."
        )

        self.model = SentenceTransformer(
            settings.EMBEDDING_MODEL
        )

        logger.success(
            "Embedding model loaded."
        )

    def embed(self, text: str):
            return self.model.encode(
                text,
                normalize_embeddings=True
            ).tolist()
    
    def embed_batch(self, texts: list[str]):

        return self.model.encode(
            texts,
            batch_size=32,          # or 16 on lower-memory systems
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=True,
        ).tolist()

   