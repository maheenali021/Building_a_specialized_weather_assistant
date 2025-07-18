from agents import Runner,Agent
from openai.types.responses import ResponseTextDeltaEvent
from dotenv import load_dotenv
from config import configration
from get_weather import  get_weather_info
import chainlit as cl


load_dotenv()

weather_agent = Agent(
    name= "Weather_assistant",
    instructions= "you can give the current weather information to use the get_weather_info tool",
   tools=[get_weather_info]
)

@cl.on_chat_start
async def handle_start_chat():
    cl.user_session.set("history", [])
    await cl.Message(content="Hello! How can I assist you today?").send()

@cl.on_message
async def on_message(message: cl.Message):
    history = cl.user_session.get("history", [])  
    msg = cl.Message(content="")
    await msg.send()

    history.append({"role": "user", "content": message.content}) 
 
    result = Runner.run_streamed(
        weather_agent,
        input=history, 
        run_config=configration  
    )

    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            await msg.stream_token(event.data.delta)

    if result.final_output:  
        history.append({"role": "assistant", "content": result.final_output}) 
    
    cl.user_session.set("history", history)