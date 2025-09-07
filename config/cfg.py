from os import getenv


class Configuration:
    def __init__(self):
        self.__task_mgr_db_login = getenv("TASK_MGR_DB_LOGIN")
        self.__task_mgr_db_password = getenv("TASK_MGR_DB_PASSWORD")
        self.__task_mgr_db_name = getenv("TASK_MGR_DB_NAME")
        self.__task_mgr_db_host = getenv("TASK_MGR_DB_HOST")
        self.__task_mgr_db_port = getenv("TASK_MGR_DB_PORT")
        self._task_mgr_bearer = getenv("TASK_MGR_BEARER")
        self.__port = getenv("TASK_MGR_PORT")
        self.__host = getenv("TASK_MGR_HOST")

        for name, val in self.__dict__.items():
            if val == "":
                raise ValueError(f"Missing config for {name[1:]}")

    @property
    def db_login(self):
        return self.__task_mgr_db_login

    @property
    def db_password(self):
        return self.__task_mgr_db_password

    @property
    def db_name(self):
        return self.__task_mgr_db_name

    @property
    def db_host(self):
        return self.__task_mgr_db_host

    @property
    def db_port(self):
        return self.__task_mgr_db_port

    @property
    def task_mgr_bearer(self):
        return self._task_mgr_bearer

    @property
    def host(self):
        return self.__host

    @property
    def port(self):
        return self.__port
