import uvicorn

from app.core import App
from config.cfg import Configuration


def main():
    configuration = Configuration()
    uvicorn.run(
        App(configuration).app, host=configuration.host, port=int(configuration.port)
    )


if __name__ == "__main__":
    main()
