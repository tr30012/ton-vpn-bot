from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.ext.asyncio import AsyncResult
from vpnbot.api.dependencies import connection_pool
from vpnbot.orm.schemas import users_table

router = APIRouter(prefix='/api')


@router.get('/health')
async def health():
    return {"response": "Hello, World!"}


@router.get('/users')
async def users(connection: AsyncConnection = Depends(connection_pool)):
    result: AsyncResult = await connection.execute(select(users_table))
    return result.all()
