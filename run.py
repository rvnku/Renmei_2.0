from bot import Renmei
from core.logging import setup_logging
from core.env import Env


def main():
    setup_logging()
    client = Renmei()
    client.run(token=Env.token)


if __name__ == '__main__':
    main()
