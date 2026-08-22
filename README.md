# 🌾 AgriSahayak AI

### Agentic AI-Powered Agricultural Assistant

AgriSahayak AI is an **agentic agricultural intelligence platform** that combines computer vision, Retrieval-Augmented Generation (RAG), large language models, and domain-specific tools to assist farmers with crop disease identification and agricultural queries.

Instead of treating disease detection and knowledge retrieval as isolated features, AgriSahayak uses an **LLM-powered Farmer Agent** that dynamically decides when to use specialized tools.

The system currently combines:

- 🌱 **Plant disease detection using YOLO**
- 🤖 **LLM-powered agricultural assistant**
- 🧠 **Agentic tool calling**
- 📚 **Retrieval-Augmented Generation (RAG)**
- 🔎 **Semantic agricultural knowledge retrieval**
- 🗃️ **Persistent ChromaDB vector store**
- 🧩 **Modular tool registry**
- ⚙️ **Service and model registries**
- 🦙 **Local LLM inference through Ollama**
- ⚡ **FastAPI backend**
- 📄 **Agricultural PDF knowledge base**
- 🕷️ **TNAU agricultural knowledge extraction pipeline**

---

# 🚀 What Makes AgriSahayak Different?

Traditional agricultural applications typically follow a fixed pipeline:

```text
User
 ↓
Disease Model
 ↓
Prediction
```

AgriSahayak is being designed around an **agentic workflow**:

```text
                         ┌──────────────────┐
                         │      Farmer      │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │   Farmer Agent   │
                         │      (LLM)       │
                         └────────┬─────────┘
                                  │
                     ┌────────────┼────────────┐
                     │            │            │
                     ▼            ▼            ▼
              Disease Tool   Knowledge Tool   Future Tools
                     │            │
                     ▼            ▼
                  YOLO         ChromaDB
                     │            │
                     └─────┬──────┘
                           ▼
                    Tool Results
                           │
                           ▼
                         LLM
                           │
                           ▼
                   Farmer-Friendly
                       Response
```

The LLM acts as the **reasoning and orchestration layer**, while specialized tools provide reliable capabilities.

---

# ✨ Features

## 1. 🤖 Agentic Agricultural Assistant

The `/chat` endpoint provides the primary conversational interface.

```http
POST /chat
```

The user sends a natural-language agricultural question:

```json
{
  "message": "What disease is affecting my tomato plant?"
}
```

The `FarmerAgent` sends the request to the configured LLM and exposes the available agricultural tools.

The LLM can decide whether it needs to invoke:

- Disease Detection
- Agricultural Knowledge Retrieval

The agent then executes the selected tools and feeds their results back into the LLM.

---

# 2. 🧠 LLM Tool Calling

The latest architecture introduces an explicit tool-calling system.

The LLM does not directly execute application functionality.

Instead:

```text
LLM
 ↓
Tool Call
 ↓
Tool Registry
 ↓
Tool
 ↓
Tool Result
 ↓
LLM
```

This creates a controlled boundary between the language model and application capabilities.

The current implementation uses **Ollama** for local LLM inference.

---

# 3. 🛠️ Tool Architecture

Every AI capability exposed to the agent implements a common interface:

```python
class BaseTool:
    run(...)
    schema(...)
```

This allows tools to be dynamically registered and exposed to the LLM.

Current tools include:

### Disease Detection Tool

```text
disease_detection
```

Purpose:

> Analyze a plant image and detect possible plant diseases with confidence scores.

Internally it uses the registered disease model.

---

### Knowledge Retrieval Tool

```text
knowledge_retrieval
```

Purpose:

> Search the agricultural knowledge base for relevant information about crops, diseases, treatments, cultivation practices, and agricultural recommendations.

Internally it uses the RAG retriever and ChromaDB.

---

# 4. 🧩 Tool Registry

Tools are managed through a centralized:

```text
ToolRegistry
```

Tools are registered during application startup:

```text
ToolRegistry
 ├── disease_detection
 └── knowledge_retrieval
```

The Farmer Agent dynamically retrieves:

```python
tool.schema()
```

for every registered tool.

This means adding a new capability does not require rewriting the agent.

A future tool could therefore be introduced as:

```text
WeatherTool
MarketPriceTool
CropRecommendationTool
GovernmentSchemeTool
```

without changing the fundamental agent architecture.

---

# 5. 🌱 Plant Disease Detection

