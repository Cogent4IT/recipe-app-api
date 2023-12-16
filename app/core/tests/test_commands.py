"""
Test custom Django management commands.
"""
# import patch in order to implement mock db
from unittest.mock import patch
# one of the error "OperationalError" comes when db is
# not ready and we try to access that.
from psycopg2 import OperationalError as Psycopg2Error
# helper function "call_command" provided
# by django to simulate to call command
from django.core.management import call_command
# another form of the error "OperationalError" comes
# when db is not ready and we try to access that.
from django.db.utils import OperationalError
# Base test class to create unit test cases
from django.test import SimpleTestCase


# mocking here by using patch, by calling check method in Command class
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """ Test commands. """

    # by mocking we get patched_check object, on which we will simulate
    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if db ready. """
        # simulating that the db is ready by
        # assigning or returning True (+ve scenario)
        patched_check.return_value = True

        # calling the "handle" function in Command class of file: wait_for_db
        call_command("wait_for_db")
        # calling the "check" method in "patched_check"
        # object by passing param "database=["default"]"
        patched_check.assert_called_once_with(databases=["default"])

    # adding patch on method level to add timeout.
    #  "patched_sleep" would be the args for that
    @patch("time.sleep")
    # by mocking we get patched_check object,
    #  simulating if db is not ready yet (-ve scenario)
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError. """
        # Simulating that "Psycopg2Error"
        # (db is not ready) will be raised 2 times
        # Simulate "OperationalError"
        # (schema is not ready) will be raised 3 times, so total = 6
        # "\" is for line break
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        # calling the "handle" function in Command class of file: wait_for_db
        call_command("wait_for_db")
        # Asserting total call is 3*2 = 6
        self.assertEqual(patched_check.call_count, 6)
        # calling the "check" method in "patched_check"
        # object by passing param "database=["default"]"
        patched_check.assert_called_with(databases=["default"])
