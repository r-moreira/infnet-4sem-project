import streamlit as st
from service.openai_client_service import OpenAIClientService
from view.abstract_view import AbstractView
from abc import abstractmethod, ABC

class ChatCallbackProvider(ABC):
    
    @abstractmethod
    def on_chat_submit(self, prompt: str) -> None:
        pass

class ChatView(AbstractView):
    def __init__(self, open_ai_client_service: OpenAIClientService) -> None:
        self.open_ai_client_service = open_ai_client_service
        self.__initialize_session_state()

    def __initialize_session_state(self) -> None:
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

    def show(self, on_chat_submit: callable) -> None:
        self.open_ai_client_service.setup_open_ai_client()   
        
        st.title("💬 Chatbot")
        for message in st.session_state.messages:
            st.chat_message(message["role"]).write(message["content"])

        if prompt := st.chat_input():
            on_chat_submit(prompt)


    class Callbacks(ChatCallbackProvider):
        def __init__(self, chat_view: 'ChatView') -> None:
            self._chat_view = chat_view
            
        @st.cache_data(show_spinner=False)
        def on_chat_submit(_self, prompt: str) -> None:
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            
            message: str = _self._chat_view.open_ai_client_service.get_backend_chat_response(st.session_state.messages)
            
            st.session_state.messages.append({"role": "assistant", "content": message})
            st.chat_message("assistant").write(message)