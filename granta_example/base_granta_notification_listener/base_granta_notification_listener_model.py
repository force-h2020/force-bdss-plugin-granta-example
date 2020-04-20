from traits.api import Unicode, Password

from force_bdss.api import BaseNotificationListenerModel


class BaseGrantaNotificationListenerModel(BaseNotificationListenerModel):

    #: URL of Granta database, by default the FORCE database is provided
    url = Unicode('https://force.granta.com/mi_servicelayer/')

    #: Login name, must be provided by the user
    login = Unicode()

    #: Login password, must be provided by the user
    password = Password()

    #: Optional domain of database connection
    domain = Unicode()

    #: Reference key to FORCE Granta database
    db_key = Unicode('MI_Force')
