import os
from agents import  OpenAIChatCompletionsModel, RunConfig
from dotenv import load_dotenv
from openai import AsyncOpenAI
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

external_client=AsyncOpenAI(
   api_key = gemini_api_key,
   base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model= "gemini-2.0-flash",
    openai_client=external_client
)
configration= RunConfig(
    model= model,
    model_provider= external_client, 
    tracing_disabled=True
)
