from traits.api import String

from force_bdss.api import (
    factory_id,
    BaseNotificationListenerFactory)

from .example_notification_listener import ExampleNotificationListener
from .example_notification_listener_model import \
    ExampleNotificationListenerModel


class ExampleNotificationListenerFactory(BaseNotificationListenerFactory):
    """This is the factory of the notification listener.
    A notification listener listens to events provided by the MCO,
    and performs operations accordingly.
    """

    #: For all the code following, see the documentation on the example
    #: data source for this
    id = String(factory_id("granta", "granta_example_notification_listener"))

    name = String("GRANTA example notification listener")

    model_class = ExampleNotificationListenerModel

    listener_class = ExampleNotificationListener
