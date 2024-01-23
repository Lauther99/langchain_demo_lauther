import sys

sys.path.append("C:\\Users\\lauth\\OneDrive\\Desktop\\open_ai_assistant")

from demos.tools.sql_translator.instructions import (
    SQL_TRANSLATOR_INSTRUCTION,
    SYSTEM_INSTRUCTION,
    PROMPT_TEMPLATE,
    ERROR_INSTRUCTION,
    SQL_TRANSLATOR_TOOL_DESCRIPTION,
    SQL_FIXER_TOOL_DESCRIPTION,
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


def sql_translate(search_tables, db_schema, query_input, lan="en") -> str:
    description = get_description(db_schema, search_tables, lan)

    prompt = PromptTemplate(
        input_variables=[
            "system_instruction",
            "db_schema",
            "description",
            "sql_translator",
        ],
        template=PROMPT_TEMPLATE[lan],
    )

    formated_prompt = prompt.format(
        db_schema=db_schema,
        description=description,
        sql_translator=SQL_TRANSLATOR_INSTRUCTION[lan].format(query=query_input),
        system_instruction=SYSTEM_INSTRUCTION[lan],
    )

    llm = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-3.5-turbo", temperature=0)
    response = ""
    with get_openai_callback() as cb:
        response = llm.invoke(input=formated_prompt)
        print(f"Total Tokens: {cb.total_tokens}")
    messages = [
        {"role": "system", "content": SYSTEM_INSTRUCTION[lan]},
        {
            "role": "user",
            "content": PROMPT_TEMPLATE[lan].format(
                system_instruction=" ",
                db_schema=db_schema,
                description=description,
                sql_translator=SQL_TRANSLATOR_INSTRUCTION[lan].format(
                    query=query_input
                ),
            ),
        },
        {"role": "assistant", "content": response.content},
    ]

    # Agregando a la db
    save_to_chat(messages, "51989915557")
    return response.content or ""


def sql_error_fixer(error_message, db_schema, lan="en") -> str:
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
    error_input = ERROR_INSTRUCTION[lan].format(
        error_message=error_message, db_schema=db_schema
    )
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


class SQLTranslatorTool(BaseTool):
    name = "sql_translator"
    lan = "en"
    description = SQL_TRANSLATOR_TOOL_DESCRIPTION[lan]
    search_tables = []
    db_schema = "dbo_v2"

    def __init__(self, lan="en", search_tables=[], db_schema="dbo_v2"):
        super().__init__()
        self.lan = lan
        self.description = SQL_TRANSLATOR_TOOL_DESCRIPTION[lan]
        self.search_tables = search_tables
        self.db_schema = db_schema

    def _run(self, query_input: str):
        return sql_translate(
            search_tables=self.search_tables,
            db_schema=self.db_schema,
            query_input=query_input,
            lan=self.lan,
        )

    def _arun(self, query_input: str):
        return sql_translate(
            search_tables=self.search_tables,
            db_schema=self.db_schema,
            query_input=query_input,
            lan=self.lan,
        )


class SQLQueryFixer(BaseTool):
    name = "sql_query_fixer"
    lan = "en"
    description = SQL_FIXER_TOOL_DESCRIPTION[lan]
    db_schema = "dbo_v2"

    def __init__(self, lan="en", db_schema = "dbo_v2"):
        super().__init__()
        self.lan = lan
        self.db_schema = db_schema
        self.description = SQL_FIXER_TOOL_DESCRIPTION[lan]

    def _run(self, query_error: str):
        return sql_error_fixer(
            error_message=query_error, db_schema=self.db_schema, lan=self.lan
        )

    def _arun(self, query_error: str):
        raise NotImplementedError("This tool does not support async")


# Tests

# Test sql_translate()
# search_tables = [
#     "fcs_computadores",
#     "fcs_computador_medidor",
#     "med_sistema_medicion",
#     "var_tipo_variable",
#     "var_variable_datos",
# ]
# query = "Values of the 'Pressão Estática (kPa)' registered in october 17th in 2022 for all measurements systems for the computer with tag FQI-EMED_05-08-10"
# sql_translate(search_tables, "dbo_v2", query)


# # Test sql_error_fixer()
# sql_error_fixer("[42S02] [Microsoft][ODBC Driver 11 for SQL Server][SQL Server]Invalid object name 'fcs_computador_medidor'. (208) (SQLExecDirectW)")
