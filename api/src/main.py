from fastapi import FastAPI, HTTPException
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter

from chains.math_chain import fill_data
from langgraph.graph import START, StateGraph
from langchain_core.prompts import PromptTemplate
from langchain_chroma import Chroma
from models.math_api_models import State, Search, QueryRequest

app = FastAPI(title="Math Tutor", description="Endpoints for math tutor")

llm = ChatOpenAI(model="gpt-4o-mini")
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
vector_store = Chroma(embedding_function=embeddings)


def analyze_query(state: State):
    structured_llm = llm.with_structured_output(Search)
    query = structured_llm.invoke(state["question"])
    state["query"] = query
    return {"query": query}


def retrieve(state: State):
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

    state["context"] = retrieved_docs
    return {"context": retrieved_docs}


def generate(state: State):
    template = """You are an AI math tutor that generates excercises to prepare for math exams, use the following context to answer the questions and generate responses
    If you will generate LaTeX code or equations use $ format instead of \( and $$ instead of \[
    {context}

    Question: {question}

    Helpful Answer:"""
    custom_prompt = PromptTemplate.from_template(template)
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    prompt = custom_prompt.invoke({"question": state["question"], "context": docs_content})
    response = llm.invoke(prompt)
    state["answer"] = response.content
    return {"answer": response.content}


@app.on_event("startup")
async def startup_event():
    global graph
    math_pages = fill_data()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=200)
    all_splits = text_splitter.split_documents(math_pages)
    vector_store.add_documents(documents=all_splits)

    graph_builder = StateGraph(State).add_sequence([analyze_query, retrieve, generate])
    graph_builder.add_edge(START, "analyze_query")
    graph = graph_builder.compile()


@app.post("/query/")
async def query_endpoint(request: QueryRequest):
    try:
        response = await graph.ainvoke({"question": request.question})
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def get_status():
    return {"status": "running"}


@app.post("/math-rag-agent")
async def query_hospital_agent(query: QueryRequest) -> State:
    try:
        answer = await graph.ainvoke({"question": query.question})

        state = State(
            question=query.question,
            query=answer.get("query", {}),
            context=answer.get("context", []),
            answer=answer.get("answer", "")
        )

        return state
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
