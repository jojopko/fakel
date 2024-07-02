import asyncio
from asyncio import Queue
from logging import getLogger

from fakel.models import VKEventModel
from fakel.telegram import send_message

logger = getLogger(__name__)


async def wall_post_new_handler(message: VKEventModel):
    """Обработка события `wall_post_new`"""
    text = message.object.text
    await send_message(text)


async def _do_work(message: VKEventModel):
    logger.debug('Обработка сообщения %s', message.model_dump_json())
    if message.type == 'wall_post_new':
        await wall_post_new_handler(message)


async def message_worker(queue: Queue):
    logger.info('Обработчик сообщений запущен')
    while True:
        try:
            message = await queue.get()
            await _do_work(message)
        except asyncio.CancelledError:
            logger.info('Остановка обработчика событий')
        except Exception as e:
            logger.warning('Ошибка обработчика сообщений', exc_info=e)
        except BaseException as be:
            logger.warning('Ошибка обработчика сообщений', exc_info=be)


