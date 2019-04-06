import abc
from typing import List

from core.common.event import MarketEvent, OrderEvent
from dao.stock_data import StockXueqiuData


class StrategyTemplate(metaclass=abc.ABCMeta):
    def __init__(self, symbols: List[str],
                 init_capital: float,
                 back_test=True,
                 start_date=None,
                 end_date=None,
                 clock_event_queue=None,
                 market_event_queue=None):
        """

        :param symbols:
        :param init_capital:
        :param back_test:
        :param start_date:
        :param end_date:
        """
        self.__symbols = symbols
        self.__init_capital = init_capital
        self.__back_test = back_test
        self.__start_date = start_date
        self.__end_date = end_date
        self.__portfolio = None
        self.__clock_event_queue = clock_event_queue
        self.__market_event_queue = market_event_queue
        self.stock_api = StockXueqiuData()
        self.init()

    @property
    def symbols(self):
        return self.__symbols

    @property
    def init_capital(self):
        return self.__init_capital

    @property
    def back_test(self):
        return self.__back_test

    @property
    def start_date(self):
        return self.__start_date

    @property
    def end_date(self):
        return self.__end_date

    @property
    def portfolio(self):
        return self.__portfolio

    @portfolio.setter
    def portfolio(self, value):
        if self.__portfolio is None:
            self.__portfolio = value

    @property
    def clock_event_queue(self):
        return self.__clock_event_queue

    @clock_event_queue.setter
    def clock_event_queue(self, value):
        if self.__clock_event_queue is None:
            self.__clock_event_queue = value

    @property
    def market_event_queue(self):
        return self.__market_event_queue

    @market_event_queue.setter
    def market_event_queue(self, value):
        if self.__market_event_queue is None:
            self.__market_event_queue = value

    @abc.abstractmethod
    def init(self):
        # 进行相关的初始化操作
        raise NotImplementedError()

    @abc.abstractmethod
    def id(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def name(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def description(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def market_data_func(self, current_date: str):
        raise NotImplementedError()

    @abc.abstractmethod
    def strategy(self, event: MarketEvent) -> OrderEvent:
        """:param event event.data 为所有股票的信息，结构如下
        {'162411':
        {'ask1': '0.493',
         'ask1_volume': '75500',
         'ask2': '0.494',
         'ask2_volume': '7699281',
         'ask3': '0.495',
         'ask3_volume': '2262666',
         'ask4': '0.496',
         'ask4_volume': '1579300',
         'ask5': '0.497',
         'ask5_volume': '901600',
         'bid1': '0.492',
         'bid1_volume': '10765200',
         'bid2': '0.491',
         'bid2_volume': '9031600',
         'bid3': '0.490',
         'bid3_volume': '16784100',
         'bid4': '0.489',
         'bid4_volume': '10049000',
         'bid5': '0.488',
         'bid5_volume': '3572800',
         'buy': '0.492',
         'close': '0.499',
         'high': '0.494',
         'low': '0.489',
         'name': '华宝油气',
         'now': '0.493',
         'open': '0.490',
         'sell': '0.493',
         'turnover': '420004912',
         'volume': '206390073.351'}}
        """
        raise NotImplementedError()

    def run(self, event) -> OrderEvent:
        return self.strategy(event)


if __name__ == '__main__':
    class Test:
        def func(self, str):
            return str


    test = Test()
    f = test.func
    print(f("xiaoxi"))
