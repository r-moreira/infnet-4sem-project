from fastapi import FastAPI
import logging
from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject
from controller.openai_controller import OpenAiController
from service.openai_client_service import OpenAIClientService

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    
    openai_client_service = providers.Singleton(OpenAIClientService)

    openai_controller = providers.Singleton(
        OpenAiController,
        openai_client_service=openai_client_service
    )
    

@inject
def include_routers(openai_controller: OpenAiController = Provide[Container.openai_controller]) -> None:
    app.include_router(openai_controller.router)  

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

app = FastAPI()
container = Container()
container.wire(modules=[__name__])
include_routers()