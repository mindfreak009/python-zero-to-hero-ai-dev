
from pathlib import Path

from pinecone import Pinecone, ServerlessSpec
from langchain_ollama import OllamaEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from config import (
    OLLAMA_EMBEDDING_MODEL,
    PINECONE_API_KEY,
    PINECONE_INDEX_NAME,
    PINECONE_NAMESPACE,
)


def create_index():
    pc = Pinecone(api_key=PINECONE_API_KEY)

    indexes = pc.list_indexes().names()

    if PINECONE_INDEX_NAME not in indexes:
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=768,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1",
            ),
        )
        print("Pinecone index created")
    else:
        print("Pinecone index already exists")


def load_documents():
    documents = []
    folder = Path("documents")

    if not folder.exists():
        raise FileNotFoundError(
            f"Documents folder not found: {folder.resolve()}"
        )

    for file in folder.glob("*.txt"):
        text = file.read_text(encoding="utf-8")

        documents.append(
            Document(
                page_content=text,
                metadata={"source": file.name},
            )
        )

    print(f"Documents loaded: {len(documents)}")
    return documents


def get_vector_store():
    embeddings = OllamaEmbeddings(
        model=OLLAMA_EMBEDDING_MODEL
    )

    vector_store = PineconeVectorStore(
        index_name=PINECONE_INDEX_NAME,
        embedding=embeddings,
        namespace=PINECONE_NAMESPACE,
    )

    return vector_store


def ingest_documents():
    documents = load_documents()

    if not documents:
        print("No text documents found. Nothing to ingest.")
        return

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
    )

    chunks = splitter.split_documents(documents)

    print(f"Chunks created: {len(chunks)}")

    create_index()

    vector_store = get_vector_store()
    vector_store.add_documents(chunks)

    print(f"Successfully added {len(chunks)} chunks to Pinecone.")


def retrieve_documents(question):
    vector_store = get_vector_store()

    retriever = vector_store.as_retriever(
        search_kwargs={"k": 4}
    )

    documents = retriever.invoke(question)

    return documents


if __name__ == "__main__":
    ingest_documents()
