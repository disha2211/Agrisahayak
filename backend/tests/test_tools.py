from app.core.tools import tool_registry


for tool in tool_registry.list_tools():

    print(
        f"{tool.name}: "
        f"{tool.description}"
    )