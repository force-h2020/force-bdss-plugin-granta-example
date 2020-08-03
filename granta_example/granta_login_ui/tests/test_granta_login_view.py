#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from unittest import TestCase, mock

from granta_example.granta_login_ui.granta_login_view import (
    GrantaLoginModel, GrantaLoginView)

GRANTA_CONNECT_PATH = 'granta.connect'


def mock_connect_error(*args, **kwargs):
    raise ConnectionError('Connection failed')


class TestGrantaLoginModel(TestCase):

    def setUp(self):
        self.model = GrantaLoginModel()

    def test_test_connection(self):
        check, error = self.model.test_connection()
        self.assertTrue(check)
        self.assertIsNone(error)

        with mock.patch(GRANTA_CONNECT_PATH) as mock_connect:
            mock_connect.side_effect = mock_connect_error

            check, error = self.model.test_connection()
            self.assertFalse(check)
            self.assertIsInstance(error, ConnectionError)


class TestGrantaLoginView(TestCase):

    def setUp(self):
        self.model = GrantaLoginModel()
        self.view = GrantaLoginView(model=self.model)

    def test_can_connect(self):
        self.assertTrue(self.view.can_connect())

        with mock.patch(GRANTA_CONNECT_PATH) as mock_connect:
            mock_connect.side_effect = mock_connect_error

            with mock.patch.object(
                    GrantaLoginView, '_display_error') as mock_dialog:
                self.assertFalse(self.view.can_connect())
                mock_dialog.assert_called()
