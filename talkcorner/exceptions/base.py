from typing import Union, Dict, Any


class BaseAppException(Exception):

    @property
    def detail(self) -> Union[str, Dict[str, Any]]:
        raise NotImplementedError
