from langchain_core.prompts import PromptTemplate

template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

{summaries}

Question: {question}
Helpful Answer:"""

updated_template = "You are a helpful assistant for RealEstate research. Please provide a precise answer. " + template
PROMPT = PromptTemplate(template=updated_template, input_variables=["summaries", "question"])

EXAMPLE_PROMPT = PromptTemplate(
    template="Content: {page_content}\nSource: {source}",
    input_variables=["page_content", "source"],
)