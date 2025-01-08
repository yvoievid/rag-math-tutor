from langchain_core.tools import tool
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from models.math_api_models import State, Search
from chains.math_chain import load_pdf_pages, fill_data

def analyze_query(state: State):
    """_summary_

    Args:
        state (State): _description_

    Returns:
        _type_: _description_
    """
    print(state)
    structured_llm = llm.with_structured_output(Search)
    query = structured_llm.invoke(state["question"])
    state["query"] = query
    return {"query": query}


def retrieve(state: State):
    """_summary_

    Args:
        state (State): _description_

    Returns:
        _type_: _description_
    """
    
    print(state)
    query = state["query"]
    query_text = query.get("query")
    section = query.get("section")

    if not query_text:
        raise ValueError("Query text is missing in the state['query'].")

    retrieved_docs = vector_store.similarity_search(
        query_text,
        k=5,
        filter={"section": section} if section else None
    )

    quizzes = []
    for doc in retrieved_docs:
        if "quiz" in doc.metadata or "exercise" in doc.metadata:
            quizzes.append(doc.page_content)

    state["context"] = quizzes
    return {"context": quizzes}


def generate(state: State):
    """_summary_

    Args:
        state (State): _description_

    Returns:
        _type_: _description_
    """
    print("generating",state)
    template = """You are an AI math tutor that generates exercises to prepare for math exams. Generate 10 questions for exam, considering the preferences that user inputs. Use provided context to generate questions.Use Ukraininan to answer.
    Only answer for math questions, nothing else. If you are asked anything not related to the topic, say: "Вибачте я вас не розумію, назвіть тему до якої хочете підготуватись" 
    If you will generate LaTeX code or equations, use $ format instead of \\( and $$ instead of \\[
    Context: {context}
    Question: {question}

    Helpful Answer:"""
    custom_prompt = PromptTemplate.from_template(template)
    docs_content = "\n\n".join(state["context"])
    prompt = custom_prompt.invoke({"question": state["question"], "context": docs_content})
    response = llm.invoke(prompt)
    state["answer"] = response.content
    return {"answer": response.content}




async def query_wolfram(state: State):
    """_summary_

    Args:
        state (State): _description_

    Returns:
        _type_: _description_
    """
                    
    template = """Work as Wolfram Alpha api to answer following question. Use Ukraininan to answer. 
    Use LaTeX for displaying equations.
    If you will generate LaTeX code or equations, use $ format instead of \\( and $$ instead of \\[
    Never use \\( and \\[ in LaTeX, only use $ and $$ 

    Question: {answer}

    Helpful Answer:"""
    custom_prompt = PromptTemplate.from_template(template)
    prompt = custom_prompt.invoke({"answer": state["answer"]})
    response = llm.invoke(prompt)
    state["wolfram_answer"] = response.content
    print("end quering wolfram", response.content)
    return {"wolfram_answer": response.content}



def generate_builder():
    global llm, vector_store
    math_pages = fill_data()

    llm = ChatOpenAI(model="gpt-4o-mini")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    vector_store = Chroma(embedding_function=embeddings)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=200)
    all_splits = text_splitter.split_documents(math_pages)
    vector_store.add_documents(documents=all_splits)

    graph_builder = StateGraph(State).add_sequence([analyze_query, retrieve, generate, query_wolfram])

    graph_builder.add_edge(START, "analyze_query")
    graph_builder.add_edge("analyze_query", "retrieve")
    graph_builder.add_edge("retrieve", "generate")
    graph_builder.add_edge("generate", "query_wolfram")
    graph_builder.add_edge("query_wolfram", END)

    graph = graph_builder.compile()

    return graph
