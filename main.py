from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from src.exec_code import run_code_in_container
from src.extract_code import extract_code

from dotenv import load_dotenv
load_dotenv()

# Setup LLM HuggingFace
# llm = HuggingFaceEndpoint(
#     repo_id="Qwen/Qwen3-Coder-30B-A3B-Instruct",
#     task="text-generation",
#     max_new_tokens=10000
# )
# chat_model = ChatHuggingFace(llm=llm)

# Setup LLM Groq
chat_model = ChatGroq(model="openai/gpt-oss-20b")

# The Prompt Engineering
system_prompt = """
generate python code to find answer.
Instructions:
1. Add '# AUTO_INSTALL: package_name' for dependencies. If no dependencies do not add '# AUTO_INSTALL:'.
2. Put logic in a function.
3. The final answer should be a descriptive string.
4. Store final answer in a variable named 'result'.
5. Don't print anything.
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



query="what's the highlight in this page https://docs.langchain.com/oss/python/integrations/chat/groq"
# query="whats 27 * 35"
# Run it!
chat(query)