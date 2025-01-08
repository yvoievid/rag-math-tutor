from fastapi import FastAPI, HTTPException
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter

from chains.math_chain import fill_data
from langgraph.graph import START, StateGraph
from langchain_core.prompts import PromptTemplate
from langchain_chroma import Chroma
from models.math_api_models import State, Search, QueryRequest
from agents.math_agent import generate_builder
app = FastAPI(title="Math Tutor", description="Endpoints for math tutor")

llm = ChatOpenAI(model="gpt-4o-mini")
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
vector_store = Chroma(embedding_function=embeddings)

@app.on_event("startup")
async def startup_event():
    global graph
    graph = generate_builder()


@app.post("/query/")
async def query_endpoint(request: QueryRequest):
    try:
        state = {
            "question": request.question,
            "query": {},
            "context": [],
            "wolfram_answer": [],
            "answer": ""
        }

        response = await graph.ainvoke(state)
        
        return {"response": response}        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def get_status():
    return {"status": "running"}


@app.post("/math-rag-agent")
async def query_hospital_agent(query: QueryRequest):
    try:
        state = {
            "question": query.question,
            "query": {},
            "context": [],
            "wolfram_answer": [],
            "answer": ""
        }
        
        graph_response = await graph.ainvoke(state)

        state = {
            "question": query.question,
            "query": graph_response.get("query", {}),
            "context": graph_response.get("context", []),
            "wolfram_answer": graph_response.get("wolfram_answer", []),
            "answer": graph_response.get("answer", "")
        }
        
        return state
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
