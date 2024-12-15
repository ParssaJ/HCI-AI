FROM python:3.11.10-bookworm
COPY StreamLitDemo ./app
WORKDIR ./app
RUN pip install altair pandas streamlit langchain langchain-community llama-cpp-python jq chromadb
EXPOSE 8501
CMD [ "streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]