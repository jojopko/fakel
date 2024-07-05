import asyncio
from asyncio import Queue
from logging import getLogger
from typing import Optional

from fakel.models import VKEventModel
from fakel.telegram import TelegramBotService
from fakel.utils import batched

logger = getLogger(__name__)

telegram: Optional[TelegramBotService] = None

TELEGRAM_SEND_MESSAGE_LIMIT = 4096


async def _wall_post_new_handler(message: VKEventModel):
    """Обработка события `wall_post_new`"""
    try:
        if len(message.object.text) > TELEGRAM_SEND_MESSAGE_LIMIT:
            text_patitions = [''.join(part) for part in batched(message.object.text, TELEGRAM_SEND_MESSAGE_LIMIT)]
        else:
            text_patitions = [message.object.text]

        logger.debug('Части текста:\n%s', text_patitions)

        for part in text_patitions:
            await telegram.send_message(part)
    except Exception as e:
        logger.warning('Ошибка при обработке сообщения', exc_info=e)
    except BaseException as be:
        logger.warning('Ошибка при обработке сообщения', exc_info=be)


async def _do_work(message: VKEventModel):
    logger.debug('Сообщение: %s', message.model_dump_json())
    logger.info('Обработка сообщения %s', message.event_id)
    if message.type == 'wall_post_new':
        await _wall_post_new_handler(message)
    else:
        logger.warning('Сообщение %s не обработано! Тип: %s', message.event_id, message.type)


async def message_worker(queue: Queue):
    global telegram
    telegram = TelegramBotService()
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
