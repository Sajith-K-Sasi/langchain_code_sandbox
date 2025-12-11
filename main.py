from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.messages import HumanMessage, SystemMessage
from src.exec_code import run_code_in_container
from src.extract_code import extract_code

from dotenv import load_dotenv
load_dotenv()

# Setup LLM
llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen3-Coder-480B-A35B-Instruct",
    task="text-generation",
    max_new_tokens=512
)
chat_model = ChatHuggingFace(llm=llm)

# The Prompt Engineering
system_prompt = """
generate python code to find answer.
Instructions:
1. Add '# AUTO_INSTALL: package_name' for dependencies.
2. Put logic in a function.
3. The final answer should be a descriptive string.
4. Store final answer in a variable named 'result'.
"""

def chat(query: str):
    # 1. Ask LLM to generate code
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=query)
    ]
    response = chat_model.invoke(messages)
    
    # 2. Extract and Run Code
    code = extract_code(response.content)
    print(f"Generated code:\n{code}")
    output = run_code_in_container(code)
    
    print(f"Result: {output}")

# Run it!
chat("what's the time and date now in Indian timezone")