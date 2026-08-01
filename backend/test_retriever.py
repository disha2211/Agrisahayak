from app.rag.retriever import Retriever
from app.core.registry import model_registry

model_registry.load_models()
retriever = Retriever()

results = retriever.retrieve(

    "Tomato leaf curl disease"

)

print(results["documents"][0])