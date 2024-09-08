import random
from utils.logging_tool.log_control import WARNING, ERROR
import re
from typing import Union, List, Dict
import ast
from utils.read_files_tools.regular_control import cache_regular
from utils.mysql_tool.mysql_control import MysqlDB


class CustomFunc:
    """
    customfunc for setup_func
    """
    def __init__(self) -> None:
        pass


    @classmethod
    def random_int(cls) -> int:
        """
        :return: random int
        """
        _data = random.randint(0, 5000)
        return _data
    

    @classmethod
    def query_test(cls, id) -> dict:
        sql = f'select * from user where id = {id}'

        data = MysqlDB().query(sql)[0]

        return data


    def setup_func_data(self, func: Union[List, None]) -> Dict:

        func = ast.literal_eval(cache_regular(str(func)))

        try:
            data = {}
            if func is not None:
                for f in func:
                    func_name = f.split("(")[0]
                    value_name = f.split("(")[1][:-1]
                    if value_name == "":
                        value_data = getattr(CustomFunc(), func_name)()
                    else:
                        value_data = getattr(CustomFunc(), func_name)(*value_name.split(","))
                    
                    data[func_name] = value_data

            return data
        except Exception as e:
            ERROR.logger.error("func execute failed!!")
            raise e


