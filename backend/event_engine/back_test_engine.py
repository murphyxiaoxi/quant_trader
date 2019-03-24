#!/usr/bin/python
# -*- coding: utf-8 -*-

import queue
import time
from datetime import datetime
from typing import List, Dict, Set

from backend.commons.abstract_strategy import AbstractStrategy
from backend.commons.data_handlers.abstract_handler import CommonDataHandler
from backend.commons.enums.event_type_enums import EventTypeEnum
from backend.commons.events.base import AbstractEvent, MarketEvent
from backend.commons.order_execution.order_execute_handler import AbstractOrderExecuteHandler, \
    SimulatedOrderExecuteHandler
from backend.commons.portfolios.base import Portfolio


class BackTestEngine(object):
    # todo 完善
    """
    事件驱动型回测框架
    """

    def __init__(self, symbol_list: List[str], initial_capital: float, start_date: str,
                 data_handler: CommonDataHandler, strategy: AbstractStrategy):
        self.symbol_list: List[str] = symbol_list
        self.initial_capital: float = initial_capital
        self.start_date: str = start_date
        self.data_handler: CommonDataHandler = data_handler
        self.strategy: AbstractStrategy = strategy

        # self init property
        self.portfolio: Portfolio = Portfolio()
        self.execution_handler: SimulatedOrderExecuteHandler = SimulatedOrderExecuteHandler()

        self.global_events_que = queue.Queue()
        self.signals = 0
        self.orders = 0
        self.fills = 0
        self.num_strategies = 1
        self._heartbeat_time = 0.5  # 0.5s

        # map(symbol_code -> previous_processed_date_index)
        # 前一次处理的历史交易日期Index
        self.previous_process_date_index_map: Dict[str, int] = {}

        self.symbol_whole_bill_date: Dict[str, List[datetime]] = dict(
            [
                (symbol_code, self.data_handler.get_symbol_whole_bill_date(symbol_code).sort(reverse=False))
                for symbol_code in self.symbol_list
            ]
        )

    def _init_first_market_events(self):
        init_index = 0
        for symbol_code in self.symbol_whole_bill_date.keys():
            bill_date_list = self.symbol_whole_bill_date[symbol_code]
            self.previous_process_date_index_map[symbol_code] = init_index

            self.global_events_que.put(MarketEvent(bill_date_list[init_index]))

    def _run_back_test(self):
        """
        Executes the backtest.
        """

        heartbeats = 0
        while True:
            """
            外层:心跳
            """
            heartbeats += 1
            print("heartbeats: %s", heartbeats)
            """
            内层:循环处理事件
            """
            # Handle the events
            while True:
                try:
                    event: AbstractEvent = self.global_events_que.get(False)
                except queue.Empty:
                    break
                else:
                    if event is None:
                        continue
                    else:
                        self._process_event(event)

            time.sleep(self._heartbeat_time)

    def _process_event(self, event: AbstractEvent):
        if event.event_type() == EventTypeEnum.MARKET:

    def _output_performance(self):
        """
        Outputs the strategy performance from the backtest.
        """
        self.portfolio.create_equity_curve_data_frame()

        print("Creating summary stats...")
        stats = self.portfolio.output_summary_stats()

        print("Creating equity curve...")
        print(self.portfolio.equity_curve.tail(10))
        print(stats)

        print("Signals: %s" % self.signals)
        print("Orders: %s" % self.orders)
        print("Fills: %s" % self.fills)

    def simulate_trading(self):
        """
        Simulates the backtest and outputs portfolios performance.
        """
        self._run_back_test()
        self._output_performance()