from autogen import AssistantAgent, UserProxyAgent, ConversableAgent
from mysettings import llm_config
from mysettings import generated_directory
from autogen.coding import LocalCommandLineCodeExecutor

code_executor = LocalCommandLineCodeExecutor(work_dir=generated_directory)

user_proxy = UserProxyAgent(
    name="user_proxy",
    is_termination_msg=lambda x: x.get("content", "") and x.get(
        "content", "").rstrip().endswith("TERMINATE"),
    human_input_mode="TERMINATE",
    max_consecutive_auto_reply=10,
    code_execution_config={"executor": code_executor},
)

writing_assistant = AssistantAgent(
    name="writing_assistant",
    system_message="You are an writing assistant tasked to write engaging blogpost. You try generate the best blogpost possible for the user's request. If the user provides critique, respond with a revised version of your previous attempts.",
    llm_config={"config_list": llm_config["config_list"], "cache_seed": None},
)

reflection_assistant = AssistantAgent(
    name="reflection_assistant",
    system_message="Generate critique and recommendations on the writing. Provide detailed recommendations, including requests for length, depth, style, etc..",
    llm_config={"config_list": llm_config["config_list"], "cache_seed": None},
)


def reflection_message(recipient, messages, sender, config):
    print("Reflecting...")
    return f"Reflect and provide critique on the following writing. \n\n {recipient.chat_messages_for_summary(sender)[-1]['content']}"


nested_chat_queue = [
    {
        "recipient": reflection_assistant,
        "message": reflection_message,
        "max_turns": 1,
    },
]
user_proxy.register_nested_chats(
    nested_chat_queue,
    trigger=writing_assistant,
    # position=4,
)

user_proxy.initiate_chat(
    writing_assistant,
    message="Write an engaging blogpost on the recent updates in AI. "
    "The blogpost should be engaging and understandable for general audience. "
    "Should have more than 3 paragraphes but no longer than 1000 words.",
    max_turns=2
)
