
from app.graph.workflow import build_graph


class FarmerGraphAgent:

    def __init__(self):
        self.graph = build_graph()

    async def run(
        self,
        message: str,
        image_path: str | None = None,
    ):
        state = {
            "messages": [
                {"role": "user", "content": message}
            ],
            "image_path": image_path,
        }

        result = await self.graph.ainvoke(state)

        final_message = result["messages"][-1]
        return final_message.content
