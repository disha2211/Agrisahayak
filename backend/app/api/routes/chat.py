from fastapi import APIRouter, Depends

from app.agents.farmer_agent import FarmerAgent
from app.api.dependencies import get_farmer_agent
from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
)


router = APIRouter(
    prefix="/chat",
    tags=["AI Assistant"],
)


@router.post(
    "",
    response_model=ChatResponse,
)
async def chat(
    request: ChatRequest,
    agent: FarmerAgent = Depends(
        get_farmer_agent
    ),
):

    response = agent.run(
        request.message
    )

    return ChatResponse(
        response=response
    )