import json
import os
from django.conf import settings
from django.core.management.base import BaseCommand

from paranuara.data_loader import get_or_create_company, get_or_create_person, assign_person_following, get_timestamp_prefix


class Command(BaseCommand):
    help = 'Imports data from companies.json and people.json'

    COMPANIES_FILE = os.path.join(settings.BASE_DIR, 'resources/companies.json')
    PEOPLE_FILE = os.path.join(settings.BASE_DIR, 'resources/people.json')
    INDEX_PREFIX = get_timestamp_prefix()

    def handle(self, *args, **options):
        self.stdout.write('-----------------------------------------------------')
        self.stdout.write('Importing data. This may take some time.')
        self.stdout.write('-----------------------------------------------------')

        with open(Command.COMPANIES_FILE) as companies_file, open(Command.PEOPLE_FILE) as people_file:
            companies_json = json.load(companies_file)
            people_json = json.load(people_file)

            # --- Creating companies ---
            for company_json in companies_json:
                get_or_create_company(company_json, Command.INDEX_PREFIX)
            self.stdout.write(self.style.SUCCESS('Created companies. Now creating people.'))

            # --- Creating people ---
            for person_json in people_json:
                get_or_create_person(person_json, Command.INDEX_PREFIX)
            self.stdout.write(self.style.SUCCESS('Created people. Now assigning following (friends).'))

            #  --- Assigning person to people he/she is following ---
            for person_json in people_json:
                assign_person_following(person_json, Command.INDEX_PREFIX)
            self.stdout.write(self.style.SUCCESS('Assigned people to person following'))

        self.stdout.write(self.style.SUCCESS('All done.'))

