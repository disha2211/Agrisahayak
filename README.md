# 🌾 AgriSahayak AI

**AI-Powered Agricultural Disease Detection and Knowledge Assistant**

AgriSahayak AI is an AI-driven agriculture assistance platform designed to help farmers identify crop diseases from plant images and support diagnosis with trusted agricultural knowledge.

The system combines **computer vision, domain-specific knowledge, semantic search, and an agent-based decision layer** into a modular backend architecture.

---

## 🚀 Overview

Farmers often face difficulty identifying crop diseases and determining appropriate actions quickly. AgriSahayak AI addresses this by combining image-based disease detection with a retrieval-based agricultural knowledge system.

The current backend provides:

- 🌱 Crop disease detection from plant images
- 🧠 AI-based disease analysis
- 📚 Agricultural knowledge retrieval using RAG
- 🔎 Semantic search over agricultural documents
- 🗃️ Persistent ChromaDB vector storage
- 📄 PDF-based agricultural knowledge ingestion
- 🕷️ Web-based agricultural knowledge extraction pipeline
- 🧩 Modular model registry
- ⚡ FastAPI REST API
- 🛡️ Image validation and temporary file management
- 📊 Health and service-status endpoints
- 📝 Structured logging

The architecture is designed so that additional capabilities such as **weather intelligence, LLM-based recommendations, voice interaction, and additional crop/disease models** can be integrated without redesigning the core system.

---

# ✨ Features

## 1. Plant Disease Detection

Users can upload a plant image through the FastAPI API.

The system:

1. Validates the uploaded image.
2. Stores it temporarily.
3. Passes it to the disease detection model.
4. Extracts detected disease classes and confidence scores.
5. Sends the prediction to the disease analysis agent.
6. Returns structured disease information.
7. Deletes the temporary image.

Currently, the disease model is implemented using **Ultralytics YOLO**.

Supported image formats:

- `.jpg`
- `.jpeg`
- `.png`

Maximum upload size:

- **10 MB**

---

## 2. Disease Analysis Agent

The `DiseaseAgent` provides a domain-specific interpretation layer on top of raw model predictions.

Instead of returning only:

```text
Disease = Tomato___Late_Blight
Confidence = 0.91
```

the agent maps the prediction to agricultural domain information such as:

- Crop
- Disease
- Confidence
- Severity
- Recommended action
- Whether weather information may be required
- Whether RAG retrieval may be required

Example:

```json
{
  "crop": "Tomato",
  "disease": "Tomato___Late_Blight",
  "confidence": 0.91,
  "severity": "High",
  "recommended_action": "Spray fungicide immediately.",
  "needs_weather": true,
  "needs_rag": true
}
```

This creates a separation between **model prediction** and **agricultural reasoning**.

---

# 📚 Retrieval-Augmented Generation Knowledge System

AgriSahayak contains a domain-specific RAG foundation for agricultural information.

The current knowledge base includes the:

**Agriculture Crop Production Guide (Agriculture-CPG-2020)**

The RAG pipeline consists of:

```text
PDF Documents
      ↓
Document Loader
      ↓
Text Cleaning
      ↓
Text Chunking
      ↓
Embedding Generation
      ↓
ChromaDB
      ↓
Semantic Retrieval
```

---

## 3. Document Ingestion

PDF documents are loaded using PyMuPDF.

The `DocumentLoader`:

- scans the knowledge-base directory
- opens PDF documents
- extracts text page-by-page
- associates extracted text with the source filename

---

## 4. Text Cleaning

Extracted PDF text is normalized before indexing.

The cleaner:

- removes newline fragmentation
- normalizes whitespace
- produces cleaner text for downstream chunking

---

## 5. Text Chunking

Documents are divided into overlapping chunks.

Current configuration:

```text
Chunk size: 500 characters
Overlap:    100 characters
```

The overlap helps preserve contextual continuity between neighboring chunks.

---

## 6. Semantic Embeddings

The system uses **Sentence Transformers** to convert agricultural text into vector representations.

Embeddings are normalized before storage, allowing efficient semantic similarity retrieval.

