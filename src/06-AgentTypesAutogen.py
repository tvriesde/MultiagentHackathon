from autogen import UserProxyAgent, AssistantAgent
import pprint

# UserProxyAgent is a subclass of ConversableAgent
# Existing AutoGen examples often create code executor agent using the
# UserProxyAgent class, which is a subclass of ConversableAgent with
# human_input_mode = ALWAYS and llm_config = False – it always requests
# human input for every message and does not use LLM. It also comes with
# default description field for each of the human_input_mode setting.
# This class is a convenient short-cut for creating an agent that is
# intended to be used as a code executor.
user_proxy_agent = UserProxyAgent(
    name="user_proxy_agent"
)

pprint.pp(user_proxy_agent.description)
pprint.pp(user_proxy_agent.code_executor)

# AssistantAgent is a subclass of ConversableAgent with human_input_mode=NEVER
# and code_execution_config=False – it never requests human input and does not
# use code executor. It also comes with default system_message and description
# fields. This class is a convenient short-cut for creating an agent that is
# intended to be used as a code writer and does not execute code.
pprint.pprint(AssistantAgent.DEFAULT_SYSTEM_MESSAGE)
