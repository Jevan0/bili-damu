import asyncio
import logging
import queue
import threading

import pyttsx3

from config.Logger import Logger
from Listener import Listener
from model.Message import Message

enable_tts = False

# 全局 TTS 队列
tts_queue: "queue.Queue[str]" = queue.Queue()


import subprocess


def tts_worker():
    while True:
        msg = tts_queue.get()
        if msg is None:
            break
        try:
            subprocess.run(
                ["espeak-ng", "-v", "zh", "-s", "200", msg],
                check=False,
            )
        except Exception as e:
            logging.error(f"TTS 播报失败: {e}")
        finally:
            tts_queue.task_done()


async def main(func, url_room_id: int):
    maestro = Listener(url_room_id)
    maestro.init_room()
    await asyncio.gather(maestro.connect(), maestro.consume(func))


def handle(message: Message):
    msg = f"{message.username[:1]}说{message.message}"
    logging.info(msg)
    if enable_tts:
        tts_queue.put(msg)  # 只丢进队列，不再开线程


if __name__ == "__main__":
    Logger.init_logger()

    room_id = 1805595700
    enable_tts = True

    # 启动 TTS worker（只启一次）
    threading.Thread(target=tts_worker, daemon=True).start()

    asyncio.run(main(handle, room_id))
