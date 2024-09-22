import streamlit as st
from view.abstract_view import AbstractView

class ApiKeyView(AbstractView):
    def __init__(self) -> None:
        self._api_key = st.secrets.get("OPEN_AI_API_KEY")

    def show(self) -> None:
        if not self._api_key:
            if "api_key_set" not in st.session_state:
                st.session_state["api_key_set"] = False

            if not st.session_state["api_key_set"]:
                st.warning("Please add your OpenAI API key to the Streamlit secrets.toml file or add below.")
                self._api_key = st.text_input("OpenAI API Key (press enter to confirm)", type="password")
                st.markdown("---")
                st.write("You can create an OpenAI account and get an API key here: https://platform.openai.com/signup")

                if self._api_key:
                    st.session_state["api_key_set"] = True
                    st.session_state["api_key"] = self._api_key
                    st.rerun()
                else:
                    st.stop()
            else:
                self._api_key = st.session_state["api_key"]
        else:
            st.session_state["api_key_set"] = True
            st.session_state["api_key"] = self._api_key