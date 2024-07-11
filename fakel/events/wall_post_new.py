import textwrap
from logging import getLogger
from typing import List

from fakel.models import VKEventModel, PhotoModel
from fakel.telegram import TelegramBotService, TELEGRAM_SEND_MESSAGE_LIMIT, TELEGRAM_SEND_PHOTO_LIMIT

logger = getLogger(__name__)

ATTACHMENTS_AVAIBLE_TYPES = {'photo'}


async def _make_message_with_image(message_full_text: str, photos: List[PhotoModel], use_hack=True):
    """Отправляет одно сообщение с картинкой"""
    if not photos:
        return

    photo = photos[0].sizes[0].url  # FIXME Придумать алгоритм выбора наибольшего размера

    if use_hack:
        batches = textwrap.wrap(message_full_text, width=TELEGRAM_SEND_MESSAGE_LIMIT, break_long_words=False,
                                replace_whitespace=False)
        await TelegramBotService().send_message(batches[0], pic_url=photo)
        for batch in batches[1:]:
            await TelegramBotService().send_message(batch)
    else:
        text = textwrap.fill(message_full_text, width=TELEGRAM_SEND_PHOTO_LIMIT, max_lines=1, placeholder='')
        await TelegramBotService().send_photo(photo, caption=text)


async def _make_messages_without_images(message_full_text: str):
    """Отправляет сообщение без кортинки"""
    batches = textwrap.wrap(message_full_text, width=TELEGRAM_SEND_MESSAGE_LIMIT, break_long_words=False,
                            replace_whitespace=False)
    for batch in batches:
        await TelegramBotService().send_message(batch)


async def wall_post_new_handler(message: VKEventModel):
    """Обработка события `wall_post_new`"""

    if message.object.copy_history:
        # Если запись была репостнута, эта запись будет в массиве copy_history
        text = message.object.copy_history[0].text
        attachments = message.object.copy_history[0].attachments
    else:
        text = message.object.text
        attachments = message.object.attachments

    photos = [
        att.photo
        for att in attachments
        if att.type in ATTACHMENTS_AVAIBLE_TYPES
    ]

    if photos:
        await _make_message_with_image(text, photos)
    else:
        await _make_messages_without_images(text)
