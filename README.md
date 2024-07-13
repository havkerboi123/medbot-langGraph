


# MedBot

LangGraph based memory capable web-search tool that assists with medical related queries.

## Technical details

Project utilizes LangGraph and LangChain to manage its workflow and process user inputs efficiently. 

Upon receiving a query from the user, the bot conducts a web search using DuckDuckGo's API, retrieving detailed information to aid in answering the query. The bot's language model, powered by OpenAI's LLM , integrates the retrieved web context and previous chat history to generate a compassionate and professional response. 

A custom StateGraph from LangGraph orchestrates the workflow, ensuring the correct sequence of operations, from web search to response generation. Additionally, the bot's interface, created with Streamlit, includes custom styling to enhance user experience. 

The architecture leverages a combination of tools such as LangChain, OpenAI, and DuckDuckGo to provide a seamless and reliable medical assistance service.


## LangGraph routing

The web-search with the user input query is initiated at the very beginning.
```python
workflow.set_entry_point("websearch")
```

This web search content along with chat history ( if available ) is sent to the next node in order to generate a reply :)

```python
workflow.add_node("websearch", web_search)
workflow.add_node("generate reply",get_reply)
```
The following initial GraphStates were set
```python
user_input = st.text_area(placeholder='How to deal with a sprained knee',label='Describe issue here')

initial_state = {
    'query': user_input,
    'history': "",
    'context': ""
}
```
## Libraries used

LangGraph
, LangChain , Streamlit


