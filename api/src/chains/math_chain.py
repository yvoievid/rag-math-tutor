import os
import glob
from langchain_community.document_loaders import PyPDFLoader

if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
BASE_PATH = "/data"


def load_pdf_pages(paths: list):
    directory_path = BASE_PATH

    pdf_files = glob.glob(f"{directory_path}/*.pdf")

    docs = []
    for pdf_file in pdf_files:
        loader = PyPDFLoader(pdf_file)
        docs.extend(loader.load())

    print(len(docs))
    return docs

def fill_data():
    math_pdfs = os.listdir(BASE_PATH)   
    math_docs = load_pdf_pages(math_pdfs)      

    return math_docs
