import json
import inspect

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

    async def _execute_tool(
        self,
        tool_name: str,
        arguments: dict,
    ):

        tool = tool_registry.get(
            tool_name
        )

        result = tool.run(
            **arguments
        )

        if inspect.isawaitable(result):

            result = await result

        return result

    async def run(
    self,
    user_message: str,
):

        messages = [
            {
                "role": "system",
                "content": (
                    "You are AgriSahayak, an agricultural "
                    "AI assistant.\n\n"

                    "Your job is to answer farmer questions "
                    "using the available tools whenever "
                    "appropriate.\n\n"

                    "IMPORTANT RULES:\n"
                    "1. Use knowledge_retrieval for agricultural "
                    "knowledge, crop diseases, treatment, and "
                    "crop management.\n"
                    "2. Use weather when weather information "
                    "is requested or relevant.\n"
                    "3. Use market_price when market prices "
                    "are requested.\n"
                    "4. If the user asks multiple questions, "
                    "answer ALL parts of the question.\n"
                    "5. If multiple tools are required, use "
                    "all relevant tools before producing "
                    "the final answer.\n"
                    "6. Do not ask the user whether they want "
                    "information that they already requested.\n"
                    "7. Do not invent agricultural treatment "
                    "recommendations.\n"
                    "8. Use retrieved agricultural knowledge "
                    "as the basis for treatment recommendations.\n"
                    "9. After receiving tool results, synthesize "
                    "ALL relevant results into one complete answer.\n"
                    "10. Before producing the final answer, inspect "
                    "all tool results and address every requested "
                    "sub-question."
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

            print("\n========== LLM RESPONSE ==========")
            print(response)
            print("==================================\n")

            message = response["message"]

            tool_calls = message.get(
                "tool_calls"
            )

            # --------------------------------
            # No more tools -> final answer
            # --------------------------------

            if not tool_calls:

                print(
                    "\n[AGENT] No more tool calls."
                )

                print(
                    "[AGENT] Final answer:"
                )

                print(
                    message["content"]
                )

                return message["content"]

            # --------------------------------
            # Preserve assistant tool request
            # --------------------------------

            messages.append(message)

            # --------------------------------
            # Execute every requested tool
            # --------------------------------

            for tool_call in tool_calls:

                function = tool_call["function"]

                tool_name = function["name"]

                arguments = function.get(
                    "arguments",
                    {},
                )

                print(
                    f"\n[AGENT] Calling tool: {tool_name}"
                )

                print(
                    f"[AGENT] Arguments: {arguments}"
                )

                result = await self._execute_tool(
                    tool_name,
                    arguments,
                )

                print(
                    f"[AGENT] Tool result: {result}"
                )


                print("\n========== MESSAGES SENT TO FINAL LLM ==========")

                for i, msg in enumerate(messages):

                    print(
                        f"\n--- MESSAGE {i} ---"
                    )

                    print(
                        f"ROLE: {msg.get('role')}"
                    )

                    print(
                        str(msg.get("content", ""))[:2000]
                    )

                print(
                    "\n================================================="
                )

                # --------------------------------
                # Send tool result back to LLM
                # --------------------------------

                messages.append(
                    {
                        "role": "tool",
                        "content": json.dumps(
                            result,
                            ensure_ascii=False,
                        ),
                    }
                )