from pathlib import Path


AUTO_EXTEND = False
FALLBACK_ERROR_FORMAT = 'json'
INSTALLED_APPS = [
    'convert'
]

MIDDLEWARES = {
    'request': [],
    'response': []
}

NOISY_EXCEPTIONS = True
ROOT = Path(__file__).resolve().parent.parent
