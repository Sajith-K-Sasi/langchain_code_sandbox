from langchain.chat_models import init_chat_model, BaseChatModel
from langchain.tools import tool,ToolRuntime
from langchain.messages import AnyMessage, SystemMessage, ToolMessage, HumanMessage

from langgraph.graph import StateGraph, START, END
from langgraph.types import Command

from src.exec_code import run_code_in_container
from src.extract_code import extract_code   

from typing_extensions import TypedDict, Annotated
from typing import Literal
import operator
import json

from dotenv import load_dotenv
load_dotenv()


class RouterState(TypedDict):
    action: Literal["compute", "reply"]
    reason: str

class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    router_state: RouterState

model: BaseChatModel = init_chat_model(model="openai/gpt-oss-120b",model_provider="groq")

# Define tools
@tool
def code_executor(code: str) -> str:
    """Execute the given code.

    Args:
        code: The code to execute
    """
    code = extract_code(code)
    return run_code_in_container(code)


# Augment the LLM with tools
code_agent_tools: list[tool] = [code_executor]
tools_by_name: dict[str, tool] = {tool.name: tool for tool in code_agent_tools}
coding_model = model.bind_tools(code_agent_tools)

def tool_node(state: dict):
    """Performs the tool call"""

    result = []
    for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
    return {"messages": result}

router_system_prompt = """
Decide whether to generate code or direct response and give the reason for the same.
Decision Instructions:
1. code generation is needed for arithmetic calculations, math problems, up-to-date information etc.
2. direct response is needed for general questions, information from your knowledge base etc.
Response Instructions:
2. If direct response is required, respond with {"action": "reply", "reason": "reason"}
3. If code generate is required, respond with {"action": "code", "reason": "reason"}
"""

code_agent_system_prompt = """
Always generate python code and execute it to find answer.
Code Generation Instructions:
1. Add '# AUTO_INSTALL: [package_name1, package_name2]' for dependencies if required.
3. Put logic in a function.
4. The final answer should be a descriptive string with the complete result not the summary only.
5. Store final answer in a variable named 'result'.
6. Don't print anything.
Code Execution Instructions:
1. Use tool "code_executor" to execute the code.
2. If tool "code_executor" returns an error, then try again with updated code.
"""

def llm_router(state: MessagesState)-> MessagesState:
    """Decide if we should continue with code agent or llm node"""
    

    state["messages"]=        [
        model.invoke(
            [
            SystemMessage(
                content=router_system_prompt
                )
            ]
            +state["messages"]
            )
            ]
        

    router_state:RouterState = json.loads(state["messages"][-1].content)
    state["router_state"] = router_state

    return state
    
def code_agent(state: MessagesState) -> MessagesState:
    """LLM decides whether to call a tool or not"""

    return {
        "messages": [
            coding_model.invoke(
                [
                    SystemMessage(
                        content=code_agent_system_prompt
                    )
                ]
                + state["messages"]
            )
        ]
    }

def llm_node(state: MessagesState) -> MessagesState:
    """LLM evaluates the result"""
    return {
        "messages": [
            model.invoke(
                [
                    SystemMessage(
                        content="""you are an AI assistant, answer the user query"""
                    )
                ]
                + state["messages"]
            )
        ]
    }
    

def should_call_agent_tool(state: MessagesState) -> Literal["code_agent_tool_node", END]:
    """Decide if we should continue the loop or stop based upon whether the LLM made a tool call"""

    messages:list[AnyMessage] = state["messages"]
    last_message = messages[-1]

    # If the LLM makes a tool call, then perform an action
    if last_message.tool_calls:
        return "code_agent_tool_node"

    # Otherwise, we stop (reply to the user)
    return END

def route_to(state: MessagesState) -> Literal["agent_node", "llm_node"]:
    """Decide which node to route to based upon the router state"""

    router_state = state.get("router_state", RouterState(action="reply"))    

    if router_state["action"] == "code":
        return "code_agent"
    elif router_state["action"] == "reply":
        return "llm_node"
    

# Build workflow
agent_builder = StateGraph(MessagesState)

# Add nodes
agent_builder.add_node("llm_router", llm_router)
agent_builder.add_node("code_agent_tool_node", tool_node)
agent_builder.add_node("llm_node", llm_node)
agent_builder.add_node("code_agent", code_agent)

# Add edges to connect nodes
agent_builder.add_edge(START, "llm_router")
agent_builder.add_conditional_edges(
    "llm_router",
    route_to,
    ["code_agent", "llm_node"]
)
agent_builder.add_conditional_edges(
    "code_agent",
    should_call_agent_tool,
    ["code_agent_tool_node", END]
)
agent_builder.add_edge("code_agent_tool_node", "code_agent")
agent_builder.add_edge("llm_node", END)
# Compile the agent
agent = agent_builder.compile()


# Invoke

query="get me the latest news about bitcoin"
# query="Hello"
# query="what is 3 * 456"


messages: list[HumanMessage] = [HumanMessage(content=query)]
messages = agent.invoke({"messages": messages,"router_state": {"action": "compute"}})
for m in messages["messages"]:
    m.pretty_print()




