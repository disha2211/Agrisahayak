import json

from app.core.services import service_registry
from app.core.tools import tool_registry


class FarmerAgent:

    def __init__(self):

        self.llm = service_registry.get(
            "llm"
        )

    def _get_tool_schemas(self):

        return [
            tool.schema()
            for tool in tool_registry.list_tools()
        ]

    def _execute_tool(
        self,
        tool_name: str,
        arguments: dict,
    ):

        tool = tool_registry.get(
            tool_name
        )

        return tool.run(**arguments)

    def run(
    self,
    user_message: str,
):

        messages = [
            {
                "role": "system",
                "content": (
                    "You are AgriSahayak, an "
                    "agricultural AI assistant. "
                    "Use tools whenever reliable "
                    "external agricultural knowledge "
                    "is required. "
                    "Never invent treatment advice."
                ),
            },
            {
                "role": "user",
                "content": user_message,
            },
        ]

        tools = self._get_tool_schemas()

        while True:

            response = self.llm.chat(
                messages=messages,
                tools=tools,
            )

            message = response["message"]

            tool_calls = message.get(
                "tool_calls"
            )

            if not tool_calls:

                return message["content"]

            messages.append(message)

            for tool_call in tool_calls:

                function = tool_call["function"]

                tool_name = function["name"]

                arguments = function.get(
                    "arguments",
                    {},
                )

                result = self._execute_tool(
                    tool_name,
                    arguments,
                )

                messages.append(
                    {
                        "role": "tool",
                        "name": tool_name,
                        "content": json.dumps(
                            result
                        ),
                    }
                )