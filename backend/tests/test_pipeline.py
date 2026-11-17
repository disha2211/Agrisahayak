from pprint import pprint

from app.rag.pipeline import (

    KnowledgePipeline

)

pipeline = KnowledgePipeline()

documents = pipeline.run()

pprint(documents)