Batch embedding is also supported for more efficient knowledge-base construction.

---

## 7. ChromaDB Vector Store

AgriSahayak uses **ChromaDB** as its persistent vector database.

Each stored chunk contains:

- unique chunk ID
- source filename
- chunk index
- original chunk text
- embedding vector

This allows agricultural information to be retrieved based on semantic similarity rather than simple keyword matching.

---

## 8. Semantic Retriever

The `Retriever` converts a user query into an embedding and queries ChromaDB for the most relevant knowledge chunks.

Example query:

```text
Tomato leaf curl disease
```

The retriever returns the most semantically relevant agricultural information.

The default retrieval size is:

```text
k = 5
```

---

# 🕷️ Generic Agricultural Knowledge Pipeline

The repository also contains a separate experimental/general-purpose knowledge ingestion pipeline under:

```text
generic_KB/
```

This pipeline was designed to collect crop information from the **Tamil Nadu Agricultural University (TNAU)** agricultural website and transform it into structured Markdown knowledge bases.

The pipeline follows:

```text
TNAU Website
     ↓
Crawler
     ↓
Raw HTML
     ↓
HTML Parser
     ↓
HTML Cleaner
     ↓
Markdown Builder
     ↓
Markdown Normalizer
     ↓
Crop Knowledge Base
```

---

## 9. Web Crawler

The `TNAUCrawler`:

- downloads agricultural webpages
- discovers crop-specific links
- restricts crawling to the TNAU domain
- skips irrelevant navigation pages
- retries failed HTTP requests
- introduces request delays
- stores raw HTML locally

Configured crop targets include:

- Tomato
- Potato
- Cotton
- Rice

---

## 10. HTML Parsing and Cleaning

The knowledge pipeline removes web-specific noise such as:

- navigation
- headers
- footers
- scripts
- styles
- breadcrumbs
- duplicate links
- comments
- irrelevant text
- empty HTML elements

The parser attempts to identify the largest meaningful content region from each page.

---

## 11. Markdown Knowledge Base Generation

Cleaned agricultural webpages are converted into Markdown.

Generated documents include metadata such as:

```yaml
---
title: Tomato
crop: Tomato
source: TNAU
category: Crop Production
language: English
---
```

Multiple pages belonging to a crop can be merged into a unified crop knowledge document.

---

## 12. Knowledge Normalization

The Markdown normalization stage removes or reduces:

- duplicate paragraphs
- duplicate headings
- excessive blank lines
- repeated separators
- irrelevant navigation words

This was intended to make web-extracted agricultural information more suitable for downstream knowledge retrieval.

---

# 🏗️ Architecture

AgriSahayak follows a modular layered architecture.

```text
                    ┌───────────────────────┐
                    │       Client          │
                    │ Web / Mobile / UI     │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │       FastAPI         │
                    │    API Layer          │
                    └───────────┬───────────┘
                                │
                    ┌───────────▼───────────┐
                    │       Services         │
                    │ DiseaseService         │
                    │ HealthService          │
                    └───────┬─────────┬─────┘
                            │         │
                ┌───────────▼───┐ ┌──▼──────────────┐
                │ Disease Model │ │ Disease Agent  │
                │    YOLO       │ │ Domain Logic   │
                └───────────────┘ └───────┬────────┘
                                          │
                                  ┌───────▼────────┐
                                  │      RAG       │
                                  │                │
                                  │ Retriever      │
                                  │ Embeddings     │
                                  │ Vector Store   │
                                  └───────┬────────┘
                                          │
                                  ┌───────▼────────┐
                                  │    ChromaDB    │
                                  │ Agricultural   │
                                  │ Knowledge Base │
                                  └────────────────┘
```

---

# 📁 Project Structure

