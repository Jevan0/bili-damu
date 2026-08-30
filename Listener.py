import logging
from typing import Self
import asyncio
from collections import deque
from bilibili_api import live, select_client, get_selected_client, get_registered_clients

from model.Message import Message


class Listener:

    def __init__(self, room_id: int):
        self.room_id = room_id
        self.room = None
        self.message_queue = deque(maxlen=100)
        select_client("aiohttp")

    def __set_room_listener(self) -> Self:
        room = self.room

        @room.on("ALL")
        async def on_all(event):
            if event['type'] == 'DANMU_MSG':
                info = event["data"]["info"]
                self.message_queue.append(Message(info[2][1], info[1]))

        return self

    def init_room(self) -> Self:
        self.room = live.LiveDanmaku(self.room_id)
        self.__set_room_listener()
        return self

    def change_room_by_id(self, room_id: int) -> Self:
        self.room_id = room_id
        self.init_room()
        return self

    async def connect(self):
        if self.room is None:
            raise RuntimeError("room not initialized, call init_room() first")

        room = self.room
        try:
            await room.connect()
            logging.info("已连接到直播间，开始监听弹幕...")

            while True:
                await asyncio.sleep(1)

        except KeyboardInterrupt:
            logging.info("\n正在断开连接...")
            await room.disconnect()
            logging.info("已断开连接")

    async def consume(self,handler):
        while True:
            if not self.message_queue:
                await asyncio.sleep(0.05)
                continue

            message = self.message_queue.popleft()
            handler(message)
