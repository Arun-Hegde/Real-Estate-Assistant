import streamlit as st
from rag import process_urls, generate_answer

st.set_page_config(page_title="Real Estate Research Tool", page_icon="🏙️", layout="wide")

# Initialize session state for vector store
if 'vector_store' not in st.session_state:
    st.session_state.vector_store = None

# Custom CSS for a premium look
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #FF4B4B;
        color: white;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
    }
    .css-1d391kg {
        padding-top: 3.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏙️ Real Estate Research Tool")
st.markdown("### 🤖 AI-Powered News Research Assistant")

with st.sidebar:
    st.header("Configuration")
    st.markdown("Enter the URLs of the news articles you want to analyze.")
    url1 = st.text_input("URL 1", placeholder="https://example.com/article1")
    url2 = st.text_input("URL 2", placeholder="https://example.com/article2")
    url3 = st.text_input("URL 3", placeholder="https://example.com/article3")
    
    process_url_button = st.button("Process URLs")

main_placeholder = st.empty()

urls = [url for url in (url1, url2, url3) if url.strip() != ""]

if process_url_button:
    if not urls:
        st.error("Please provide at least one valid URL.")
    else:
        with st.spinner("Processing URLs..."):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Consume generator and update progress
            steps = 0
            for item in process_urls(urls, st.session_state.vector_store):
                if isinstance(item, str):
                    # It's a status message
                    steps += 1
                    progress_value = min(steps * 20, 100)
                    progress_bar.progress(progress_value)
                    status_text.text(item)
                else:
                    # It's the vector store being returned
                    st.session_state.vector_store = item
            
            progress_bar.progress(100)
            status_text.success("Processing Complete! ✅")

st.divider()

query = st.text_input("Ask a question about the articles:", placeholder="e.g., What are the current mortgage rates?")

if query:
    if st.session_state.vector_store is None:
        st.error("Please process URLs first before asking questions.")
    else:
        try:
            with st.spinner("Generating answer..."):
                answer, sources = generate_answer(query, st.session_state.vector_store)
                
            st.markdown("### Answer")
            st.info(answer)

            if sources:
                st.markdown("### Sources")
                with st.expander("View Source URLs"):
                    for source in sources:
                        st.markdown(f"- [{source}]({source})")
                        
        except RuntimeError as e:
            st.error(f"Error: {str(e)}. Please process URLs first.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")