```text
Agrisahayak-ai/
│
├── backend/
│   │
│   ├── app/
│   │   ├── agents/
│   │   │   └── disease_agent.py
│   │   │
│   │   ├── api/
│   │   │   ├── dependencies.py
│   │   │   └── routes/
│   │   │       ├── disease.py
│   │   │       └── health.py
│   │   │
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── constants.py
│   │   │   ├── logger.py
│   │   │   ├── model_registry.py
│   │   │   └── registry.py
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
│   │   │   └── disease.py
│   │   │
│   │   ├── services/
│   │   │   ├── disease_service.py
│   │   │   └── health_service.py
│   │   │
│   │   └── utils/
│   │       ├── file_manager.py
│   │       └── validators.py
│   │
│   ├── knowledge_base/
│   │   ├── raw/
│   │   ├── processed/
│   │   └── chroma/
│   │
│   ├── build_vector_db.py
│   ├── test_pipeline.py
│   └── test_retriever.py
│
├── generic_KB/
│   └── backend/
│       └── app/
│           ├── knowledge_pipeline/
│           │   ├── crawler.py
│           │   ├── parser.py
│           │   ├── cleaner.py
│           │   ├── markdown_builder.py
│           │   ├── normalizer.py
│           │   └── config.py
│           │
│           └── knowledge_base/
│               └── crops/
│                   └── tomato.md
│
├── data/
│   └── sample images
│
└── requirements.txt
```

---

# 🧠 Architectural Decisions

The repository's Git history shows that the architecture was developed incrementally rather than as a single monolithic implementation.

Several important architectural decisions can be extracted from that evolution.

## 1. Layered Backend Architecture

The project separates:

```text
API
 ↓
Service
 ↓
Model / Agent
 ↓
Infrastructure
```

For example:

```text
disease.py
    ↓
DiseaseService
    ↓
DiseaseModel
    ↓
YOLO
```

This prevents API routes from directly containing model inference logic.

**Decision:** Keep HTTP/API concerns separate from business logic and ML inference.

**Benefit:** Individual components can be changed without rewriting the API layer.

---

## 2. Model Registry

Models are initialized through a centralized `ModelRegistry`.

```text
ModelRegistry
 ├── disease model
 └── embedding model
```

Models are loaded during FastAPI startup.

**Decision:** Centralize model initialization and access.

**Reason:** ML models are expensive to initialize and should not be recreated for every request.

**Benefit:**

- avoids repeated model loading
- provides a single model lifecycle
- makes future model additions easier
- allows services to retrieve models by name

---

## 3. Dependency Injection

FastAPI dependency injection is used for services:

```python
get_disease_service()
```

and the dependency is cached using:

```python
@lru_cache
```

**Decision:** Reuse service instances rather than constructing them for every request.

This works particularly well because the service itself accesses already-loaded models.

---

## 4. Service Layer

Disease inference is not implemented directly inside the API route.

Instead:

```text
API Route
   ↓
DiseaseService
   ↓
Validator
   ↓
FileManager
   ↓
DiseaseModel
   ↓
DiseaseAgent
```

**Decision:** Introduce a service layer between HTTP endpoints and AI components.

**Benefit:** Business logic remains independent from FastAPI.

---

## 5. Separate Prediction from Reasoning

The project deliberately separates:

```text
DiseaseModel → What disease was detected?
DiseaseAgent → What does that prediction mean?
```

The YOLO model produces raw predictions.

The agent adds:

- severity
- crop information
- recommended action
- RAG requirement
- weather requirement

**Decision:** Do not embed agricultural decision logic directly into the computer-vision model.

This makes the system easier to extend to additional diseases and reasoning mechanisms.

---

## 6. RAG as a Separate Subsystem

The RAG implementation is isolated under:

```text
app/rag/
```

with separate components for:

- loading
- cleaning
- chunking
- embeddings
- vector storage
- retrieval

**Decision:** Treat knowledge retrieval as an independent subsystem rather than tightly coupling it to disease detection.

This is important because agricultural knowledge can evolve independently of the disease model.

---

## 7. Persistent Vector Storage

ChromaDB is configured as a persistent local vector store.

```text
knowledge_base/chroma/
```

**Decision:** Persist embeddings locally instead of recomputing them during application startup.

**Benefit:**

- faster application startup
- reusable knowledge index
- offline/local development
- simple deployment architecture

---

## 8. Offline Knowledge-Building Pipeline

Knowledge ingestion is separated from runtime retrieval.

