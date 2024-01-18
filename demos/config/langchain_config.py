import sys

sys.path.append("C:\\Users\\lauth\\OneDrive\\Desktop\\open_ai_assistant")
from langchain.utilities.sql_database import SQLDatabase
from sqlalchemy.engine import URL
from demos.config.env_config import USER, PWD, HOST, DBNAME, ODBCDRIVER


# # Used when creating agent with langchain native sql tools
# connection_uri = URL.create(
#     "mssql+pyodbc",
#     username=USER,
#     password=PWD,
#     host=HOST,
#     database=DBNAME,
#     query={"driver": ODBCDRIVER},
# )
# def get_langchain_sql_object(search_tables) -> SQLDatabase:
#     sql: SQLDatabase = SQLDatabase.from_uri(
#         connection_uri,
#         schema="dbo_v2",
#         include_tables=search_tables,
#         sample_rows_in_table_info=2,
#     )
#     return sql
