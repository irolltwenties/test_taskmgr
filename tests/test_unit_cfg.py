from config.cfg import Configuration


def test_config_loading():
    config = Configuration()  # config does not throw an err on init
