from fastapi import FastAPI
import logging
from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject
from controller.openai_controller import OpenAiController
from controller.genius_controller import GeniusController
from controller.spotify_controller import SpotifyController
from service.spotify_client_service import SpotifyClientService
from service.openai_client_service import OpenAIClientService
from service.genius_client_service import GeniusClientService
from service.local_llm_service import LocalLLMService

import os

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    openai_controller = providers.Singleton(
        OpenAiController,
        config=config,
        openai_client_service=providers.Singleton(
            OpenAIClientService,
            config=config
        ),
        local_llm_service=providers.Singleton(
            LocalLLMService,
            config=config
        )
    )
    
    genius_controller = providers.Singleton(
        GeniusController,
        genius_client_service=providers.Singleton(
            GeniusClientService,
            config=config
        )
    )
    
    spotify_controller = providers.Singleton(
        SpotifyController,
            spotify_client_service=providers.Singleton(
            SpotifyClientService,
            config=config
        )
    )
    

@inject
def include_routers(
        openai_controller: OpenAiController = Provide[Container.openai_controller],
        genius_controller: GeniusController = Provide[Container.genius_controller],
        spotify_controller: SpotifyController = Provide[Container.spotify_controller],
    ) -> None:
    
    app.include_router(openai_controller.router)  
    app.include_router(genius_controller.router)
    app.include_router(spotify_controller.router)
    
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
container.config.from_yaml(os.path.join(os.path.dirname(__file__), '../config.yml'))
container.wire(modules=[__name__])
 
include_routers()