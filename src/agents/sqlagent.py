"""SQL agent."""
import sys

sys.path.append('C:\\Users\\lauth\\OneDrive\\Desktop\\py_projects\\langchain_demo_lauther')
from src.prompts.prompt import CUSTOM_PREFIX, CUSTOM_FORMAT_INSTRUCTIONS, CUSTOM_SUFFIX

from typing import Any, Dict, List, Optional

from langchain.agents.agent import AgentExecutor, BaseSingleActionAgent
from langchain.agents.agent_toolkits.sql.prompt import (
    SQL_FUNCTIONS_SUFFIX,
    SQL_PREFIX,
    SQL_SUFFIX,
)
from langchain.agents.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.agents.mrkl.base import ZeroShotAgent
from langchain.agents.mrkl.prompt import FORMAT_INSTRUCTIONS
from langchain.callbacks.base import BaseCallbackManager
from langchain.chains.llm import LLMChain
from langchain.schema.language_model import BaseLanguageModel
from langchain.tools import BaseTool


def create_sql_agent_plus_extra_tools(
    llm: BaseLanguageModel,
    toolkit: SQLDatabaseToolkit,
    callback_manager: Optional[BaseCallbackManager] = None,
    prefix: str = CUSTOM_PREFIX,
    suffix: Optional[str] = CUSTOM_SUFFIX,
    format_instructions: str = CUSTOM_FORMAT_INSTRUCTIONS,
    input_variables: Optional[List[str]] = None,
    top_k: int = 10,
    max_iterations: Optional[int] = 15,
    max_execution_time: Optional[float] = None,
    early_stopping_method: str = "force",
    verbose: bool = False,
    agent_executor_kwargs: Optional[Dict[str, Any]] = None,
    extra_tools = List[BaseTool],
    **kwargs: Dict[str, Any],
) -> AgentExecutor:
    """Construct an SQL agent from an LLM and tools."""
    tools = extra_tools
    prefix = prefix.format(dialect=toolkit.dialect, top_k=top_k)
    agent: BaseSingleActionAgent
    prompt = ZeroShotAgent.create_prompt(
            tools,
            prefix=prefix,
            suffix=suffix or CUSTOM_SUFFIX,
            format_instructions=format_instructions,
            input_variables=input_variables,
        )
    llm_chain = LLMChain(
            llm=llm,
            prompt=prompt,
            callback_manager=callback_manager,
        )
    tool_names = [tool.name for tool in tools]
    agent = ZeroShotAgent(llm_chain=llm_chain, allowed_tools=tool_names, **kwargs)

    return AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        callback_manager=callback_manager,
        verbose=verbose,
        max_iterations=max_iterations,
        max_execution_time=max_execution_time,
        early_stopping_method=early_stopping_method,
        **(agent_executor_kwargs or {}),
    )

