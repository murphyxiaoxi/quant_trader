from abc import ABCMeta, abstractmethod
from typing import List

from pandas import DataFrame


class CommonDataHandler(metaclass=ABCMeta):
    def __init__(self, data_frame: DataFrame, cols_name: List[str]):
        """

        :param data_frame: pandas dataFrame
        :param cols_name: 待获取列名称
        :param symbol_list: 标的代号
        """
        self.data_frame = data_frame
        self.cols_name: List[str] = cols_name

    @abstractmethod
    def get_latest_bar(self, symbol_code: str, date: str) -> DataFrame:
        pass
