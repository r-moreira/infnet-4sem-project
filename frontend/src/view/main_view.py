from typing import List
from enums.view_strategy import ViewStrategy
from view.abstract_view import AbstractView
from utils.streamlit_utils import StreamlitUtils
from view.abstract_view import AbstractView
from view.abstract_strategy_view import AbstractStrategyView
import streamlit as st
import logging

class MainView(AbstractView):
    logger = logging.getLogger(__name__)
    
    def __init__(
        self, 
        sidebar_view: AbstractView,
        strategy_view_list: List[AbstractStrategyView]
        ) -> None:
        
        self._sidebar_view = sidebar_view
        self._strategy_view_list = strategy_view_list
        
    def show(self) -> None:        
        try:
            self.do_show()
        except Exception as e:
            MainView.logger.error(f"Error rendering View: {e}")
            self.global_error_dialog()
       
    def do_show(self) -> None:
        StreamlitUtils.setup_page_config()
        
        # Strategy pattern
        strategy: ViewStrategy = self._sidebar_view.show()
        
        for strategy_view in self._strategy_view_list:
            if strategy_view.accept(strategy):
                strategy_view.show()
                break
       
    @st.dialog("Error")
    def global_error_dialog(self) -> None:
        st.error(f"Something went wrong :(")