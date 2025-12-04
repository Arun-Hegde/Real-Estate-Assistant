# 🏙️ Real Estate Research Tool

**An AI-powered research assistant for the real estate domain.**

This tool allows users to input news article URLs, process them to extract insights, and ask questions to get accurate answers with source citations. It leverages **LangChain**, **Groq (Llama 3)**, and **ChromaDB** for efficient RAG (Retrieval-Augmented Generation).

![product screenshot](/image.png)

## ✨ Features

-   **🔗 URL Loading**: Fetch content directly from news article URLs with custom headers for reliable access.
-   **🧠 Intelligent Processing**: Uses LangChain's WebBaseLoader and RecursiveCharacterTextSplitter for robust content extraction.
-   **🔍 Vector Search**: HuggingFace embeddings stored in ChromaDB for fast and accurate retrieval.
-   **🤖 LLM Integration**: Powered by Llama 3.3 70B (via Groq) for high-quality, precise answers.
-   **📚 Source Citations**: Every answer includes up to 2 relevant source article links.
-   **🎯 Precise Answers**: Optimized prompts ensure concise and accurate responses.

## 🛠️ Setup & Installation

1.  **Clone the repository** (if you haven't already).

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Environment Configuration**:
    Create a `.env` file in the root directory with your Groq API credentials:
    ```env
    GROQ_API_KEY=your_groq_api_key_here
    ```

4.  **Run the Application**:
    ```bash
    streamlit run main.py
    ```

## 🚀 Usage

1.  Open the web app in your browser (usually `http://localhost:8501`).
2.  **Sidebar**: Enter up to 3 URLs of real estate news articles.
3.  Click **"Process URLs"**. Wait for the "Processing Complete!" message.
4.  **Ask a Question**: Type your query in the main input box (e.g., "What are the current mortgage rate trends?").
5.  **Get Answers**: Read the AI-generated response and check the sources.

### Example Articles
-   [CNBC: Fed Rate Policy & Mortgages](https://www.cnbc.com/2024/12/21/how-the-federal-reserves-rate-policy-affects-mortgages.html)
-   [CNBC: Mortgage Rates Jump](https://www.cnbc.com/2024/12/20/why-mortgage-rates-jumped-despite-fed-interest-rate-cut.html)

---

## 📄 License

This software is licensed under the MIT License.
**Commercial use is strictly prohibited without prior written permission.**
Attribution is required for any substantial use.

### 🙋‍♂️ Author
Developed by **Arun Hegde**

📎 Git Hub - [GitHub Profile](https://github.com/Arun-Hegde)

Feel free to ⭐ the repo or connect on GitHub!