AgriSahayak integrates an Ultralytics YOLO-based disease detection model.

The model can analyze uploaded plant images and return predictions containing:

- disease class
- confidence score

The disease service then passes the prediction to `DiseaseAgent`.

The current flow is:

```text
Plant Image
     ↓
Image Validation
     ↓
Temporary File
     ↓
YOLO Model
     ↓
Disease Prediction
     ↓
Disease Agent
     ↓
Structured Analysis
```

---

# 6. 🧠 Disease Analysis Agent

The `DiseaseAgent` provides a domain-specific interpretation layer over the raw YOLO prediction.

It maps disease classes to agricultural information including:

- Crop
- Disease
- Confidence
- Severity
- Recommended action
- Weather requirement
- RAG requirement

This creates a separation between:

```text
Disease Model
"What was detected?"
```

and:

```text
Disease Agent
"What does the detection mean?"
```

---

# 7. 📚 Retrieval-Augmented Generation

AgriSahayak contains a domain-specific agricultural knowledge system.

The current primary knowledge source is:

**Agriculture Crop Production Guide (Agriculture-CPG-2020)**

The RAG architecture is:

```text
Agricultural Documents
        ↓
Document Loader
        ↓
Text Cleaner
        ↓
Text Chunker
        ↓
Embedding Model
        ↓
ChromaDB
        ↓
Semantic Retrieval
```

---

# 8. 🔎 Semantic Knowledge Retrieval

The `KnowledgeRetrievalTool` exposes the RAG system to the Farmer Agent.

A query such as:

```text
How do I control tomato leaf curl disease?
```

can be converted into an embedding and searched against the agricultural knowledge base.

The retriever returns:

- relevant documents
- document metadata
- source information

The current tool supports configurable retrieval size:

```text
k = 10
```

---

# 9. 🗃️ ChromaDB Vector Store

AgriSahayak uses **ChromaDB** as a persistent vector database.

The vector store maintains:

- document chunks
- embeddings
- source filenames
- chunk metadata

The collection is:

```text
agrisahayak
```

The vector database is persisted under:

```text
backend/knowledge_base/chroma/
```

This allows the expensive embedding/indexing process to be performed separately from runtime retrieval.

---

# 10. 📄 Agricultural Knowledge Pipeline

The PDF ingestion pipeline processes agricultural documents through several stages.

```text
PDF
 ↓
DocumentLoader
 ↓
TextCleaner
 ↓
TextChunker
 ↓
JSON Processing
 ↓
EmbeddingService
 ↓
ChromaDB
```

The current knowledge source includes:

```text
Agriculture-CPG-2020.pdf
```

Processed output is stored under:

```text
knowledge_base/processed/
```

---

# 🏗️ System Architecture

The latest architecture can be represented as:

```text
                              ┌──────────────────────┐
                              │        Farmer        │
                              └──────────┬───────────┘
                                         │
                                         ▼
                              ┌──────────────────────┐
                              │      FastAPI API     │
                              │                      │
                              │  /chat               │
                              │  /disease/predict    │
                              │  /health             │
                              └──────────┬───────────┘
                                         │
                                         ▼
                              ┌──────────────────────┐
                              │     FarmerAgent      │
                              │                      │
                              │ LLM + Tool Calling   │
                              └──────────┬───────────┘
                                         │
                              ┌──────────┴──────────┐
                              │                     │
                              ▼                     ▼
                    ┌──────────────────┐  ┌──────────────────┐
                    │ Disease Detection│  │ Knowledge        │
                    │ Tool             │  │ Retrieval Tool   │
                    └────────┬─────────┘  └────────┬─────────┘
                             │                     │
                             ▼                     ▼
                    ┌──────────────────┐  ┌──────────────────┐
                    │   YOLO Model     │  │    Retriever     │
                    └──────────────────┘  └────────┬─────────┘
                                                   │
                                                   ▼
                                          ┌──────────────────┐
                                          │    ChromaDB      │
                                          │ Agricultural KB  │
                                          └──────────────────┘

                              ┌──────────────────────┐
                              │     Ollama LLM       │
                              │  Local Inference     │
                              └──────────────────────┘
```

---

# 🔄 Agent Execution Flow

The current Farmer Agent follows an iterative tool-calling loop.

