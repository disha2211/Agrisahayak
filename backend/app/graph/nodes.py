import inspect
import json

from langchain_core.messages import SystemMessage, ToolMessage
from app.core.prompts import FARMER_AGENT_SYSTEM_PROMPT

from app.core.services import service_registry
from app.core.tools import tool_registry

def llm_node(state):
    llm_service = service_registry.get("llm")
    model = llm_service.get_model()

    tools = [
        tool.schema()
        for tool in tool_registry.list_tools()
    ]

    model_with_tools = model.bind_tools(tools)

    messages = [
        SystemMessage(content=FARMER_AGENT_SYSTEM_PROMPT),
        *state["messages"],
    ]

    response = model_with_tools.invoke(messages)

    return {
        "messages": [response]
    }

async def tool_node(state):
    last_message = state["messages"][-1]

    tool_calls = last_message.tool_calls or []

    tool_messages = []

    for tool_call in tool_calls:

        tool_name = tool_call["name"]
        arguments = tool_call["args"]
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

    if last_message.tool_calls:
        return "tools"

    return "end"