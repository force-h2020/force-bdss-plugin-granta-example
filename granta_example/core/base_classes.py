from force_bdss.api import (
    BaseDataSource, BaseDataSourceModel,
    BaseNotificationListener, BaseNotificationListenerModel)

from .granta_mixin_classes import GrantaAuthMixin, GrantaConnectMixin


class BaseGrantaDataSource(GrantaConnectMixin, BaseDataSource):
    """A BaseDataSource with utility traits and methods for
    connecting to a Granta MI database"""


class BaseGrantaDataSourceModel(GrantaAuthMixin, BaseDataSourceModel):
    """A BaseDataSourceModel with traits containing
    Granta MI authentication details"""


class BaseGrantaNotificationListener(
        GrantaConnectMixin, BaseNotificationListener):
    """A BaseNotificationListener with utility traits and methods for
    connecting to a Granta MI database"""

    def initialize(self, model):
        """Initializes a session with a Granta MI database

        Parameters
        ----------
        model: BaseGrantaNotificationListenerModel
            Model associated with this class
        """
        self._connect_mi(model)


class BaseGrantaNotificationListenerModel(
        GrantaAuthMixin, BaseNotificationListenerModel):
    """A BaseNotificationListenerModel with traits containing
    Granta MI authentication details"""