```text
User Query
    │
    ▼
FarmerAgent
    │
    ▼
Ollama LLM
    │
    ├── No tool required
    │       ↓
    │   Final response
    │
    └── Tool required
            │
            ▼
       Tool Selection
            │
            ▼
       Tool Registry
            │
            ▼
       Tool Execution
            │
            ▼
        Tool Result
            │
            ▼
       Ollama LLM
            │
            ├── Another tool required
            │       ↓
            │    Repeat
            │
            └── Final answer
```

This allows the agent to perform **multi-step reasoning through tools** instead of following a hard-coded sequence.

---

# 🧱 Architectural Components

## API Layer

Responsible for HTTP communication.

```text
app/api/
```

Current endpoints include:

```text
GET  /health
GET  /disease/status
POST /disease/predict
POST /chat
```

---

## Agent Layer

```text
app/agents/
```

Contains:

- `FarmerAgent`
- `DiseaseAgent`

### FarmerAgent

Responsible for:

- interacting with the LLM
- exposing tool schemas
- processing tool calls
- executing tools
- returning the final response

### DiseaseAgent

Responsible for:

- interpreting disease predictions
- applying disease-specific domain rules

---

## Tool Layer

```text
app/tools/
```

Contains:

- `BaseTool`
- `DiseaseDetectionTool`
- `KnowledgeRetrievalTool`

This layer provides the controlled interface between the LLM and application capabilities.

---

## Service Layer

```text
app/services/
```

Contains:

- `DiseaseService`
- `HealthService`
- `LLMService`

`LLMService` abstracts Ollama communication away from the agent itself.

---

## Model Layer

```text
app/models/
```

Contains the computer-vision inference implementation.

The model lifecycle is managed through:

```text
ModelRegistry
```

Current registered models:

```text
disease
embedding
```

---

## RAG Layer

```text
app/rag/
```

Contains:

- Document Loader
- Cleaner
- Chunker
- Embedding Service
- Vector Store
- Retriever
- Knowledge Pipeline

---

# 📁 Project Structure

```text
Agrisahayak-ai/
│
├── backend/
│   │
│   ├── app/
│   │   │
│   │   ├── agents/
│   │   │   ├── disease_agent.py
│   │   │   └── farmer_agent.py
│   │   │
│   │   ├── api/
│   │   │   ├── dependencies.py
│   │   │   └── routes/
│   │   │       ├── chat.py
│   │   │       ├── disease.py
│   │   │       └── health.py
│   │   │
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── constants.py
│   │   │   ├── logger.py
│   │   │   ├── model_registry.py
│   │   │   ├── registry.py
│   │   │   ├── services.py
│   │   │   ├── service_registry.py
│   │   │   ├── tools.py
│   │   │   └── tool_registry.py
│   │   │
│   │   ├── exceptions/
│   │   │   └── disease.py
│   │   │
│   │   ├── models/
│   │   │   └── disease_model.py
│   │   │
│   │   ├── rag/
│   │   │   ├── cleaner.py
│   │   │   ├── chunker.py
│   │   │   ├── embeddings.py
│   │   │   ├── loader.py
│   │   │   ├── pipeline.py
│   │   │   ├── retriever.py
│   │   │   └── vector_store.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── agent.py
│   │   │   ├── chat.py
│   │   │   └── disease.py
│   │   │
│   │   ├── services/
│   │   │   ├── disease_service.py
│   │   │   ├── health_service.py
│   │   │   └── llm_service.py
│   │   │
│   │   ├── tools/
│   │   │   ├── base.py
│   │   │   ├── disease_tool.py
│   │   │   └── rag_tool.py
│   │   │
│   │   └── utils/
│   │       ├── file_manager.py
│   │       └── validators.py
│   │
│   ├── knowledge_base/
│   │   ├── chroma/
│   │   ├── processed/
│   │   └── raw/
│   │
│   ├── build_vector_db.py
│   ├── test_pipeline.py
│   ├── test_retriever.py
│   └── test_tools.py
│
│
├── data/
│   └── sample images
│
├── README.md
└── requirements.txt
```

---

# 🧠 Architectural Decisions

## 1. Move from Fixed Pipelines to Agentic Orchestration

The most important recent architectural decision is introducing the `FarmerAgent`.

Previously:

```text
API
 ↓
Specific Service
 ↓
Specific Model
```

The newer architecture introduces:

```text
API
 ↓
FarmerAgent
 ↓
LLM
 ↓
Tools
```

The LLM can determine which capability is required for a query.

This is the foundation for making AgriSahayak a true **agentic AI system** rather than a collection of independent AI APIs.

---

