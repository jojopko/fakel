import textwrap
from logging import getLogger
from typing import List

from fakel.models import VKEventModel, PhotoModel, AttachmentModel, PhotoSizeModel
from fakel.utils.telegram import TelegramBotService, TELEGRAM_SEND_MESSAGE_LIMIT, TELEGRAM_SEND_PHOTO_LIMIT

logger = getLogger(__name__)

ATTACHMENTS_AVAIBLE_TYPES = {'photo'}

ATTACHMENTS_PHOTO_TYPE = 'photo'


def _get_best_photo(photo: PhotoModel) -> PhotoSizeModel:
    max_res = 0
    max_size = None
    for size in photo.sizes:
        res = size.width * size.height
        if res > max_res:
            max_res = res
            max_size = size
    return max_size


def _get_only_photo_from_attachments(attachments: List[AttachmentModel]) -> List[PhotoModel]:
    return [
        att.photo
        for att in attachments
        if att.type == ATTACHMENTS_PHOTO_TYPE
    ]


async def _make_message_with_image(message_full_text: str, photos: List[PhotoModel], use_hack=True):
    """Отправляет одно сообщение с картинкой"""
    if not photos:
        return

    photo = _get_best_photo(photos[0])

    if use_hack:
        batches = textwrap.wrap(message_full_text, width=TELEGRAM_SEND_MESSAGE_LIMIT, break_long_words=False,
                                replace_whitespace=False)
        await TelegramBotService().send_message(batches[0], pic_url=photo.url)
        for batch in batches[1:]:
            await TelegramBotService().send_message(batch)
    else:
        text = textwrap.fill(message_full_text, width=TELEGRAM_SEND_PHOTO_LIMIT, max_lines=1, placeholder='')
        await TelegramBotService().send_photo(photo.url, caption=text)


async def _make_messages_without_images(message_full_text: str):
    """Отправляет сообщение без кортинки"""
    batches = textwrap.wrap(message_full_text, width=TELEGRAM_SEND_MESSAGE_LIMIT, break_long_words=False,
                            replace_whitespace=False)
    for batch in batches:
        await TelegramBotService().send_message(batch)


async def wall_post_new_handler(message: VKEventModel):
    """Обработка события `wall_post_new`"""
    message_object = message.object.get_preferred_object()
    text = message_object.text
    attachments = message_object.attachments

    photos = _get_only_photo_from_attachments(attachments)

    if photos:
        await _make_message_with_image(text, photos)
    else:
        await _make_messages_without_images(text)
