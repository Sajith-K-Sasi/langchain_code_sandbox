from langchain_core.messages import HumanMessage, SystemMessage
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

from rich.console import Console
from rich.panel import Panel

from src.exec_code import run_code_in_container
from src.extract_code import extract_code

from dotenv import load_dotenv
load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen3-Coder-480B-A35B-Instruct",
    task="text-generation",
    max_new_tokens=512,
    do_sample=False,
    repetition_penalty=1.03,
    provider="auto",
)

chat_model = ChatHuggingFace(llm=llm)


def chat(query:str):

    console = Console()

    # without code execution

    messages = [
        SystemMessage(content="You are a helpful assistant"),
        HumanMessage(content=query)
    ]   

    response = chat_model.invoke(messages)
    
    panel = Panel(query, title="Question", border_style="blue")
    console.print(panel)
    
    panel = Panel(response.content, title="AI Response - without code execution", border_style="red")
    console.print(panel)

    # with code execution

    messages = [
        SystemMessage(
            content="""generate python code to find answer, only generate the code.
            Instructions:
            Add the comment # AUTO_INSTALL: package_name1 package_name2 ... on the top of the code for any additional packages that are required for the code to run successfully.
            Don't use print statements in the code.
            Put the whole code in a function and run the function to execute the code storing the result to result variable.
            The result should be always a descriptive string.
            example 1:
            # AUTO_INSTALL: numpy
            def execute_code():
                import numpy
                ans = 1 + 1
                return f"the answer is {ans}"
            result=execute_code()

            example 2:
            # AUTO_INSTALL: numpy
            async def execute_code():
                import numpy
                import asyncio
                ans = 1 + 1
                return f"the answer is {ans}"
            result=asyncio.run(execute_code())
            """
        ),
        HumanMessage(content=query),
    ]

    response = chat_model.invoke(messages)

    # Extract code
    code = extract_code(response.content)

    # Run code
    result = run_code_in_container(code)
    panel = Panel(result, title="AI Response - with code execution", border_style="green")
    console.print(panel)





# query = "create me a pandas dataframe with 10 rows and 3 columns with random values"
# query = "Hello"
# query = "How many r's are there in strawberries"
query = "what's the time and date now in Indian timezone"
# query = "what is my age if i was born on 22/02/1989."
chat(query)






