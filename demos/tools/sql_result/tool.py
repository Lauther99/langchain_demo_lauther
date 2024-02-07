import sys

sys.path.append("C:\\Users\\lauth\\OneDrive\\Desktop\\open_ai_assistant")
from demos.config.database_connection import conn
from langchain.tools import BaseTool
from demos.tools.sql_result.instructions import SQL_QUERY_TOOL_DESCRIPTION
from langchain.agents import tool

@tool
def sql_db_query(sql_query: str):
    """
    Input to this tool is a detailed and correct SQL query, output is a result from the database.
    If an empty value is returned, you MUST USE 'sql_translator' tool again.
    If the query is not correct, an error message will be returned.
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql_query)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error executing SQL query: {e}")
        return e.args[1]
    finally:
        cursor.close()

# class SQLQueryTool(BaseTool):
#     name = "sql_db_query"
#     description: str = SQL_QUERY_TOOL_DESCRIPTION
#     # If an error is returned, rewrite the query, check the query, and try again.

#     def __init__(self):
#         super().__init__()
#         self.description = SQL_QUERY_TOOL_DESCRIPTION

#     def _run(self, sql_query):
#         return sql_db_query(sql_query)

#     def _arun(self):
#         raise NotImplementedError("This tool does not support async")