The project uses:

```text
build_vector_db.py
```

to:

1. load documents
2. clean them
3. chunk them
4. generate embeddings
5. rebuild the vector database

**Decision:** Perform expensive preprocessing offline rather than during API requests.

This keeps runtime inference focused on serving users.

---

## 9. Temporary File Lifecycle

Uploaded images are stored using UUID-generated temporary filenames.

After inference:

```python
finally:
    FileManager.delete(path)
```

**Decision:** Treat uploaded images as temporary inference artifacts.

**Benefit:**

- avoids filename collisions
- reduces unnecessary disk usage
- limits persistence of user-uploaded images

---

## 10. Configuration Through Environment Variables

Runtime configuration is represented through a Pydantic settings class.

Important settings include:

```text
PROJECT_NAME
PROJECT_VERSION
DEBUG
HOST
PORT
DISEASE_MODEL_PATH
EMBEDDING_MODEL
WHISPER_MODEL
LLM_MODEL
```

**Decision:** Keep environment-dependent configuration outside application code.

This prepares the system for different development, testing, and production environments.

---

## 11. Domain Knowledge Outside the ML Model

Disease metadata currently lives in:

```text
app/core/constants.py
```

rather than inside the YOLO implementation.

**Decision:** Keep domain rules separate from model inference.

This allows disease-specific actions and severity rules to evolve without changing the inference implementation.

---

# 🔄 Disease Detection Flow

A disease-detection request follows this sequence:

```text
User uploads image
        │
        ▼
FastAPI /disease/predict
        │
        ▼
ImageValidator
        │
        ├── Extension check
        └── Size check
        │
        ▼
FileManager
        │
        ▼
DiseaseService
        │
        ▼
DiseaseModel
        │
        ▼
YOLO inference
        │
        ▼
Disease prediction
        │
        ▼
DiseaseAgent
        │
        ▼
Agricultural analysis
        │
        ▼
Response
        │
        ▼
Temporary image deleted
```

---

# 🔎 RAG Flow

Knowledge ingestion:

```text
Agricultural PDF
      │
      ▼
DocumentLoader
      │
      ▼
TextCleaner
      │
      ▼
TextChunker
      │
      ▼
SentenceTransformer
      │
      ▼
Embeddings
      │
      ▼
ChromaDB
```

Query retrieval:

```text
User Query
    │
    ▼
Embedding Model
    │
    ▼
Query Vector
    │
    ▼
ChromaDB
    │
    ▼
Top-K Relevant Chunks
```

---

# 🌐 API Endpoints

## Root

```http
GET /
```

Returns a welcome message.

---

## Health Check

```http
GET /health
```

Example:

```json
{
  "status": "healthy",
  "service": "AgriSahayak AI",
  "version": "1.0.0"
}
```

---

## Disease Service Status

```http
GET /disease/status
```

Returns model/service availability information.

---

## Disease Prediction

```http
POST /disease/predict
```

### Request

Multipart form-data:

```text
file = plant_image.jpg
```

### Response

The current service returns structured disease analysis containing:

```text
crop
disease
confidence
severity
recommended_action
needs_weather
needs_rag
```

---

# 🛠️ Technology Stack

### Backend

- Python
- FastAPI
- Uvicorn
- Pydantic

### Computer Vision

- Ultralytics YOLO
- PyTorch
- TorchVision
- OpenCV

### RAG

- Sentence Transformers
- ChromaDB
- PyMuPDF

### Knowledge Engineering

- Requests
- BeautifulSoup
- lxml
- Markdownify
- Trafilatura
- TQDM

### Engineering

- Loguru
- Environment-based configuration
- FastAPI dependency injection
- Modular service architecture

---

# ⚙️ Setup

## 1. Clone the repository

```bash
git clone <your-repository-url>
cd Agrisahayak-ai
```

---

## 2. Create a virtual environment

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

For the backend-specific environment:

```bash
cd backend
pip install -r requirements.txt
```

---

## 4. Configure environment variables

Create:

```text
backend/.env
```

