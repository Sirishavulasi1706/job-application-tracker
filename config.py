import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "this_is_a_secret_key"