import granta

from traits.api import Str, Any

from force_bdss.api import BaseNotificationListener


class BaseGrantaNotificationListener(BaseNotificationListener):

    #: Reference to the GrantaMI session
    _mi = Any()

    _db_key = Str()

    def initialize(self, model):
        self._mi = granta.MI(
            model.url,
            user_name=model.login,
            password=model.password,
            domain=model.domain)
        self._db_key = model.db_key
