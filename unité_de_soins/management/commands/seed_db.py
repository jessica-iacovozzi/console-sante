from django.core.management.base import BaseCommand
from django.db import connection
from django.conf import settings
from pathlib import Path
import os


class Command(BaseCommand):
    help = 'Populates the database'

    def handle(self, *args, **options):
        print('Populating the database...')
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, 'dev_seed.sql' if settings.DEBUG else 'prod_seed.sql')
        sql = Path(file_path).read_text()

        with connection.cursor() as cursor:
            cursor.execute(sql)
