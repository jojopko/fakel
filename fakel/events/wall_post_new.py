import textwrap
from logging import getLogger
from typing import List

from fakel.models import VKEventModel, PhotoModel
from fakel.telegram import TelegramBotService, TELEGRAM_SEND_MESSAGE_LIMIT, TELEGRAM_SEND_PHOTO_LIMIT

logger = getLogger(__name__)

ATTACHMENTS_AVAIBLE_TYPES = {'photo'}


async def _make_message_with_image(message: VKEventModel, photos: List[PhotoModel], use_hack=True):
    """Отправляет одно сообщение с картинкой"""
    if not photos:
        return

    photo = photos[0].sizes[0].url  # FIXME Придумать алгоритм выбора наибольшего размера

    if use_hack:
        text = textwrap.fill(message.object.text, width=TELEGRAM_SEND_MESSAGE_LIMIT, max_lines=1, placeholder='')
        await TelegramBotService().send_message(text, pic_url=photo)
    else:
        text = textwrap.fill(message.object.text, width=TELEGRAM_SEND_PHOTO_LIMIT, max_lines=1, placeholder='')
        await TelegramBotService().send_photo(photo, caption=text)


async def _make_messages_without_images(message: VKEventModel):
    """Отправляет сообщение без кортинки"""
    batches = textwrap.wrap(message.object.text, width=TELEGRAM_SEND_MESSAGE_LIMIT, replace_whitespace=False)
    for batch in batches:
        await TelegramBotService().send_message(batch)


async def wall_post_new_handler(message: VKEventModel):
    """Обработка события `wall_post_new`"""
    photos = [
        att.photo
        for att in message.object.attachments
        if att.type in ATTACHMENTS_AVAIBLE_TYPES
    ]

    await _make_message_with_image(message, photos)
    await _make_messages_without_images(message)
