from abc import abstractmethod, ABCMeta
from datetime import datetime
from typing import Optional

from backend.commons.data_handlers.abstract_handler import CommonDataHandler
from backend.commons.enums.bar_val_type_enums import BarValTypeEnum
from backend.commons.enums.event_type_enums import EventTypeEnum
from backend.commons.events.base import FillEvent, OrderEvent


class AbstractOrderExecuteHandler(metaclass=ABCMeta):
    """
    The ExecutionHandler abstract class handles the interaction
    between a set of order objects generated by a Portfolio and
    the ultimate set of Fill objects that actually occur in the
    market.

    The handlers can be used to subclass simulated brokerages
    or live brokerages, with identical interfaces. This allows
    strategies to be backtested in a very similar manner to the
    live trading engine.
    """

    @abstractmethod
    def execute_order(self, data_handler: CommonDataHandler, order_event: OrderEvent):
        """
        Takes an Order event and executes it, producing
        a Fill event that gets placed onto the Events queue.

        Parameters:
        event - Contains an Event object with order information.
        """
        raise NotImplementedError("Should implement execute_order()")


class SimulatedOrderExecuteHandler(AbstractOrderExecuteHandler):
    """
    The simulated execution handler simply converts all order
    objects into their equivalent fill objects automatically
    without latency, slippage or fill-ratio issues.

    This allows a straightforward "first go" test of any strategy,
    before implementation with a more sophisticated execution
    handler.
    """

    def __init__(self):
        """
        Initialises the handler, setting the event queues
        up internally.

        Parameters:
        events - The Queue of Event objects.
        """

    def execute_order(self, data_handler: CommonDataHandler, order_event: OrderEvent) -> Optional[FillEvent]:
        """
        Simply converts Order objects into Fill objects naively,
        i.e. without any latency, slippage or fill ratio problems.

        Parameters:
        event - Contains an Event object with order information.
        """
        # 通知交易下单
        self._send_email(order_event)
        self._send_notice(order_event)

        # 处理花费
        if order_event.event_type == EventTypeEnum.ORDER:
            adj_close: float = data_handler.get_bar_value(order_event.symbol(), order_event.date_str(),
                                                          BarValTypeEnum.ADJ_CLOSE)
            fill_cost: float = float(order_event.quantity * adj_close)

            commission: float = self._commission_from_guojin(order_event)

            fill_event = FillEvent(order_event.symbol(), datetime.utcnow(), order_event.quantity,
                                   order_event.direction_type, fill_cost, commission, '国金证券')
            return fill_event

        else:
            return None

    @staticmethod
    def _commission_from_guojin(order_event: OrderEvent) -> float:
        # todo
        return order_event.quantity * 0.0

    def _fill_cost(self) -> float:
        raise NotImplementedError()

    @staticmethod
    def _send_email(order_event: OrderEvent):
        print("交易通知:%s" % order_event)
        # todo

    @staticmethod
    def _send_notice(order_event: OrderEvent):
        print("交易通知:%s" % order_event)
        # todo
