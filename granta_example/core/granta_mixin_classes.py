import granta

from traits.api import HasStrictTraits, Any, Str, Password


class GrantaAuthMixin(HasStrictTraits):
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


class GrantaConnectMixin(HasStrictTraits):

    #: Reference to the GrantaMI session
    _mi = Any()

    #: Key reference to the database to connect to
    _db_key = Str()

    def _connect_mi(self, model):
        """Sets up a Granta MI database session using authentication
        details in model

        Parameters
        ----------
        model: GrantaAuthMixin
            Object that inherits from GrantaAuthMixin and thereby
            provides access information to a database
        """
        self._mi = granta.connect(
            model.url,
            user_name=model.login,
            password=model.password,
            domain=model.domain)
        self._db_key = model.db_key
