from langgraph.graph import END , StateGraph
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from typing_extensions import TypedDict
from langchain_core.chat_history import BaseChatMessageHistory
import streamlit as st
from dotenv import load_dotenv

st.title("Medical assisant via LangGraph")


st.markdown(
    """
    <style>
    body {
        color: blue;  /* Change the font color to blue */
        font-size: 24px;  /* Change the font size to 24px */
        background-color: lightyellow; /* Change the background color to light yellow */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 



load_dotenv()

llm = ChatOpenAI(temperature=0,openai_api_key="")

class ChatMessageHistory(BaseChatMessageHistory):
    def __init__(self):
        self.messages = []

    def clear(self):
        self.messages = []

    def add_user_message(self, message):
        self.messages.append(message)

    def add_ai_message(self, message):
        self.messages.append(message)

his = ChatMessageHistory()
wrapper = DuckDuckGoSearchAPIWrapper(max_results=10)
web_search_tool = DuckDuckGoSearchRun(api_wrapper=wrapper)


chain_prompt = PromptTemplate(
    template="""
Answer the following questions as best you can, but speaking as compasionate medical professional.

You are provided with three inputs:
1. First input is the context that might help you answer the user query. This context is a compilation of detailed length answers from a web search , you might not necarirly need it but make use of it where required.
2. A brief chat history of the user with you , use it where necassry.
3. The inputted user query.


Begin! Remember to speak as a compasionate medical professional when giving your final answer. If the condition is serious advise they speak to a doctor.

Previous conversation history:
{history}

New question: {query}
Context from web search {context}""",
input_variables=['query','context','history']
)

query_chain = chain_prompt | llm | StrOutputParser()



class GraphState(TypedDict):
    query: str
    history: str=""
    context: str
    
def web_search(state):
    search_query = state['query']
    search_result = web_search_tool.invoke(search_query)
    print("searching the web")
    return {"context": search_result}

def get_reply(state):
    context = state['context']
    query = state['query']
    hist = state['history']
    res = query_chain.invoke({"query": query,"context":context,"history":hist})
    his.add_user_message(message=query)
    his.add_ai_message(message=res)
    state['history']=his.messages
    st.write(res)


workflow = StateGraph(GraphState)
workflow.add_node("websearch", web_search)
workflow.add_node("generate reply",get_reply)
workflow.set_entry_point("websearch")

workflow.add_edge("websearch","generate reply")
workflow.add_edge("generate reply", END)

agent = workflow.compile()

user_input = st.text_area(placeholder='How to deal with a sprained knee',label='Describe issue here')

initial_state = {
    'query': "How to deal with sprained knee",
    'history': "",
    'context': ""
}

final_state = agent.invoke(initial_state)
