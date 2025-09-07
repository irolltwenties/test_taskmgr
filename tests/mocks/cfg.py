from config.cfg import Configuration


class FakeConfiguration(Configuration):
    def __init__(self):
        self.__task_mgr_db_login = "dev"
        self.__task_mgr_db_password = "dev"
        self.__task_mgr_db_name = "dev"
        self.__task_mgr_db_host = "localhost"
        self.__task_mgr_db_port = "5432"
        self._task_mgr_bearer = "test"
        self.__port = "8000"
        self.__host = "0.0.0.0"
