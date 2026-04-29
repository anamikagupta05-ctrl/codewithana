from langchain.tools import tool
from langchain.messages import HumanMessage,SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchRun

# Define the tool
#@tool(description="Get the current weather in a given location")
#def get_weather(location: str) -> str:
 #   return "It's sunny."

@tool(description="Search the web using DuckDuckGo and load content from the first result")
def ddgs_search_and_load(query: str) -> str:
    """
    Searches the web using DuckDuckGo for the given query and attempts to load the content
    from the first search result. If content loading fails, it returns the search snippets.
 
    Args:
        query (str): The search query.
 
    Returns:
        str: The loaded web page content or search snippets if scraping fails.
    """
    print(f"\n--- Executing Tool: web_search_and_load for query: '{query}' ---")
    search = DuckDuckGoSearchRun()
    search_results = search.run(query)
 
    if not search_results:
        print("No search results found.")
        return "No relevant search results found."
 
    return search_results

query=input("Enter your query: ")

prompt= 'You are a helpful medical assistant and you need to answer the question based on the search result provided in brief. If the search result does not contain relevant information, answer based on your knowledge.'

# Initialize and bind (potentially multiple) tools to the model
model_with_tools = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", api_key="AIzaSyCJJZqH1IMuZaJD-mdQlvdXI4Smkf3B1G0").bind_tools([ddgs_search_and_load])

# Step 1: Model generates tool calls

messages = [
    SystemMessage(content=prompt),
    HumanMessage(query)]
ai_msg = model_with_tools.invoke(messages)

print(f"AI Message: {ai_msg.content[0]['text']}")

