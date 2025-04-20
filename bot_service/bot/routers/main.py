from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

main_routesr = Router(name="main")


@main_routesr.message(CommandStart())
async def start(message: Message) -> None:
    await message.bot.send_message(message.chat.id, "да ну наху")


@main_routesr.message(Command("/help"))
async def helpme(message: Message) -> None:
    raise NotImplementedError


@main_routesr.message(CommandStart(deep_link=True))
async def deeplink(message: Message) -> None:
    raise NotImplementedError
