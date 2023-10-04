import os
import sys
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.text_splitter import CharacterTextSplitter
import environ
from langchain.tools import Tool
# from langchain.agents.agent_toolkits import SQLDatabaseToolkit
sys.path.append('C:\\Users\\lauth\\OneDrive\\Desktop\\py_projects\\langchain_demo_lauther')
from src.sql_toolkit.sql_toolkit import CustomSQLToolkit, FAISSSQLQuerySimilarity
from langchain.chat_models import ChatOpenAI
from sqlalchemy.engine import URL
from langchain.utilities import SQLDatabase


env = environ.Env()
environ.Env.read_env()
API_KEY = env('OPENAI_API_KEY')
USER = env('USER')
PWD = env('PWD')
HOST = env('HOST')
DBNAME = env('DBNAME')
ODBCDRIVER = env('ODBCDRIVER')

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

# Creating embeddings
ruta_completa = os.path.abspath('../langchain_demo_lauther/src/dictionary/data_csv.csv')
loader = CSVLoader(file_path=ruta_completa,csv_args = {"delimiter": ';'}, source_column="Question")
data = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=800, chunk_overlap=0)
docs = text_splitter.split_documents(data)
get_similarity_tool = FAISSSQLQuerySimilarity(model_name="hkunlp/instructor-large", splitted_documents=docs)

# Creating tools
tools = [
    Tool(
        name="search_similar_examples",
        func=get_similarity_tool.get_similar_sql_examples,
        description="Useful when you need to find similar examples that can help you construct the SQL QUERY, input for this tool is the user question, output is a SQL QUERY ",
    )
]
# Getting SQL tools
toolkit = CustomSQLToolkit(db=sql_database, llm=agent_model)
# Setting custom_tools
custom_tools = toolkit.get_tools() + tools 

# Setting the agent_executor
from src.agents.sqlagent import create_sql_agent_plus_extra_tools

agent_executor = create_sql_agent_plus_extra_tools(
    llm=agent_model,
    toolkit=toolkit,
    verbose=True,
    custom_tools=custom_tools,
    top_k=10,
) 

query_str = "how many computers are in the table?"
query_str = "Meters of each computer"
query_str_v2 = "quantity of meters that the computer with IP equal to 10.233.117.63 has"
query_str_v3 = "List the names of the measurement system of the meters that the computer has with tag FQI-3161.01-017?"
query_str_v4 = "List the names of the measurement system of the meters that the computer has with IP equal to 10.233.81.59?"
query_str_v5 = "the computers that are in port 4000"

from langchain.callbacks import get_openai_callback
with get_openai_callback() as cb:
    agent_executor.run(query_str_v2)
    print(f"Total Tokens: {cb.total_tokens}")
    print(f"Prompt Tokens: {cb.prompt_tokens}")
    print(f"Completion Tokens: {cb.completion_tokens}")
    print(f"Total Cost (USD): ${cb.total_cost}")

