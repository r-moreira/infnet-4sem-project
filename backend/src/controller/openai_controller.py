from fastapi import APIRouter, HTTPException
from service.openai_client_service import OpenAIClientService
from model.chat_request import ChatRequest
from model.chat_response import ChatResponse

class OpenAiController: 
    def __init__(self, openai_client_service: OpenAIClientService) -> None:
        self._openai_client_service = openai_client_service
        self.router = APIRouter()
        self.router.add_api_route("/hello", self.read_root, methods=["GET"])
        self.router.add_api_route("/chat", self.get_chat_response, methods=["POST"])

    def read_root(self):
        return {"Hello": "World"}
    
    def get_chat_response(self, request: ChatRequest) -> ChatResponse:
        try:
            response = self._openai_client_service.get_chat_response(request.messages, request.api_key)
            return {"message": response}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))