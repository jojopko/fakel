import uvicorn
from logging import DEBUG, WARNING

from fakel.const import DEBUG_MODE, MAX_WORKERS

if __name__ == '__main__':
    if not DEBUG_MODE:
        uvicorn.run('fakel.app:app', host='0.0.0.0', port=8000,
                    workers=MAX_WORKERS,
                    log_level=WARNING)
    else:
        uvicorn.run('fakel.app:app', host='0.0.0.0', port=8000,
                    workers=MAX_WORKERS,
                    log_level=DEBUG,
                    reload=True)
