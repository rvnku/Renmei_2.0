from bot import Renmei
from core.logging import setup_logging
from dotenv import load_dotenv
import os


def main():
    setup_logging()
    load_dotenv(os.getenv('DOTENV_FILE', '.env'))
    client = Renmei()
    client.run(token=os.getenv('TOKEN'))


if __name__ == '__main__':
    main()
