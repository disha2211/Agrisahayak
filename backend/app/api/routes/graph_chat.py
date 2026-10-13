
from fastapi import APIRouter, Depends, File, Form, UploadFile

from app.agents.farmer_graph_agent import FarmerGraphAgent
from app.api.dependencies import get_farmer_graph_agent
from app.schemas.chat import ChatRequest, ChatResponse
from app.utils.file_manager import FileManager
from app.utils.validators import ImageValidator

router = APIRouter(
    prefix="/graph-chat",
    tags=["AI Assistant - LangGraph"],
)


# Existing JSON endpoint — preserve text-only chat.
@router.post("", response_model=ChatResponse)
async def graph_chat(
    request: ChatRequest,
    agent: FarmerGraphAgent = Depends(get_farmer_graph_agent),
):
    response = await agent.run(request.message)
    return ChatResponse(response=response)


# New multipart endpoint — message + optional plant image.
@router.post("/with-image", response_model=ChatResponse)
async def graph_chat_with_image(
    message: str = Form(...),
    image: UploadFile | None = File(default=None),
    agent: FarmerGraphAgent = Depends(get_farmer_graph_agent),
):
    image_path = None

    try:
        if image is not None:
            extension = await ImageValidator.validate(image)

            image_path = FileManager.save_upload(
                image,
                extension,
            )

        response = await agent.run(
            message,
            image_path=str(image_path) if image_path else None,
        )

        return ChatResponse(response=response)

    finally:
        if image_path is not None:
            FileManager.delete(image_path)
