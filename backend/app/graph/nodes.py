import inspect
import json
import uuid

from langchain_core.messages import AIMessage, ToolMessage

from app.core.services import service_registry
from app.core.tools import tool_registry


def _to_ollama_message(message):
    """Convert LangChain graph messages to Ollama message dictionaries."""
    if isinstance(message, dict):
        return message

    message_type = getattr(message, "type", "")
    role = {
        "human": "user",
        "ai": "assistant",
        "tool": "tool",
        "system": "system",
    }.get(message_type, "assistant")

    converted = {
        "role": role,
        "content": getattr(message, "content", ""),
    }

    if role == "assistant" and getattr(message, "tool_calls", None):
        converted["tool_calls"] = [
            {
                "function": {
                    "name": tool_call["name"],
                    "arguments": tool_call.get("args", {}),
                }
            }
            for tool_call in message.tool_calls
        ]

    if role == "tool" and getattr(message, "name", None):
        converted["name"] = message.name

    return converted


def llm_node(state):
    llm = service_registry.get("llm")

    tools = [
        tool.schema()
        for tool in tool_registry.list_tools()
    ]

    response = llm.chat(
        messages=state["messages"],
        tools=tools,
    )

    ollama_message = response.get("message") or {}

    tool_calls = ollama_message.get("tool_calls") or []

    return {
        "messages": [
            {
                "role": "assistant",
                "content": ollama_message.get("content") or "",
                "tool_calls": tool_calls,
            }
        ]
    }


async def tool_node(state):
    last_message = state["messages"][-1]
    tool_calls = last_message.get("tool_calls") or []

    tool_messages = []

    for tool_call in last_message.tool_calls:
        tool_name = tool_call["name"]
        arguments = tool_call.get("args", {})
        tool_call_id = tool_call["id"]

        tool = tool_registry.get(tool_name)

        result = tool.run(**arguments)

        if inspect.isawaitable(result):
            result = await result

        tool_messages.append(
            ToolMessage(
                content=json.dumps(result),
                name=tool_name,
                tool_call_id=tool_call_id,
            )
        )

    return {
        "messages": tool_messages
    }


def route_after_llm(state):
    last_message = state["messages"][-1]

    tool_calls = last_message.get("tool_calls") or []

    if tool_calls:
        return "tools"

    return "end"