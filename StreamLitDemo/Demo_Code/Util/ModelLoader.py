import streamlit as st
from langchain.callbacks.manager import CallbackManager
from langchain_community.llms import LlamaCpp


@st.cache_resource
def load_llm_model():
    callback_manager = CallbackManager(handlers=[])
    llm = LlamaCpp(
        model_path="../Assets/models/Phi-3.5-mini-instruct-Q4_K_S.gguf",
        callback_manager=callback_manager,
        n_ctx=8192,
        verbose=False,
        max_tokens=4096,
    )
    return llm


class ModelLoader:

    @staticmethod
    def cache_and_load_llm_model():
        return load_llm_model()
