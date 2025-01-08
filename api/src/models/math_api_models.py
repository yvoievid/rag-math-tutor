from pydantic import BaseModel
from typing import Any, List
from pydantic import BaseModel
from langchain_core.documents import Document
from typing_extensions import List, TypedDict
from typing import Literal
from typing_extensions import Annotated
from typing import List, Dict, Optional

class MathQueryInput(BaseModel):
    text: str

class Search(TypedDict):
    query: Annotated[str, ..., "Search query to run."]
    section: Annotated[Literal["beginning", "middle", "end"], ..., "Section to query."]

class State(TypedDict):
    question: str
    query: Optional[Search] = {}
    context: Optional[List[Document]] = []
    wolfram_answer: Optional[List[str]] = []
    answer: Optional[str] = ""

class QueryRequest(BaseModel):
    question: str

class MathQueryOutput(BaseModel):
    input: str
    output: str
    intermediate_steps: list
