import sys

sys.path.append("C:\\Users\\lauth\\OneDrive\\Desktop\\open_ai_assistant")
from demos.config.database_connection import conn
from langchain.tools import BaseTool
from demos.tools.sql_result.instructions import SQL_QUERY_TOOL_DESCRIPTION


def get_sql_query(sql_query: str):
    try:
        cursor = conn.cursor()
        cursor.execute(sql_query)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error executing SQL query: {e}")
        return e.args[1]
    finally:
        cursor.close()


class SQLQueryTool(BaseTool):
    name = "sql_db_query"
    lan = "en"
    description: str = SQL_QUERY_TOOL_DESCRIPTION[lan]
    # If an error is returned, rewrite the query, check the query, and try again.

    def __init__(self, lan="en"):
        super().__init__()
        self.lan = lan
        self.description = SQL_QUERY_TOOL_DESCRIPTION[lan]

    def _run(self, sql_query):
        return get_sql_query(sql_query)

    def _arun(self):
        raise NotImplementedError("This tool does not support async")
