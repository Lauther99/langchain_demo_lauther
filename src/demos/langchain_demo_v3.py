import os
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
import environ
from typing import (List)

env = environ.Env()
environ.Env.read_env()
API_KEY = env('OPENAI_API_KEY')
USER = env('USER')
PWD = env('PWD')
HOST = env('HOST')
DBNAME = env('DBNAME')
ODBCDRIVER = env('ODBCDRIVER')

from langchain.chat_models import ChatOpenAI, AzureChatOpenAI
from sqlalchemy.engine import URL
from langchain.utilities import SQLDatabase

connection_uri = URL.create(
    "mssql+pyodbc",
    username=USER,
    password=PWD,
    host=HOST,
    database=DBNAME,
    query={"driver": ODBCDRIVER},
)
# Setting database object
search_tables = ["fcs_computadores", "fcs_computador_medidor", "med_sistema_medicion"]
sql_database = SQLDatabase.from_uri(connection_uri, schema='dbo_v2', include_tables=search_tables, sample_rows_in_table_info=2)

# Setting the agent model
agent_model = ChatOpenAI(temperature=0, openai_api_key=API_KEY, model="gpt-3.5-turbo")

# Creating tools
from langchain.tools.base import ToolException
from langchain.tools import BaseTool, Tool, BaseSQLDatabaseTool

ruta_completa = os.path.abspath('../langchain_demo_lauther/src/dictionary/data_csv.csv')
loader = CSVLoader(file_path=ruta_completa,csv_args = {"delimiter": ';'}, source_column="Question")
data = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=800, chunk_overlap=0)
docs = text_splitter.split_documents(data)

class FAISSSQLQuerySimilarity: #Todo: Comparar con los resultados de 'Vectara, Pinecone, Chroma' para ver cual es más conveniente
    def __init__(self, model_name: str, splitted_documents: List[Document]):
        self.model_name = model_name
        self.hf_model = HuggingFaceEmbeddings(model_name=self.model_name)
        self.db = FAISS.from_documents(splitted_documents, self.hf_model)

    def get_similar_sql_examples(self, query: str):
        '''Use this tool to get similar SQL queries from a database'''
        embedding_vector = self.hf_model.embed_query(query)
        similar_results = self.db.similarity_search_with_score_by_vector(embedding_vector, k=1, score_threshold=0.25)
        #return similar_results # To see the score and results
        page_content = similar_results[0][0].page_content if similar_results else ""
        lineas = page_content.split('\n')
        for linea in lineas:
            if linea.startswith('Query:'):
                query = linea[len('Query:'):].strip()
                return query
        else:
            return ""

embeddings_model_name = "hkunlp/instructor-large"
get_similarity_tool = FAISSSQLQuerySimilarity(model_name=embeddings_model_name, splitted_documents=docs)

def _handle_error(error: ToolException) -> str:
    return (
        "The following errors occurred during tool execution:"
        + error.args[0]
        + "Please try another tool."
    )

tools = [
    Tool(
        name="search_similar_examples",
        func=get_similarity_tool.get_similar_sql_examples,
        description="Useful when you need to find similar examples that can help you construct the SQL QUERY, output is a SQL QUERY ",
        handle_tool_error=_handle_error,
    )
]

# Setting SQL Toolkit
from langchain.agents.agent_toolkits import SQLDatabaseToolkit 

toolkit = SQLDatabaseToolkit(db=sql_database, llm=agent_model)

#Setting the Prompt
from langchain.prompts import PromptTemplate

prompt_template = PromptTemplate.from_template(
    "Tell me a {adjective} joke about {content}."
)
tool_names = [tool.name for tool in tools]

# Setting the agent
import sys

sys.path.append('C:\\Users\\lauth\\OneDrive\\Desktop\\py_projects\\langchain_demo_lauther')
from src.agents.sqlagent import create_sql_agent_plus_extra_tools

agent_executor = create_sql_agent_plus_extra_tools(
    llm=agent_model,
    toolkit=toolkit,
    verbose=True,
    extra_tools=tools+toolkit.get_tools(),
    top_k=10,
) 

query_str = "how many computers are in the table?"
query_str = "Meters of each computer"
query_str_v2 = "quantity of meters that the computer with IP equal to 1.1.1.1 has"
query_str_v3 = "List the names of the measurement system of the meters that the computer has with tag FQI-3161.01-017?"
query_str_v4 = "List the names of the measurement system of the meters that the computer has with IP equal to 10.233.81.59?"
query_str_v5 = "the computers that are in port 4000"

from langchain.callbacks import get_openai_callback
with get_openai_callback() as cb:
    agent_executor.run(query_str)
    print(f"Total Tokens: {cb.total_tokens}")
    print(f"Prompt Tokens: {cb.prompt_tokens}")
    print(f"Completion Tokens: {cb.completion_tokens}")
    print(f"Total Cost (USD): ${cb.total_cost}")

