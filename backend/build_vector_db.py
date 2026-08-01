from app.core.registry import model_registry
from app.rag.pipeline import KnowledgePipeline
from app.rag.vector_store import VectorStore

model_registry.load_models()
pipeline = KnowledgePipeline()

documents = pipeline.run()

embedding = model_registry.get("embedding")

db = VectorStore()
db.reset()

for document in documents:

    print(f"Processing {document['filename']}")

    print("Number of chunks:", len(document["chunks"]))

    print("Generating embeddings...")
    vectors = embedding.embed_batch(document["chunks"])
    print("Embeddings generated:", len(vectors))

    print("Adding to Chroma...")
    db.add_documents(
        filename=document["filename"],
        chunks=document["chunks"],
        embeddings=vectors,
    )
    print("Added!")