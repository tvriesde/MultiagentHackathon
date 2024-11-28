from autogen import GroupChatManager
from autogen import GroupChat
from autogen import AssistantAgent, UserProxyAgent, ConversableAgent
from mysettings import llm_config
from mysettings import generated_directory

# Create Agents, GroupChat, and GroupChatManager in line with the original group chat

planner = AssistantAgent(
    name="Planner",
    system_message="""Planner. Suggest a plan. Revise the plan based on feedback from admin and critic, until admin approval.
The plan may involve an engineer who can write code and a scientist who doesn't write code.
Explain the plan first. Be clear which step is performed by an engineer, and which step is performed by a scientist.
""",
    llm_config=llm_config,
)

user_proxy = UserProxyAgent(
    name="Admin",
    system_message="A human admin. Interact with the planner to discuss the plan. Plan execution needs to be approved by this admin.",
    code_execution_config=False,
)

engineer = AssistantAgent(
    name="Engineer",
    llm_config=llm_config,
    system_message="""Engineer. You follow an approved plan. You write and return python/shell code to solve tasks assigned to you. Wrap the code in a code block that specifies the script type. The user can't modify your code. So do not suggest incomplete code which requires others to modify. Don't use a code block if it's not intended to be executed by the executor.
Don't include multiple code blocks in one response. Do not ask others to copy and paste the result. Check the execution result returned by the executor.
If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try.
Your only task is to write code and return the code. You don't return any other response than code.
"""
)

scientist = AssistantAgent(
    name="Scientist",
    llm_config=llm_config,
    system_message="""
    Scientist. You follow an approved plan. You are able to categorize papers after seeing their abstracts printed. You do not write code.
    """,
)

executor = UserProxyAgent(
    name="Executor",
    system_message="Executor. Execute the code written by the engineer and report the result.",
    human_input_mode="NEVER",
    code_execution_config={
        "last_n_messages": 3,
        "work_dir": generated_directory,
        "use_docker": False,
    },
)

groupchat = GroupChat(
    agents=[user_proxy, engineer, scientist, planner, executor],
    messages=[],
    max_round=10,
)

manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)

task = """
Find the latest paper about gpt-4 on arxiv and find its potential applications in software
"""

result = user_proxy.initiate_chat(manager, message=task)
