
# LangGraph Workflow

The graph package contains the explicit state-machine implementation of the AgriSahayak agent.

## Workflow

    START
      ↓
    LLM Node
      ↓
    Tool calls?
     ├── Yes → Tool Node → LLM Node
     └── No  → END

## State

AgentState contains:
- messages — conversation and tool messages
- image_path — optional trusted path to the uploaded plant image

The message list uses LangGraph's message reducer so new messages are appended to the existing conversation state.

## LLM Node

The LLM node:
1. Gets the configured LLM service.
2. Reads registered tools.
3. Removes disease detection when no image is present.
4. Binds the remaining tool schemas to the model.
5. Invokes the model with the system prompt and current messages.

## Tool Node

The tool node:
1. Reads tool calls from the latest LLM message.
2. Resolves each tool through ToolRegistry.
3. Injects the trusted image path for disease detection.
4. Executes synchronous or asynchronous tools.
5. Converts results into ToolMessage objects.
6. Returns them to the graph.

## Why LangGraph?

The graph makes the agent loop explicit instead of hiding it inside one function. This provides a clear place for state, conditional routing, validation, retries, and future workflow nodes.

The current workflow intentionally remains small: LLM → tools → LLM.
