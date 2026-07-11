from abc import ABC
import dotenv, os


dotenv.load_dotenv(os.getenv('DOTENV_FILE', '.env'))


class Env(ABC):
    token = os.getenv('TOKEN')
