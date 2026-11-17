# 🌾 AgriSahayak 

AgriSahayak is an **agentic agricultural assistant** that combines LLM-based tool orchestration, agricultural RAG, crop-disease detection, weather data, market data, and voice interaction in a FastAPI backend.

The system is designed around one principle:

> **Let the LLM decide which specialized capability is required, while deterministic tools perform the actual work.**

## Core Capabilities

- 🌱 **Crop disease detection** using YOLO
- 🤖 **LLM-powered farmer assistant** with tool calling
- 📚 **RAG over agricultural knowledge** using Sentence Transformers + ChromaDB
- 🌦️ **Weather lookup and short-term forecast** using Open-Meteo
- 📈 **Market-price lookup** from a development dataset
- 🎙️ **Voice interaction** using SraVaani STT and Edge TTS
- 🖼️ **Image-aware conversational chat** through the LangGraph workflow
- 🧩 **Registry-based tool and service architecture**
- 🔐 **Evidence-grounded response rules** for agricultural recommendations

## Architecture

```text
                         Farmer
                           │
                           ▼
                      FastAPI API
                           │
             ┌─────────────┴─────────────┐
             │                           │
          /chat                  /graph-chat/with-image
             │                           │
             ▼                           ▼
       FarmerAgent                 FarmerGraphAgent
       tool loop                   LangGraph workflow
             │                           │
             └─────────────┬─────────────┘
                           ▼
                     LLM + Tools
                           │
       ┌───────────────────┼────────────────────┐
       │                   │                    │
       ▼                   ▼                    ▼
 Disease Detection    Knowledge RAG       Weather / Market
       │                   │                    │
      YOLO              ChromaDB          External / local data
       │                   │                    │
       └───────────────────┴────────────────────┘
                           │
                           ▼
                    Grounded Response
```

The LangGraph workflow additionally supports an optional plant image. When an image is present, the disease-detection tool is exposed to the LLM; the backend injects the trusted uploaded-image path rather than allowing the model to choose a filesystem path.

## Agentic Workflow

The current graph-based assistant follows:

```text
User message + optional image
          ↓
        LLM
          ↓
   Tool call required?
       ↙       ↘
     No         Yes
     ↓           ↓
  Response    Tool node
                  ↓
              Tool result
                  ↓
                 LLM
                  ↓
             Final response
```

The loop continues until the LLM produces a response without further tool calls.

Available tools:

| Tool | Purpose |
|---|---|
| `disease_detection` | Analyze the uploaded plant image |
| `knowledge_retrieval` | Retrieve agricultural evidence from the RAG knowledge base |
| `weather` | Retrieve location-based weather and forecast |
| `market_price` | Retrieve crop-market price data |

## RAG

The agricultural knowledge pipeline is deliberately separated from runtime inference:

```text
PDF
 ↓
Load
 ↓
Clean
 ↓
Chunk
 ↓
Embed
 ↓
ChromaDB
 ↓
Semantic Retrieval
```

Current knowledge source:

- `Agriculture-CPG-2020.pdf`

Current chunking configuration:

- Chunk size: **500 characters**
- Overlap: **100 characters**
- Embeddings: **Sentence Transformers**
- Vector store: **ChromaDB**
- Runtime retrieval default: **top 10**

Detailed methodology:

**[RAG Methodology →](backend/app/rag/README.md)**

## Voice Pipeline

Voice chat is implemented as:

```text
Audio
 ↓
FFmpeg normalization
 ↓
SraVaani STT
 ↓
Farmer Agent
 ↓
Answer
 ↓
Edge TTS
 ↓
MP3
```

Supported conversational languages currently include:

- English
- Telugu
- Hindi

## API

| Endpoint | Purpose |
|---|---|
| `POST /chat` | Text-based agentic assistant |
| `POST /graph-chat` | LangGraph text assistant |
| `POST /graph-chat/with-image` | Text + optional plant image |
| `POST /disease/predict` | Direct disease prediction |
| `POST /voice/chat` | Voice → agent → voice |
| `POST /voice/transcribe` | Speech-to-text |
| `POST /voice/synthesize` | Text-to-speech |
| `GET /health` | Backend health |
| `GET /disease/status` | Disease service status |

## Project Structure

```text
backend/
├── app/
│   ├── agents/       # Agent orchestration
│   ├── api/          # FastAPI routes
│   ├── core/         # Configuration, registries, prompts
│   ├── graph/        # LangGraph workflow and state
│   ├── models/       # ML inference models
│   ├── rag/          # Knowledge ingestion and retrieval
│   ├── services/     # LLM, disease, weather, market, speech, TTS
│   └── tools/        # LLM-callable capabilities
├── knowledge_base/
│   ├── raw/
│   ├── processed/
│   └── chroma/
├── data/
│   └── market_prices.csv
└── build_vector_db.py
```

Methodology documentation is kept close to the implementation:

- **[Agent architecture →](backend/app/agents/README.md)**
- **[LangGraph workflow →](backend/app/graph/README.md)**
- **[RAG methodology →](backend/app/rag/README.md)**
- **[Tool architecture →](backend/app/tools/README.md)**

## Design Decisions

### Tool-based orchestration
The LLM does not directly access models, databases, or APIs. It selects a registered tool; the tool executes deterministic application logic and returns structured results.

### Separate services from tools
Services implement the actual functionality. Tools provide the LLM-facing interface over those services.

### Persistent RAG index
Document processing and embedding happen offline. Runtime requests perform semantic retrieval against the existing ChromaDB collection.

### Grounded agricultural responses
The system prompt explicitly distinguishes tool evidence from model reasoning and instructs the assistant not to invent disease treatments, dosages, schedules, market claims, or weather information.

### Graph-based agent execution
LangGraph represents the LLM/tool loop explicitly as nodes and conditional edges, making image-aware execution and future workflow expansion easier to control.

## Setup

```bash
git clone https://github.com/disha2211/Agrisahayak.git
cd Agrisahayak

python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
```

For the backend:

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Create the required environment variables for the selected LLM provider, model, Hugging Face access, and other configured services.

The API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## Current Scope

Implemented:

- Disease inference
- Agentic tool calling
- LangGraph workflow
- Image-aware chat
- Agricultural RAG
- Weather tool
- Market-price tool
- Voice STT/TTS
- Evidence-grounded prompting

The market service currently uses a **development dataset**, not a live mandi-price feed.

## License

MIT
