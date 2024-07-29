from structures.link.chat_link import ChatLink
from structures.link.links_handler import ChatLinksHandler
import asyncio

asyncio.run(ChatLinksHandler.restore())
