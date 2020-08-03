#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.


class DummyGrantaSession:

    def get_db(self, *args, **kwargs):
        """Returns a dummy Granta database object"""
        pass

    def make_writer(self, *args, **kwargs):
        """Returns a dummy Granta writer object"""
        pass


def connect(*args, **kwargs):
    """Stub for function to connect to a Granta database,
    returning a session object
    """
    return DummyGrantaSession()

