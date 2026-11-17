
# Agent Architecture

AgriSahayak separates agent reasoning from deterministic capabilities exposed as tools.

## Farmer Agent

The Farmer Agent is the LLM-facing orchestration layer.

Responsibilities:
1. Receive the farmer's request.
2. Expose registered tool schemas.
3. Let the LLM decide which tools are required.
4. Execute selected tools through ToolRegistry.
5. Return tool results to the LLM.
6. Repeat until the LLM produces a final response.

    User
      ↓
    FarmerAgent
      ↓
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
      ↓
    Final Answer

The sequence is not hard-coded; the model can select multiple tools when required.

## LangGraph Agent

FarmerGraphAgent represents the same agentic pattern explicitly as a graph.

    LLM
     ↓
    Tool calls?
     ├── No → END
     └── Yes
           ↓
        Tool Node
           ↓
          LLM

The graph contains:
- llm_node — invokes the LLM with available tools.
- tool_node — executes requested tools and creates tool messages.
- route_after_llm — decides whether to continue or finish.
- AgentState — carries messages and the optional image path.

## Image-Aware Execution

For graph-chat/with-image:

1. The API validates and temporarily stores the image.
2. The image path is placed in agent state.
3. Disease detection becomes available to the LLM.
4. The tool node injects the trusted backend image path.
5. Disease inference runs.
6. The result is returned to the LLM.
7. The temporary file is deleted.

The model is never trusted to choose an arbitrary filesystem path.

## Grounding

The agent prompt defines rules for:
- using tools when appropriate
- treating tool outputs as evidence
- avoiding unsupported agricultural recommendations
- distinguishing development market data from live data
- avoiding invented treatment doses or schedules

## Extending the Agent

To add a capability:
1. Implement the functionality as a service.
2. Create a BaseTool implementation.
3. Define its LLM-facing schema.
4. Register the service and tool during startup.
5. Update the prompt only when routing or grounding behavior needs explicit guidance.

The core agent loop does not need to be rewritten.
