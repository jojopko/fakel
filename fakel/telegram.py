import json
from typing import Optional

import httpx
from logging import getLogger

from fakel.const import TG_BOT_TOKEN, TG_CHANNEL_NAME, TELEGRAM_SEND_BLOCK

logger = getLogger(__name__)

TELEGRAM_SEND_PHOTO_LIMIT = 1024
TELEGRAM_SEND_MESSAGE_LIMIT = 4096


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

    async def send_message(self, text: str, pic_url: Optional[str] = None):
        """Отправка текстового сообщения"""
        if self._is_block:
            return

        if not text:
            logger.warning('Сообщение пустое!')
            raise ValueError('Текст не может быть пустым!')

        if len(text) > TELEGRAM_SEND_MESSAGE_LIMIT:
            logger.warning('Больше допустимого значения! Лимит: %s. Текущее: %s',
                           TELEGRAM_SEND_MESSAGE_LIMIT, len(text))
            raise ValueError('Сообщение слишком большое')

        # Документация https://core.telegram.org/bots/api#sendmessage
        async with httpx.AsyncClient() as client:
            if pic_url:
                data = {
                    'chat_id': '@%s' % TG_CHANNEL_NAME,
                    'text': text,
                    'link_preview_options': json.dumps({
                        'is_disabled': False,
                        'url': pic_url,
                        'prefer_small_media': False,
                        'prefer_large_media': True,
                        'show_above_text': True
                    })
                }
            else:
                data = {
                    'chat_id': '@%s' % TG_CHANNEL_NAME,
                    'text': text
                }

            logger.debug('REQUEST DATA: %s', data)

            response = await client.post(
                f'{self._BASE_URL}/sendMessage',
                data=data
            )

        result = response.json()
        logger.debug('Ответ от api.telegram.org: %s', result)

        if not result['ok']:
            logger.warning('Ошибка при обработке запроса к api.telegram.org: %s', result)

    async def send_photo(self, photo_url: str, caption: str):
        """Отправка сообщения с фотографией"""
        if self._is_block:
            return

        if len(caption) > TELEGRAM_SEND_PHOTO_LIMIT:
            logger.warning('Больше допустимого значения! Лимит: %s. Текущее: %s',
                           TELEGRAM_SEND_PHOTO_LIMIT, len(caption))
            raise ValueError('Сообщение слишком большое')

        if not photo_url:
            logger.warning('Нет фотографии!')
            raise ValueError('Нет фотографии')

        # Документация https://core.telegram.org/bots/api#sendphoto
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f'{self._BASE_URL}/sendPhoto',
                data={
                    'chat_id': '@%s' % TG_CHANNEL_NAME,
                    'photo': photo_url,
                    'caption': caption
                }
            )
        result = response.json()
        logger.debug('Ответ от api.telegram.org: %s', result)

        if not result['ok']:
            logger.warning('Ошибка при обработке запроса к api.telegram.org: %s', result)
