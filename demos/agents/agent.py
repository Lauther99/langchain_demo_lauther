from demos.agents.instructions import PREFIX_INSTRUCTION, FORMAT_INSTRUCTIONS, SUFFIX
from typing import Any, Dict, List, Optional

from langchain.callbacks.base import BaseCallbackManager

from langchain.agents.mrkl.base import ZeroShotAgent
from langchain.chains.llm import LLMChain
from langchain.schema.language_model import BaseLanguageModel
from langchain.tools import BaseTool
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.tools.convert_to_openai import format_tool_to_openai_function
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser


def create_agent(
    llm: BaseLanguageModel,
    callback_manager: Optional[BaseCallbackManager] = None,
    lan: str = "es",
    # suffix: Optional[str] = SUFFIX,
    # format_instructions: str = FORMAT_INSTRUCTIONS,
    # input_variables: Optional[List[str]] = None,
    max_iterations: Optional[int] = 5,
    max_execution_time: Optional[float] = None,
    early_stopping_method: str = "force",
    verbose: bool = False,
    agent_executor_kwargs: Optional[Dict[str, Any]] = None,
    tools=List[BaseTool],
    **kwargs: Dict[str, Any],
) -> AgentExecutor:
    """Construct an SQL agent from an LLM and tools."""
    # tools = tools
    # prompt = ZeroShotAgent.create_prompt(
    #         tools,
    #         prefix=prefix,
    #         suffix=suffix,
    #         format_instructions=format_instructions,
    #         input_variables=input_variables,
    #     )
    # llm_chain = LLMChain(
    #         llm=llm,
    #         prompt=prompt,
    #         callback_manager=callback_manager,
    #     )
    # tool_names = [tool.name for tool in tools]
    # agent = ZeroShotAgent(llm_chain=llm_chain, allowed_tools=tool_names, **kwargs)
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                PREFIX_INSTRUCTION[lan],
            ),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )
    llm_with_tools = llm.bind(
        functions=[format_tool_to_openai_function(t) for t in tools]
    )
    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_function_messages(
                x["intermediate_steps"]
            ),
        }
        | prompt
        | llm_with_tools
        | OpenAIFunctionsAgentOutputParser()
    )

    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=verbose,
        callback_manager=callback_manager,
        handle_parsing_errors=True,
        max_iterations=max_iterations,
        max_execution_time=max_execution_time,
        early_stopping_method=early_stopping_method,
        **(agent_executor_kwargs or {}),
    )
