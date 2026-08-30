import asyncio
import logging
import pyttsx3
import threading

from Listener import Listener
from config.Logger import Logger
from model.Message import Message

enable_tts = False
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[17].id)

async def main(func, url_room_id: int):
    maestro = Listener(url_room_id)
    maestro.init_room()
    await asyncio.gather(maestro.connect(), maestro.consume(func))

def tts(msg:str):
    engine.setProperty('rate', 200)
    engine.setProperty('volume', 0.7)
    engine.say(msg)
    engine.runAndWait()

# this function defined how to handle the message of danmu 
def handle(message: Message):
    msg = f"{message.username[:1]}说{message.message}"
    logging.info(msg)

    # tts speak 
    if enable_tts:
        threading.Thread(
            target=tts,
            args=(msg,),
            daemon=True
        ).start()


if __name__ == "__main__":
    Logger.init_logger()

    # 直播间监听
    room_id = 1764821878
    enable_tts = True

    asyncio.run(main(handle, room_id))