with values corresponding to the settings required by the application.

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
LLM_MODEL=<your-llm-model>
```

> The disease model file is not included in the repository. A trained YOLO model must be supplied separately at the configured path.

---

# ▶️ Running the Backend

From the `backend` directory:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 🧠 Building the Vector Database

The repository already contains a processed agricultural knowledge base and ChromaDB artifacts.

To rebuild the vector database:

```bash
cd backend
python build_vector_db.py
```

The pipeline will:

1. Load agricultural PDFs.
2. Extract text.
3. Clean the text.
4. Create overlapping chunks.
5. Generate embeddings.
6. Reset the ChromaDB collection.
7. Store the new vectors.

---

# 🧪 Testing Retrieval

The repository contains a simple retrieval test:

```bash
python test_retriever.py
```

The test performs semantic retrieval for a query such as:

```text
Tomato leaf curl disease
```

and prints the retrieved knowledge chunk.

---

# 📊 Current Project State

The repository currently represents a **working backend foundation and RAG prototype**, rather than a fully completed end-to-end agricultural assistant.


### Planned / Extensible

- [ ] Fully trained production disease model
- [ ] LLM-based agricultural response generation
- [ ] Retrieval integrated directly into disease responses
- [ ] Weather-aware recommendations
- [ ] Voice interaction
- [ ] Multi-crop disease coverage
- [ ] More comprehensive disease knowledge
- [ ] Frontend/mobile client
- [ ] Production deployment
- [ ] Automated evaluation of RAG retrieval quality

---

# 🔮 Future Architecture

The intended evolution of AgriSahayak is toward a multimodal agricultural AI assistant:

```text
                    ┌─────────────────────┐
                    │      User           │
                    └──────────┬──────────┘
                               │
                  ┌────────────▼────────────┐
                  │     AgriSahayak AI      │
                  │      Orchestrator       │
                  └────────────┬────────────┘
                               │
       ┌───────────────────────┼────────────────────────┐
       │                       │                        │
       ▼                       ▼                        ▼
┌──────────────┐       ┌──────────────┐        ┌──────────────┐
│ Computer     │       │ Agricultural │        │   Weather    │
│ Vision       │       │ RAG          │        │   Service    │
│ YOLO         │       │ ChromaDB     │        │              │
└──────────────┘       └──────────────┘        └──────────────┘
       │                       │                        │
       └───────────────────────┼────────────────────────┘
                               ▼
                     ┌──────────────────┐
                     │       LLM        │
                     │ Reasoning Layer  │
                     └────────┬─────────┘
                              ▼
                     ┌──────────────────┐
                     │ Farmer-Friendly  │
                     │ Recommendation   │
                     └──────────────────┘
```

The long-term objective is to move from **disease classification** toward **context-aware agricultural decision support**.

---

# 🎯 Design Philosophy

AgriSahayak follows four major principles:

### 1. Modular AI

Computer vision, retrieval, embeddings, and reasoning are independent components.

### 2. Domain Grounding

Agricultural recommendations should be grounded in agricultural reference material rather than relying entirely on general-purpose model knowledge.

### 3. Separation of Concerns

API handling, business logic, model inference, knowledge retrieval, and data processing remain separate.

### 4. Extensibility

The architecture is designed to accommodate additional AI capabilities without replacing the existing backend foundation.

---

# 👩‍💻 Project Development

The repository was developed incrementally, with the architecture evolving through several stages:

```text
Health API
    ↓
Disease Detection API
    ↓
Validation & Exception Handling
    ↓
Model Registry
    ↓
Disease Agent
    ↓
RAG Folder Structure
    ↓
PDF Document Loader
    ↓
Text Cleaning
    ↓
Chunking
    ↓
RAG Pipeline
    ↓
Agricultural Knowledge ETL
    ↓
Embedding Service
    ↓
ChromaDB
    ↓
Semantic Retrieval
```

This progression reflects the project's transition from a simple disease-detection backend into a broader **agricultural AI reasoning platform**.


---

# 🌱 AgriSahayak AI

**From identifying a crop disease to helping farmers understand what to do next.**

---

# 📜 License

Add the project's chosen license here.


