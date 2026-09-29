from app.graph.workflow import build_graph


class FarmerGraphAgent:

    def __init__(self):

        self.graph = build_graph()

    async def run(
        self,
        message: str,
    ):

        state = {
            "messages": [
                {
                    "role": "user",
                    "content": message,
                }
            ]
        }

        result = await self.graph.ainvoke(
            state
        )

        final_message = (
            result["messages"][-1]
        )

        if isinstance(final_message, dict):
            return final_message["content"]

        return final_message.content