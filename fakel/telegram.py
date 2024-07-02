import httpx
from logging import getLogger

from fakel.const import TG_BOT_TOKEN, TG_CHANNEL_NAME, TELEGRAM_SEND_BLOCK

logger = getLogger(__name__)


class TelegramBotService:
    _instance = None
    _BASE_URL = 'https://api.telegram.org/bot%s' % TG_BOT_TOKEN

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(TelegramBotService, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._is_block = TELEGRAM_SEND_BLOCK
            if self._is_block:
                logger.warning('Включена блокировка сообщений в telegram')
            self._initialized = True

    async def send_message(self, text: str):
        """Отправка текстового сообщения"""
        if self._is_block:
            return

        if not text:
            raise ValueError('Текст не может быть пустым!')

        # Документация https://core.telegram.org/bots/api#sendmessage
        async with httpx.AsyncClient() as client:
            result = await client.post(
                f'{self._BASE_URL}/sendMessage',
                data={
                    'chat_id': '@%s' % TG_CHANNEL_NAME,
                    'text': text
                }
            )
        logger.debug('Ответ от api.telegram.org: %s', result.json())
