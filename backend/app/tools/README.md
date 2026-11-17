
# Tool Architecture

Tools are the interface between the LLM and deterministic application capabilities.

## Base Contract

Tools inherit from BaseTool and provide:
- a tool name
- a description
- an LLM-facing schema
- a run() implementation

## Current Tools

| Tool | Backend capability |
|---|---|
| disease_detection | YOLO disease inference |
| knowledge_retrieval | ChromaDB semantic retrieval |
| weather | Open-Meteo forecast |
| market_price | Development market dataset lookup |

## Execution Pattern

    LLM
      ↓
    Tool schema
      ↓
    Tool call
      ↓
    ToolRegistry
      ↓
    Tool.run()
      ↓
    Service / Retriever
      ↓
    Structured result
      ↓
    LLM

The LLM never directly calls the underlying service or database.

## Service vs Tool

Services contain the actual application logic.

Examples:
- DiseaseService
- WeatherService
- MarketService

Tools adapt those capabilities for LLM use.

    WeatherService
          ↑
      WeatherTool
          ↑
          LLM

This keeps the application logic independent from the LLM interface.

## Tool Registry

ToolRegistry stores tools by name. During application startup, the backend registers the available tools. The agent then discovers their schemas dynamically.

Adding a tool therefore does not require tool-specific logic inside the agent loop.

## Design Principle

Services do the work; tools expose the work to the agent.
