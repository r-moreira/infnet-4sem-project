from view.abstract_view import AbstractView
from utils.streamlit_utils import StreamlitUtils
from view.api_key_view import ApiKeyView
from view.chat_view import ChatCallbackProvider

class MainView(AbstractView):
    def __init__(
        self, 
        sidebar_view: AbstractView,
        album_analysis_view: AbstractView,
        api_key_view: AbstractView,
        chat_view: AbstractView,
        chat_view_callbacks: ChatCallbackProvider,
        ) -> None:
        
        self._sidebar_view = sidebar_view
        self._album_analysis_view = album_analysis_view
        self._chat_view = chat_view
        self._chat_view_callbacks = chat_view_callbacks
        self._api_key_view = api_key_view
        
    def show(self) -> None:
        StreamlitUtils.setup_page_config()
        
        app_mode = self._sidebar_view.show()
        
        if app_mode == "Album Analisys":
            self._album_analysis_view.show()
        else:
            self._api_key_view.show()
            self._chat_view.show(self._chat_view_callbacks.on_chat_submit)