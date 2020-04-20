import granta

from traits.trait_types import Any, Str

from force_bdss.api import (
    BaseDataSourceModel, BaseNotificationListener,
    BaseNotificationListenerModel)

from .granta_auth_mixin import GrantaAuthMixin


class BaseGrantaDataSourceModel(GrantaAuthMixin, BaseDataSourceModel):
    """A BaseDataSourceModel with traits containing
    Granta MI authentication details"""


class BaseGrantaNotificationListener(BaseNotificationListener):

    #: Reference to the GrantaMI session
    _mi = Any()

    _db_key = Str()

    def initialize(self, model):
        """Expects model to be of type
        BaseGrantaNotificationListenerModel"""
        self._mi = granta.MI(
            model.url,
            user_name=model.login,
            password=model.password,
            domain=model.domain)
        self._db_key = model.db_key


class BaseGrantaNotificationListenerModel(
        GrantaAuthMixin, BaseNotificationListenerModel):
    """A BaseNotificationListenerModel with traits containing
    Granta MI authentication details"""
