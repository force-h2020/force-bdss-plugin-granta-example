import granta

from traits.api import Any, Str, Password


class GrantaAuthMixin:
    """Mixin class containing traits required for authentication
    to a Granta MI database
    """

    #: URL of Granta database, by default the FORCE database is provided
    url = Str('https://force.granta.com/mi_servicelayer/')

    #: Login name, must be provided by the user
    login = Str()

    #: Login password, must be provided by the user
    password = Password()

    #: Optional domain of database connection
    domain = Str()

    #: Reference key to FORCE Granta database
    db_key = Str('MI_Force')


class GrantaConnectMixin:

    #: Reference to the GrantaMI session
    _mi = Any()

    #: Key reference to the database to connect to
    _db_key = Str()

    def _connect_mi(self, model):
        """Sets up a Granta MI database session using authentication
        details in model

        Parameters
        ----------
        model: BaseGrantaNotificationListenerModel
            Model associated with this class
        """
        self._mi = granta.MI(
            model.url,
            user_name=model.login,
            password=model.password,
            domain=model.domain)
        self._db_key = model.db_key
