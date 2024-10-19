import logging
import nltk
from service.openai_client_service import OpenAIClientService
from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject
from view.sidebar_view import SidebarView
from view.chat_view import ChatView
from view.main_view import MainView
from view.api_key_view import ApiKeyView
from view.album_analysis_view import AlbumAnalysisView


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    open_ai_client_service = providers.Singleton(OpenAIClientService)
    
    sidebar_view = providers.Singleton(SidebarView)
    
    album_analysis_view = providers.Singleton(AlbumAnalysisView)
    
    api_key_view = providers.Singleton(ApiKeyView)
    
    chat_view = providers.Singleton(
        ChatView,
        open_ai_client_service=open_ai_client_service
    )
    
    chat_view_callbacks = providers.Singleton(
        ChatView.Callbacks,
        chat_view=chat_view
    )

    main_view = providers.Singleton(
        MainView,
        sidebar_view=sidebar_view,
        album_analysis_view=album_analysis_view,
        api_key_view=api_key_view,
        chat_view=chat_view,
        chat_view_callbacks=chat_view_callbacks
    )

@inject
def main(main_view: MainView = Provide[Container.main_view]) -> None:
    main_view.show()    

if __name__ == "__main__":
    container = Container()
    container.wire(modules=[__name__])
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("app.log"),
            logging.StreamHandler()
        ]
    )
    
    nltk.download('punkt_tab')
    nltk.download('stopwords')
    
    main() 