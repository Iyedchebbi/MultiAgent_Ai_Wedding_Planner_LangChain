from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

llm_model = init_chat_model(
    "nvidia/nemotron-3-ultra-550b-a55b:free",
    model_provider="openrouter"
)

#result = llm_model.invoke("capital of tunisia, answer in 2 lines ")
#print(result.content)

