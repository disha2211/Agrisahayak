
# RAG Methodology

AgriSahayak uses Retrieval-Augmented Generation to provide the LLM with agricultural evidence from a local knowledge base.

## Pipeline

    Agricultural PDF
          ↓
    Document Loader
          ↓
    Text Cleaning
          ↓
    Chunking
          ↓
    Embedding
          ↓
    ChromaDB
          ↓
    Semantic Retrieval
          ↓
    KnowledgeRetrievalTool
          ↓
    LLM

## 1. Document Loading

DocumentLoader reads documents from:

    backend/knowledge_base/raw/

The current primary source is Agriculture-CPG-2020.pdf.

## 2. Cleaning

TextCleaner preprocesses extracted document text while retaining the agricultural content needed for retrieval.

## 3. Chunking

TextChunker currently uses:
- chunk size: 500 characters
- overlap: 100 characters

The overlap preserves context across chunk boundaries.

## 4. Embeddings

EmbeddingService uses Sentence Transformers.

Each chunk is converted into a vector representation and normalized before storage. At runtime, the farmer query is embedded using the same model.

## 5. Vector Store

ChromaDB is used as a persistent vector store.

Stored information includes:
- chunk text
- embedding
- source filename
- chunk index

The collection is named agrisahayak.

## 6. Retrieval

Retriever:
1. Embeds the incoming query.
2. Queries ChromaDB.
3. Requests the configured number of nearest chunks.
4. Returns documents and metadata.

KnowledgeRetrievalTool exposes the retriever to the agent. The current default is top 10 results.

## 7. Agent Integration

    Farmer question
          ↓
    LLM decides retrieval is needed
          ↓
    KnowledgeRetrievalTool
          ↓
    Retriever
          ↓
    ChromaDB
          ↓
    Retrieved evidence
          ↓
    LLM
          ↓
    Grounded response

RAG retrieves evidence; it does not generate the final answer.

## 8. Offline vs Runtime

Document loading, cleaning, chunking, embedding, and indexing are preprocessing steps.

Runtime requests perform query embedding and retrieval against the existing ChromaDB collection.

## Current Limitation

The current implementation is a straightforward semantic-retrieval pipeline. It does not yet implement reranking, hybrid retrieval, or an evaluation-driven retrieval optimization layer.
