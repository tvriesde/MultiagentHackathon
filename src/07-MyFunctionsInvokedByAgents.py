import os
import pprint
from autogen import AssistantAgent, UserProxyAgent
from typing import Annotated, Literal
from mysettings import llm_config
from autogen import register_function

Operator = Literal["+", "-", "*", "/"]


def calculator(a: int, b: int, operator: Annotated[Operator, "operator"]) -> int:
    if operator == "+":
        return a + b
    elif operator == "-":
        return a - b
    elif operator == "*":
        return a * b
    elif operator == "/":
        return int(a / b)
    else:
        raise ValueError("Invalid operator")


# Let's first define the assistant agent that suggests tool calls.
assistant = AssistantAgent(
    name="Assistant",
    system_message="You are a helpful AI assistant. "
    "You can help with simple calculations. "
    "Return 'TERMINATE' when the task is done.",
    llm_config=llm_config
)

# The user proxy agent is used for interacting with the assistant agent
# and executes tool calls.
user_proxy = UserProxyAgent(
    name="User",
    llm_config=False,
    is_termination_msg=lambda msg: msg.get(
        "content") is not None and "TERMINATE" in msg["content"],
    human_input_mode="NEVER",
)

register_function(
    calculator,
    # The assistant agent can suggest calls to the calculator.
    caller=assistant,
    # The user proxy agent can execute the calculator calls.
    executor=user_proxy,
    # By default, the function name is used as the tool name.
    name="calculator",
    description="A simple calculator",  # A description of the tool.
)

chat_result = user_proxy.initiate_chat(
    assistant, message="What is (44232 + 13312 / (232 - 32)) * 5?")

pprint.pp(assistant.llm_config["tools"])
