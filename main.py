from langgraph.graph import StateGraph, START, END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
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


def main():

    messages = [
        # SystemMessage(
        #     content="""generate python code to find answer, only generate the code.
        #     Instructions:
        #     Add the comment # AUTO_INSTALL: package_name1 package_name2 ... on the top of the code if any packages are required.
        #     Don't use print statements in the code.
        #     Put the whole code in a function and run the function to execute the code storing the result to result variable.
        #     The result should be always a descriptive string.
        #     example 1:
        #     # AUTO_INSTALL: numpy
        #     def execute_code():
        #         import numpy
        #         ans = 1 + 1
        #         return f"the answer is {ans}"
        #     result=execute_code()

        #     example 2:
        #     # AUTO_INSTALL: numpy
        #     async def execute_code():
        #         import numpy
        #         import asyncio
        #         ans = 1 + 1
        #         return f"the answer is {ans}"
        #     result=asyncio.run(execute_code())
        #     """
        # )
    ]

    messages.append(HumanMessage(content="what is my age if i was born on 22/02/1989."))
    # messages.append(HumanMessage(content="create me a pandas dataframe with 10 rows and 3 columns with random values"))
    # messages.append(HumanMessage(content="Hello"))
    # messages.append(HumanMessage(content="How many r's are there in strawberries"))
    # messages.append(HumanMessage(content="whats the time and date now use indian timezone"))


    response = chat_model.invoke(messages)

    print(response.content)

    # Extract code
    # code = extract_code(response.content)
    # print(code)

    # # Run code
    # result = run_code_in_container(code)
    # print(result)


main()





