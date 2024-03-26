import os

from dotenv import load_dotenv

load_dotenv()


def init_url(env_key):
    if os.getenv(env_key) is None:
        raise Exception(f"'{env_key}' is not existed")
    if os.getenv('test_env') is None:
        raise Exception(f"test_env is not existed")
    return os.getenv(env_key).replace('{test_env}',
                                      os.getenv('test_env'))
