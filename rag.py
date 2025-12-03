from uuid import uuid4
from dotenv import load_dotenv
from pathlib import Path
from prompt import PROMPT, EXAMPLE_PROMPT
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chains.qa_with_sources.loading import load_qa_with_sources_chain
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_huggingface.embeddings import HuggingFaceEmbeddings

load_dotenv()

CHUNK_SIZE = 1000
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
VECTORSTORE_DIR = Path(__file__).parent / "resources/vectorstore"
COLLECTION_NAME = "real_estate"

llm = None
vector_store = None


def initialize_components():
    global llm, vector_store

    if llm is None:
        llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.9, max_tokens=500)

    if vector_store is None:
        ef = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={"trust_remote_code": True}
        )

        vector_store = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=ef,
            persist_directory=str(VECTORSTORE_DIR)
        )


def process_urls(urls, vector_store=None):
    """
    This function scraps data from a url and stores it in a vector db
    :param urls: input urls
    :param vector_store: existing vector store or None
    :return: yields status messages
    """
    yield "Initializing Components"
    
    # Initialize LLM
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.9, max_tokens=500)
    
    # Initialize embeddings
    ef = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"trust_remote_code": True}
    )

    yield "Resetting vector store..."
    # Delete old collection if it exists
    if vector_store is not None:
        try:
            vector_store.delete_collection()
        except:
            pass
    
    # Create new vector store
    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=ef,
        persist_directory=str(VECTORSTORE_DIR)
    )

    yield "Loading data..."
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    loader = WebBaseLoader(web_paths=urls, header_template=headers)
    data = loader.load()

    yield "Splitting text into chunks..."
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ".", " "],
        chunk_size=CHUNK_SIZE
    )
    docs = text_splitter.split_documents(data)

    yield "Add chunks to vector database..."
    uuids = [str(uuid4()) for _ in range(len(docs))]
    vector_store.add_documents(docs, ids=uuids)

    yield "Done adding docs to vector database..."
    
    # Yield the vector store so it can be stored in session state
    yield vector_store

def generate_answer(query, vector_store):
    if not vector_store:
        raise RuntimeError("Vector database is not initialized ")
    
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.9, max_tokens=500)
    
    qa_chain = load_qa_with_sources_chain(llm, chain_type="stuff",
                                      prompt=PROMPT,
                                      document_prompt=EXAMPLE_PROMPT)
    chain = RetrievalQAWithSourcesChain(combine_documents_chain=qa_chain, retriever=vector_store.as_retriever(),
                                        reduce_k_below_max_tokens=True, max_tokens_limit=8000,
                                        return_source_documents=True)
    result = chain.invoke({"question": query}, return_only_outputs=True)
    sources_docs = [doc.metadata['source'] for doc in result['source_documents']]
    
    # Limit to unique sources and max 2
    unique_sources = list(dict.fromkeys(sources_docs))
    return result['answer'], unique_sources[:2]


if __name__ == "__main__":
    urls = [
        "https://www.cnbc.com/2024/12/21/how-the-federal-reserves-rate-policy-affects-mortgages.html",
        "https://www.cnbc.com/2024/12/20/why-mortgage-rates-jumped-despite-fed-interest-rate-cut.html"
    ]

    for status in process_urls(urls):
        print(status)
    answer, sources = generate_answer("Tell me what was the 30 year fixed mortagate rate along with the date?")
    print(f"Answer: {answer}")
    print(f"Sources: {sources}")