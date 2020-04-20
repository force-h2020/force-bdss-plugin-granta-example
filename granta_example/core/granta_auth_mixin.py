from traits.api import Str, Password


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
