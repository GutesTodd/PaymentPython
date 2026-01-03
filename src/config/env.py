import sys

from environs import Env

env = Env()
env.read_env() if 'pytest' not in sys.modules else env.read_env('.env.test')