# 2. Tool Calling Instead of Direct LLM Access

The LLM does not directly access the database or model.

Instead, it receives structured tool schemas.

```text
LLM
 ↓
Tool Schema
 ↓
Tool Call
 ↓
Application Tool
```

This provides a controlled interface between probabilistic LLM reasoning and deterministic application functionality.

---

# 3. Local LLM Through Ollama

The project currently uses Ollama as the LLM runtime.

```text
FarmerAgent
     ↓
LLMService
     ↓
Ollama Client
     ↓
Local LLM
```

This provides:

- local inference
- reduced dependency on external LLM APIs
- control over the selected model
- easier experimentation with different local models

The model and Ollama host are configurable through environment variables.

---

# 4. Tool Registry for Extensibility

Tools are registered independently from the Farmer Agent.

```text
ToolRegistry
     │
     ├── DiseaseDetectionTool
     ├── KnowledgeRetrievalTool
     │
     └── Future tools
```

The Farmer Agent does not need to know the implementation details of individual tools.

This makes the architecture extensible.

---

# 5. Service Registry

A separate `ServiceRegistry` manages runtime services.

Current services include:

```text
vector_store
llm
```

This allows agents and tools to retrieve shared infrastructure without tightly coupling themselves to concrete implementations.

---

# 6. Model Registry

ML models are loaded once during application startup.

```text
ModelRegistry
     │
     ├── Disease Model
     └── Embedding Model
```

This avoids repeatedly loading expensive models for individual requests.

---

# 7. Separate Agent Reasoning from Domain Logic

There are now two different reasoning responsibilities:

### FarmerAgent

Handles:

```text
LLM reasoning
Tool selection
Tool orchestration
Final response generation
```

### DiseaseAgent

Handles:

```text
Disease-specific domain interpretation
Severity
Recommended action
Disease metadata
```

This prevents the general-purpose conversational agent from becoming tightly coupled to disease-specific rules.

---

# 8. RAG as an Agent Tool

The RAG system is no longer merely a standalone retrieval API.

It is exposed as:

```text
KnowledgeRetrievalTool
```

This is an important architectural shift.

The agent can now decide when agricultural knowledge retrieval is necessary.

---

# 9. Offline Knowledge Processing

Expensive operations such as:

- PDF extraction
- cleaning
- chunking
- embedding
- vector indexing

are performed separately from runtime inference.

Runtime requests only perform retrieval.

This keeps the API responsive and reduces unnecessary computation.

---

# 10. Modular Extension Strategy

The current architecture makes it possible to introduce future agricultural tools such as:

```text
WeatherTool
MarketPriceTool
CropRecommendationTool
GovernmentSchemeTool
FertilizerRecommendationTool
IrrigationTool
```

without rewriting the Farmer Agent.

The intended architecture becomes:

```text
                    FarmerAgent
                         │
        ┌────────────────┼─────────────────┐
        │                │                 │
        ▼                ▼                 ▼
 Disease Tool       RAG Tool        Weather Tool
        │                │                 │
        ▼                ▼                 ▼
       YOLO           ChromaDB         Weather API
```

---

# 🔐 Safety-Oriented Design

The Farmer Agent system prompt explicitly instructs the model:

> Use tools whenever reliable external agricultural knowledge is required.

and:

> Never invent treatment advice.

This establishes an important design principle:

**Agricultural recommendations should be grounded in available domain tools and knowledge sources rather than relying entirely on unconstrained LLM generation.**

This becomes increasingly important as more agricultural decision-support capabilities are added.

---

# 🔌 API

## Chat

```http
POST /chat
```

Request:

```json
{
  "message": "How can I control tomato leaf curl disease?"
}
```

The Farmer Agent may invoke:

```text
knowledge_retrieval
```

before generating the final response.

---

## Disease Prediction

```http
POST /disease/predict
```

Upload a plant image using multipart form-data.

The image is:

1. validated
2. temporarily stored
3. processed by YOLO
4. interpreted by `DiseaseAgent`
5. deleted after processing

---

## Disease Status

```http
GET /disease/status
```

Returns the current disease service status.

---

## Health

```http
GET /health
```

Used to verify backend availability.

---

# ⚙️ Configuration

Create:

```text
backend/.env
```

Example:

```env
PROJECT_NAME=AgriSahayak AI
PROJECT_VERSION=1.0.0
DEBUG=True

HOST=127.0.0.1
PORT=8000

DISEASE_MODEL_PATH=models/best.pt

EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

WHISPER_MODEL=base

LLM_MODEL=<ollama-model>

OLLAMA_HOST=http://localhost:11434
```

