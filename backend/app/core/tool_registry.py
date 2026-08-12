from app.tools.base import BaseTool


class ToolRegistry:

    def __init__(self):

        self.tools: dict[str, BaseTool] = {}

    def register(
        self,
        tool: BaseTool,
    ):

        self.tools[tool.name] = tool

    def get(
        self,
        name: str,
    ):

        if name not in self.tools:

            raise ValueError(
                f"Tool '{name}' not found."
            )

        return self.tools[name]

    def list_tools(self):

        return list(
            self.tools.values()
        )