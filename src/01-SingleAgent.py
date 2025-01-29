from mysettings import llm_config
from autogen import ConversableAgent


agent = ConversableAgent(
    "chatbot",
    system_message="You are a comedian specialized in telling short story jokes.",
    llm_config=llm_config,
    human_input_mode="NEVER",  # Never ask for human input...
)

reply = agent.generate_reply(
    messages=[{"content": "Tell me a joke.", "role": "user"}])
print(reply)
