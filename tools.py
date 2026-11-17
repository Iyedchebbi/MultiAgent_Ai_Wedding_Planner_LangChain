from langchain.tools import tool
from tavily import TavilyClient
from dotenv import load_dotenv
import logging 

# configure my logging

logging.basicConfig(
    level=logging.INFO,
    format= '%(asctime)s | %(levelname)s | %(message)s'
)

load_dotenv()
TavilyClient = TavilyClient()

@tool
def search_web(topic : str) -> str:
    """search the web for a given topic and returns the results."""
    logging.info(f"Searching the web for topic :{topic}")
    return  TavilyClient.search(topic)
    
    

