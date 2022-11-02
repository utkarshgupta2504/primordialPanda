from os import environ


class globaldata:
    isTesting = environ["BOT_ENV"] == "development"
