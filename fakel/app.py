import asyncio
import os
from contextlib import asynccontextmanager
from logging import getLogger, Logger
from typing import Optional

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

from fakel.const import ACCESS_TOKEN, VK_GROUP_ID, SUPPORT_API_VERSION
from fakel.logger import init_logger
from fakel.message_worker import message_worker
from fakel.models import VKEventModel

logger: Optional[Logger] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global logger
    init_logger()
    logger = getLogger(__name__)
    logger.info('Переменные среды:\n%s', '\n'.join([f'{k}={v}' for k, v in os.environ.items()]))

    loop = asyncio.get_running_loop()
    message_worker_task = loop.create_task(message_worker(messages_queque), name='message_worker')
    yield


app = FastAPI(lifespan=lifespan)

messages_queque = asyncio.Queue()


@app.get('/')
async def health_check():
    return 'hello!'


async def confirmation():
    """Обработка события `confirmation`"""
    import httpx
    async with httpx.AsyncClient() as client:
        result = await client.post(
            'https://api.vk.com/method/groups.getCallbackConfirmationCode?group_id=%s&v=%s' % (
                VK_GROUP_ID, SUPPORT_API_VERSION
            ),
            headers={
                'Authorization': 'Bearer %s' % ACCESS_TOKEN
            }
        )
    logger.debug('Ответ api.vk.com getCallbackConfirmationCode: %s', result.json())
    return result.json()['response']['code']


@app.post('/', response_class=PlainTextResponse)
async def handle(update_data: VKEventModel):
    """Обработка событий из VK API. Подробнее: https://dev.vk.com/ru/api/callback/getting-started"""
    try:
        logger.info("Получено сообщение от VK: %s", update_data.event_id)
        if update_data.type == 'confirmation':
            return await confirmation()
        await messages_queque.put(update_data)
    except Exception as e:
        logger.warning('Ошибка при получении события', exc_info=e)
    except BaseException as be:
        logger.warning('Ошибка при получении события', exc_info=be)
    return 'ok'
