import asyncio
from asyncio import Queue
from logging import getLogger

from fakel.models import VKEventModel
from fakel.events import wall_post_new_handler

logger = getLogger(__name__)


async def _do_work(message: VKEventModel):
    logger.info('Обработка сообщения %s', message.event_id)
    logger.debug('Сообщение: %s', message.model_dump_json())

    try:
        if message.type == 'wall_post_new':
            await wall_post_new_handler(message)
        else:
            logger.warning('Сообщение %s не обработано! Тип: %s', message.event_id, message.type)
    except (Exception, BaseException) as e:
        raise e


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
