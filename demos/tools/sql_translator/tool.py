import sys

sys.path.append("C:\\Users\\lauth\\OneDrive\\Desktop\\open_ai_assistant")

from demos.tools.sql_translator.instructions import (
    sql_translator_instruction,
    system_instruction,
    content_error_instruction,
)
from demos.mongo.users_manager import save_to_chat, find_user
from demos.data.data_info import tables
from demos.config.env_config import OPENAI_API_KEY
from demos.utils.getDescription import get_description
from langchain.tools import BaseTool
from langchain.pydantic_v1 import BaseModel, Field
from langchain.prompts import PromptTemplate
from langchain.memory import (
    ConversationSummaryBufferMemory,
    ConversationBufferMemory,
    ChatMessageHistory,
)
from langchain.chains import ConversationChain, LLMChain
from langchain.llms.openai import OpenAI
from langchain.llms.huggingface_hub import HuggingFaceHub

from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_community.callbacks import get_openai_callback


def get_sql_query(search_tables, db_schema, query_input) -> str:
    description = get_description(db_schema, search_tables)

    prompt_template = """
    {system_instruction}
    Using the schema '{db_schema}' and database information below:\n'''\n{description}\n'''\n{sql_translator_instruction}
    """
    prompt = PromptTemplate(
        input_variables=[
            "system_instruction",
            "db_schema",
            "description",
            "sql_translator_instruction",
        ],
        template=prompt_template,
    )

    formated_prompt = prompt.format(
        db_schema=db_schema,
        description=description,
        sql_translator_instruction=sql_translator_instruction.format(query=query_input),
        system_instruction=system_instruction,
    )

    llm = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-3.5-turbo", temperature=0)
    response = ""
    with get_openai_callback() as cb:
        response = llm.invoke(input=formated_prompt)
        print(f"Total Tokens: {cb.total_tokens}")
    messages = [
        {"role": "system", "content": system_instruction},
        {
            "role": "user",
            "content": prompt_template.format(
                system_instruction=" ",
                db_schema=db_schema,
                description=description,
                sql_translator_instruction=sql_translator_instruction.format(query=query_input),
            ),
        },
        {"role": "assistant", "content": response.content},
    ]

    # Agregando a la db
    save_to_chat(messages, "51989915557")
    return response.content or ""


def sql_error_fixer(error_message) -> str:
    user = find_user("51989915557")
    messages = user["chats"] or []

    llm = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-3.5-turbo")

    # Creando la memoria
    memory_messages = []
    for message in messages:
        role = message.get("role", "")
        content = message.get("content", "")

        if role == "user":
            memory_messages.append(HumanMessage(content=content))
        elif role == "assistant":
            memory_messages.append(AIMessage(content=content))
        elif role == "system":
            memory_messages.append(SystemMessage(content=content))

    memory_history = ChatMessageHistory(messages=memory_messages)
    window_memory = ConversationSummaryBufferMemory(
        llm=llm, chat_memory=memory_history, input_key="input", memory_key="history"
    )
    conversation = ConversationChain(llm=llm, verbose=True, memory=window_memory)
    error_input = content_error_instruction.format(error_message=error_message)
    response = ""

    with get_openai_callback() as cb:
        response = conversation.predict(input=error_input)
        print(f"Total Tokens: {cb.total_tokens}")

    messages.append(
        {
            "role": "user",
            "content": error_input,
        }
    )
    messages.append(
        {
            "role": "assistant",
            "content": response or "",
        }
    )

    # Agregando a la db
    save_to_chat(messages, "51989915557")

    # print(response)
    return response or ""


class BaseSQLDatabaseTool(BaseModel):
    """Base tool for interacting with a SQL database."""

    search_tables: list[str] = Field(exclude=True)
    db_schema: str = Field(exclude=True)

    class Config(BaseTool.Config):
        pass


class SQLTranslatorTool(BaseSQLDatabaseTool, BaseTool):
    name = "sql_translator"
    description = "this tool allows you to translate a text to SQL code or rewrite the query. Input to this tool is a formatted user question, NOT A CODE, ONLY THE OUTPUT is a SQL code"

    def _run(self, query_input: str):
        return get_sql_query(self.search_tables, self.db_schema, query_input)

    def _arun(self, query_input: str):
        return get_sql_query(self.search_tables, self.db_schema, query_input)


class SQLQueryFixer(BaseTool):
    name = "sql_query_fixer"
    description = "this tool allows you to correct and rewrite the query. Input to this tool is only the error message from database failed query from 'sql_db_query' tool, only the output to this tool is a SQL code. Use this tool as many times as you need"

    def _run(self, query_error: str):
        return sql_error_fixer(query_error)

    def _arun(self, query_error: str):
        raise NotImplementedError("This tool does not support async")


# Tests

# Test get_sql_query()
# search_tables = [
#     "fcs_computadores",
#     "fcs_computador_medidor",
#     "med_sistema_medicion",
#     "var_tipo_variable",
#     "var_variable_datos",
# ]
# query = "Values of the 'Pressão Estática (kPa)' registered in october 17th in 2022 for all measurements systems for the computer with tag FQI-EMED_05-08-10"
# get_sql_query(search_tables, "dbo_v2", query)


# # Test sql_error_fixer()
# sql_error_fixer("[42S02] [Microsoft][ODBC Driver 11 for SQL Server][SQL Server]Invalid object name 'fcs_computador_medidor'. (208) (SQLExecDirectW)")
