from structures.link.chat_link import ChatLink
from structures.link.links_handler import ChatLinksHandler
from structures.link.chats.topic import GroupTopic
import asyncio

asyncio.run(ChatLinksHandler.restore())
