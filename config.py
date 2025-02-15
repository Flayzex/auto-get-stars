from decouple import config

class Config:
    API_ID = config('API_ID')
    API_HASH = config('API_HASH')