The exact LLM model can be changed without modifying the Farmer Agent.

---

# ▶️ Running the Project

## 1. Clone

```bash
git clone <your-repository-url>
cd Agrisahayak-ai
```

---

## 2. Create virtual environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python -m venv .venv
source .venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

Or install backend dependencies:

```bash
cd backend
pip install -r requirements.txt
```

---

# 🦙 Running Ollama

Install and run Ollama separately.

Make sure the configured model is available locally.

For example:

```bash
ollama pull <model-name>
```

Then verify Ollama:

```bash
ollama list
```

The backend connects to the configured:

```text
OLLAMA_HOST
```

---

# ▶️ Start the Backend

From the backend directory:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 🧠 Build the Knowledge Base

To process the agricultural documents:

```bash
python build_vector_db.py
```

The pipeline performs:

```text
PDF
 ↓
Extraction
 ↓
Cleaning
 ↓
Chunking
 ↓
Embeddings
 ↓
ChromaDB
```

---

# 🧪 Testing

The repository includes tests for:

```text
test_pipeline.py
test_retriever.py
test_tools.py
```

Tool registration can be inspected using:

```bash
python test_tools.py
```

---


# 🚧 In Progress / Future Work

The architecture provides the foundation for several capabilities that are not yet fully implemented.

- [ ] Integrate image upload directly into conversational `/chat`
- [ ] Connect disease predictions and RAG results into a unified conversational workflow
- [ ] Weather intelligence tool
- [ ] Crop recommendation tool
- [ ] Market price tool
- [ ] Fertilizer recommendation tool
- [ ] Voice interaction
- [ ] Multilingual farmer interaction
- [ ] More crop/disease models
- [ ] Production-grade model evaluation
- [ ] RAG evaluation and grounding metrics
- [ ] Frontend/mobile application
- [ ] Production deployment
- [ ] Persistent conversation memory

---

# 🔮 Target Architecture

The long-term objective is to evolve AgriSahayak into a **multimodal agricultural agent**.

```text
                              ┌──────────────────────┐
                              │        Farmer        │
                              └──────────┬───────────┘
                                         │
                                         ▼
                              ┌──────────────────────┐
                              │     AgriSahayak      │
                              │     Farmer Agent     │
                              └──────────┬───────────┘
                                         │
                  ┌──────────────────────┼──────────────────────┐
                  │                      │                      │
                  ▼                      ▼                      ▼
          ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
          │ Disease Tool │      │   RAG Tool   │      │ Weather Tool │
          └──────┬───────┘      └──────┬───────┘      └──────┬───────┘
                 │                     │                     │
                 ▼                     ▼                     ▼
              YOLO                  ChromaDB             Weather API
                 │                     │                     │
                 └─────────────────────┼─────────────────────┘
                                       │
                                       ▼
                              ┌──────────────────────┐
                              │       LLM            │
                              │  Reasoning Layer     │
                              └──────────┬───────────┘
                                         │
                                         ▼
                              ┌──────────────────────┐
                              │ Farmer-Friendly      │
                              │ Grounded Response    │
                              └──────────────────────┘
```

---

# 🎯 Design Philosophy

AgriSahayak is built around five principles.

### 1. Agentic

Use an LLM to determine which capabilities are required instead of hard-coding every workflow.

### 2. Tool-Grounded

Give the LLM access to deterministic tools for specialized tasks.

### 3. Knowledge-Grounded

Use agricultural reference material when reliable domain knowledge is required.

### 4. Modular

Keep models, agents, tools, services, retrieval, and API layers independently replaceable.

### 5. Extensible

New agricultural capabilities should be addable as tools rather than requiring a redesign of the agent.

---

# 🌱 Project Vision

AgriSahayak aims to evolve from a **crop disease detection system** into a **multimodal agricultural decision-support agent**.

The final goal is not simply to answer:

> *“What disease is this?”*

but to help answer:

> *“What is happening to my crop, why is it happening, what should I do, and what reliable agricultural information supports that recommendation?”*

The current agentic + RAG architecture establishes the foundation for that system.

---

# 📜 License

Add the project's chosen license here.

---

## 🌾 AgriSahayak AI

**An agentic agricultural assistant combining computer vision, RAG, and LLM-powered tool use.**
