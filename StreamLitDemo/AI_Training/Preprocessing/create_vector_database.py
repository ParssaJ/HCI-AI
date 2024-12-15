import chromadb
from langchain_community.document_loaders import JSONLoader

if __name__ == '__main__':
    chroma_client = chromadb.PersistentClient(
        path="./chroma_db"
    )

    collection = chroma_client.create_collection(name="train_questions_and_queries")

    file_path = "../../Assets/datasets/spider_data/train_spider.json"
    loader = JSONLoader(
        file_path=file_path,
        jq_schema='.[] | {db_id: .db_id, question: .question, query: .query}',
        text_content=False)

    data = loader.load()
    documents = [document.page_content for document in data]
    ids = list(map(str, list(range(len(documents)))))

    collection.add(
        documents=documents,
        ids=ids
    )
