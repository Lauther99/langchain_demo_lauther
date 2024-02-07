import sys

sys.path.append("C:\\Users\\lauth\\OneDrive\\Desktop\\open_ai_assistant")

from demos.tools.sql_translator.instructions import (
    SQL_TRANSLATOR_INSTRUCTION,
    SYSTEM_INSTRUCTION,
    PROMPT_TEMPLATE,
    ERROR_INSTRUCTION,
    SQL_TRANSLATOR_TOOL_DESCRIPTION,
    SQL_FIXER_TOOL_DESCRIPTION,
    SQL_FILTER_TOOL
)
from demos.mongo.users_manager import save_to_chat, find_user
from demos.data.data_info import tables
from demos.config.env_config import OPENAI_API_KEY, VANNA_API_KEY, VANNA_MODEL, OPENAI_MODEL
from demos.utils.getDescription import get_description
from langchain.tools import BaseTool
from langchain.prompts import PromptTemplate
from langchain.memory import (
    ConversationSummaryBufferMemory,
    ConversationBufferMemory,
    ChatMessageHistory,
)

from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_community.callbacks import get_openai_callback
from langchain.agents import tool

from vanna.remote import VannaDefault

@tool
def sql_translator(question) -> str:
    '''
    this tool allows you to translate a text to SQL code or rewrite the query. Input to this tool is the user question, NOT A SQL CODE, ONLY THE OUTPUT  to this tool is a SQL code
    '''
    vn = VannaDefault(model="test-lauther-2", api_key="7e2cde60a92a41bd988a444d6fd1dc22")
    res = vn.generate_sql(question=question)
    return res
    
@tool
def sql_filter_tool(question :str)  -> bool:
    '''
    Useful when you need to filter the user question if need to be translated to SQL code or can easily be aswered by yourself, input to this tool is the user question and the output to this tool is a boolean True or False
    '''
    vn = VannaDefault(model="test-lauther-3", api_key="7e2cde60a92a41bd988a444d6fd1dc22")
    res = vn.generate_sql(question=question)
    if (res == "No SELECT statement could be found in the SQL code"):
        return False
    else:
        return True

# Antiguas tools
def sql_translate(search_tables, db_schema, query_input) -> str:
    description = get_description(db_schema, search_tables)

    prompt = PromptTemplate(
        input_variables=[
            "system_instruction",
            "db_schema",
            "description",
            "sql_translator",
        ],
        template=PROMPT_TEMPLATE,
    )

    formated_prompt = prompt.format(
        db_schema=db_schema,
        description=description,
        sql_translator=SQL_TRANSLATOR_INSTRUCTION.format(query=query_input),
        system_instruction=SYSTEM_INSTRUCTION,
    )

    llm = ChatOpenAI(api_key=OPENAI_API_KEY, model=OPENAI_MODEL, temperature=0)
    response = ""
    with get_openai_callback() as cb:
        response = llm.invoke(input=formated_prompt)
        print(f"Total Tokens: {cb.total_tokens}")
    messages = [
        {"role": "system", "content": SYSTEM_INSTRUCTION},
        {
            "role": "user",
            "content": PROMPT_TEMPLATE.format(
                system_instruction=" ",
                db_schema=db_schema,
                description=description,
                sql_translator=SQL_TRANSLATOR_INSTRUCTION.format(
                    query=query_input
                ),
            ),
        },
        {"role": "assistant", "content": response.content},
    ]

    # Agregando a la db
    save_to_chat(messages, "51989915557")
    return response.content or ""

def sql_error_fixer(error_message, db_schema) -> str:
    user = find_user("51989915557")
    messages = user["chats"] or []

    llm = ChatOpenAI(api_key=OPENAI_API_KEY, model=OPENAI_MODEL)

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
    error_input = ERROR_INSTRUCTION.format(
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

class SQLQueryFixer(BaseTool):
    name = "sql_query_fixer"
    description = SQL_FIXER_TOOL_DESCRIPTION
    db_schema = "dbo_v2"

    def __init__(self, db_schema = "dbo_v2"):
        super().__init__()
        self.db_schema = db_schema
        self.description = SQL_FIXER_TOOL_DESCRIPTION

    def _run(self, query_error: str):
        return sql_error_fixer(
            error_message=query_error, db_schema=self.db_schema
        )

    def _arun(self, query_error: str):
        raise NotImplementedError("This tool does not support async")
