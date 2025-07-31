from typing import TYPE_CHECKING

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

if TYPE_CHECKING:
    from bot.base.bot import ITSBot

main_router = Router(name="main")


@main_router.message(CommandStart())
async def start(message: Message) -> None:
    bot: ITSBot = message.bot

    welcome_text = (
        "👋 Приветствую в новостном боте МГТУ им. Н.Э. Баумана!\n\n"
        "Я буду присылать тебе свежие новости, анонсы мероприятий и важные объявления "  # noqa: E501
        "из нашего университета. Оставайся в курсе всех событий!\n\n"
        "Используй команду /help, чтобы узнать доступные возможности."
    )
    await message.answer(welcome_text)


@main_router.message(Command("help"))
async def helpme(message: Message) -> None:
    help_text = (
        "ℹ️ Доступные команды:\n\n"
        "/start - начать работу с ботом\n"
        "/help - получить справку\n"
        "/subscribe - подписаться на рассылку\n"
        "/unsubscribe - отписаться от рассылки\n"
        "/categories - выбрать интересующие категории новостей\n\n"
        "Ступино 🫶"
    )
    await message.answer(help_text)


@main_router.message(CommandStart(deep_link=True))
async def deeplink(message: Message) -> None:
    deep_link_text = "🔗 Вы перешли по специальной ссылке!\n\n"
    await message.answer(deep_link_text)
