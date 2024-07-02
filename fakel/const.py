import os

# NOTE!
# На сервис не ожидается большой нагрузки, поэтому обработка сообщений и веб сервер в одном потоке.
# В случае измения требований: испльзовать внешнюю очередь (Redis, AMQP) или руками через `multiprocessing.Queue`
MAX_WORKERS = 1

DEBUG_MODE = os.getenv('DEBUG_MODE', 'false').lower() == 'true'

TELEGRAM_SEND_BLOCK = os.getenv('TELEGRAM_SEND_BLOCK', 'false').lower() == 'true'

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN', '')

VK_GROUP_ID = int(os.getenv('VK_GROUP_ID', -1))

SUPPORT_API_VERSION = '5.199'

TG_BOT_TOKEN = os.getenv('TG_BOT_TOKEN', '')

TG_CHANNEL_NAME = os.getenv('TG_CHANNEL_NAME', '')
TG_CHANNEL_NAME = int(TG_CHANNEL_NAME) if TG_CHANNEL_NAME.isnumeric() else TG_CHANNEL_NAME

BOT_ADMIN_TELEGRAM_IDS = os.getenv('BOT_ADMIN_TELEGRAM_IDS', '')
BOT_ADMIN_TELEGRAM_IDS = [int(admin_id) for admin_id in BOT_ADMIN_TELEGRAM_IDS.split(',')]
