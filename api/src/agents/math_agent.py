# import os 
# from langchain_openai import ChatOpenAI
# from langchain.agents import (
#     create_openai_functions_agent,
#     Tool,
#     AgentExecutor,
# )
# from langchain import hub
# from chains.math_chain import math_vector_chain

# MATH_AGENT_MODEL = os.getenv("MATH_AGENT_MODEL")

# math_agent_prompt = hub.pull("hwchase17/openai-functions-agent")

# tools = [
#     Tool(
#         name="Ortogonality",
#         func=math_vector_chain.invoke,
#         description="""Useful when you need to answer questions
#         about patient experiences, feelings, or any other qualitative
#         question that could be answered about a patient using semantic
#         search. Not useful for answering objective questions that involve
#         counting, percentages, aggregations, or listing facts. Use the
#         entire prompt as input to the tool. For instance, if the prompt is
#         "Are patients satisfied with their care?", the input should be
#         "Are patients satisfied with their care?".
#         """,
#     ), 
# ]


# chat_model = ChatOpenAI(
#     model=MATH_AGENT_MODEL,
#     temperature=0,
# )

# math_rag_agent = create_openai_functions_agent(
#     llm=chat_model,
#     prompt=math_agent_prompt,
#     tools=tools,
# )

# math_rag_agent_executor = AgentExecutor(
#     agent=math_rag_agent,
#     tools=tools,
#     return_intermediate_steps=True,
#     verbose=True,
# )