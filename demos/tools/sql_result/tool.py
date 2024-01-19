import sys
sys.path.append("C:\\Users\\lauth\\OneDrive\\Desktop\\open_ai_assistant")
from demos.config.database_connection import conn
from langchain.tools import BaseTool


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
    description: str = """
    Input to this tool is a detailed and correct SQL query, output is a result from the database.
    If the query is not correct, an error message will be returned and you have to use 'sql_query_fixer' tool.
    """
    # If an error is returned, rewrite the query, check the query, and try again.

    def _run(self, sql_query):
        return get_sql_query(sql_query)

    def _arun(self):
        raise NotImplementedError("This tool does not support async")
