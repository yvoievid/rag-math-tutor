from pydantic import BaseModel
from typing import Any, List
from pydantic import BaseModel
from langchain_core.documents import Document
from typing_extensions import List, TypedDict
from typing import Literal
from typing_extensions import Annotated

class MathQueryInput(BaseModel):
    text: str

class Search(TypedDict):
    query: Annotated[str, ..., "Search query to run."]
    section: Annotated[Literal["beginning", "middle", "end"], ..., "Section to query."]

class State(TypedDict):
    question: str
    query: Search
    context: List[Document]
    answer: str

class QueryRequest(BaseModel):
    question: str

class MathQueryOutput(BaseModel):
    input: str
    output: str
    intermediate_steps: list
