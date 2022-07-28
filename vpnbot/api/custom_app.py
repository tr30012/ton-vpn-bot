
from aiogram import Bot
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine


class BotFastAPI(FastAPI):
    engine: AsyncEngine
    bot: Bot
