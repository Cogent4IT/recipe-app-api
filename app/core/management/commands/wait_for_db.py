"""
Django command to wait for database to be available.
"""
# for timeout
import time
# raise error when db is not ready
from psycopg2 import OperationalError as Psycopg20pError
# django throws another type error when db is not ready
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """ Django command to wait for database. """
    # when we call the command, it will run this handle method
    def handle(self, *args, **options):
        """Entrypoint for command. """
        # writing to console
        self.stdout.write("Waiting for database ...")
        db_up = False
        while db_up is False:
            try:
                # we call the db, if it is not ready yet, it throws
                # error and go to "except" section
                self.check(databases=["default"])
                db_up = True
            except (Psycopg20pError, OperationalError):
                self.stdout.write("Database unavailable, waiting 1 second ...")
                # timeout for 1 second
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS("Database available !"))
