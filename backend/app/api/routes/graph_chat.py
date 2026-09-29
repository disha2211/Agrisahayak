from fastapi import (
    APIRouter,
    Depends,
)

from app.agents.farmer_graph_agent import (
    FarmerGraphAgent,
)

from app.api.dependencies import (
    get_farmer_graph_agent,
)

from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
)


router = APIRouter(
    prefix="/graph-chat",
    tags=["AI Assistant - LangGraph"],
)


@router.post(
    "",
    response_model=ChatResponse,
)
async def graph_chat(
    request: ChatRequest,
    agent: FarmerGraphAgent = Depends(
        get_farmer_graph_agent
    ),
):

    response = await agent.run(
        request.message
    )

    return ChatResponse(
        response=response
    )