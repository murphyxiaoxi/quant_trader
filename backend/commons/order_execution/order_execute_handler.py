from abc import abstractmethod, ABCMeta
from datetime import datetime
from queue import Queue

from backend.commons.enums.event_type_enums import EventTypeEnum
from backend.commons.events.base import FillEvent, AbstractEvent, OrderEvent


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
    def execute_order(self, events_queue: Queue[AbstractEvent], event):
        """
        Takes an Order event and executes it, producing
        a Fill event that gets placed onto the Events queue.

        Parameters:
        event - Contains an Event object with order information.
        """
        raise NotImplementedError("Should implement execute_order()")


# todo
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

    def execute_order(self, events_queue: Queue[AbstractEvent], event: AbstractEvent):
        """
        Simply converts Order objects into Fill objects naively,
        i.e. without any latency, slippage or fill ratio problems.

        Parameters:
        event - Contains an Event object with order information.
        """
        if event.event_type == EventTypeEnum.ORDER:
            fill_event = FillEvent(
                datetime.utcnow(), event.symbol,
                'ARCA', event.quantity, event.direction, None
            )
            self.events_que.put(fill_event)
