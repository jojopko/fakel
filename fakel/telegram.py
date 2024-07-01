import httpx
from logging import getLogger

from fakel.const import TG_BOT_TOKEN, TG_CHANNEL_NAME

logger = getLogger(__name__)


async def send_message(text: str):
    """Отправка текстового сообщения"""
    if not text:
        raise ValueError('Текст не может быть пустым!')

    # Документация https://core.telegram.org/bots/api#sendmessage
    async with httpx.AsyncClient() as client:
        result = await client.post(
            'https://api.telegram.org/bot%s/sendMessage' % TG_BOT_TOKEN,
            data={
                'chat_id': '@%s' % TG_CHANNEL_NAME,
                'text': text
            }
        )
    logger.debug('Ответ от api.telegram.org: %s', result.json())


