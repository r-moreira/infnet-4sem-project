import logging
import nltk
from service.http_client_service import HttpClientService
from service.session_state_service import SessionStateService
from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject
from view.sidebar_view import SidebarView
from view.chat_view import ChatView
from view.main_view import MainView
from view.album_analysis_view import AlbumAnalysisView
from view.song_analysis_view import SongAnalysisView
from view.playlist_view import PlaylistView

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    session_state_service = providers.Singleton(SessionStateService)

    http_client_service = providers.Singleton(HttpClientService)
    
    sidebar_view = providers.Singleton(
        SidebarView,
        session_state_service=session_state_service)
    
    album_analysis_view = providers.Singleton(AlbumAnalysisView)
    
    song_analysis_view = providers.Singleton(
            SongAnalysisView,
            http_client_service=http_client_service
        )
    
    chat_view = providers.Singleton(
        ChatView,
        session_state_service=session_state_service,
        http_client_service=http_client_service
    )

    playlist_view = providers.Singleton(
        PlaylistView,
        session_state_service=session_state_service,
        http_client_service=http_client_service
    )

    main_view = providers.Singleton(
        MainView,
        sidebar_view=sidebar_view,
        strategy_view_list=providers.List(
            album_analysis_view,
            chat_view,
            song_analysis_view,
            playlist_view
        )
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