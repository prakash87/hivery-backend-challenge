from unittest import TestCase
from django.test import Client
from django import urls
from . import test_data
import json

from paranuara.data_loader import get_timestamp_prefix, get_or_create_company, get_or_create_person, \
    assign_person_following


class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.index_prefix = get_timestamp_prefix()

        get_or_create_company(test_data.COMPANY1, self.index_prefix)
        get_or_create_company(test_data.COMPANY2, self.index_prefix)

        get_or_create_person(test_data.PERSON1, self.index_prefix)
        get_or_create_person(test_data.PERSON2, self.index_prefix)
        get_or_create_person(test_data.PERSON3, self.index_prefix)

        assign_person_following(test_data.PERSON1, self.index_prefix)
        assign_person_following(test_data.PERSON2, self.index_prefix)
        assign_person_following(test_data.PERSON3, self.index_prefix)

    def test_get_company_detail_with_employees(self):
        response = self.client.get(urls.reverse('company_detail', args=(1,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            {
                "id": 1,
                "name": "LINGOAGE",
                "employees": [
                    {
                        "id": 1,
                        "name": "Carmella Lambert",
                        "age": 61,
                        "address": "628 Sumner Place, Sperryville, American Samoa, 9819",
                        "phone": "+1 (910) 567-3630"
                    },
                    {
                        "id": 2,
                        "name": "Decker Mckenzie",
                        "age": 60,
                        "address": "492 Stockton Street, Lawrence, Guam, 4854",
                        "phone": "+1 (893) 587-3311"
                    },
                    {
                        "id": 3,
                        "name": "Bonnie Bass",
                        "age": 54,
                        "address": "455 Dictum Court, Nadine, Mississippi, 6499",
                        "phone": "+1 (823) 428-3710"
                    },
                ]
            },
            json.loads(response.content.decode("utf-8")))

    def test_get_company_detail_with_no_employees(self):
        response = self.client.get(urls.reverse('company_detail', args=(2,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            {
                "id": 2,
                "name": "INTERLOO",
                "employees": []
            },
            json.loads(response.content.decode("utf-8")))

    def test_get_company_not_found(self):
        response = self.client.get(urls.reverse('company_detail', args=(9,)))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            {
                "detail": "Not found."
            },
            json.loads(response.content.decode("utf-8")))

    def test_get_person_detail(self):
        response = self.client.get(urls.reverse('person_detail', args=(3,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            {
                "username": "Bonnie Bass",
                "age": 54,
                "fruits": [
                    "orange",
                    "banana",
                    "strawberry"
                ],
                "vegetables": [
                    "beetroot"
                ]
            },
            json.loads(response.content.decode("utf-8")))

    def test_get_person_not_found(self):
        response = self.client.get(urls.reverse('person_detail', args=(9,)))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            {
                "detail": "Not found."
            },
            json.loads(response.content.decode("utf-8")))

    def test_get_compare_people(self):
        response = self.client.get(urls.reverse('people_compare', kwargs={'comma_separated_ids': '2,1'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            {
                "people": [
                    {
                        "id": 1,
                        "name": "Carmella Lambert",
                        "age": 61,
                        "address": "628 Sumner Place, Sperryville, American Samoa, 9819",
                        "phone": "+1 (910) 567-3630"
                    },
                    {
                        "id": 2,
                        "name": "Decker Mckenzie",
                        "age": 60,
                        "address": "492 Stockton Street, Lawrence, Guam, 4854",
                        "phone": "+1 (893) 587-3311"
                    }
                ],
                "following_in_common": [
                    {
                        "id": 3,
                        "name": "Bonnie Bass",
                        "age": 54,
                        "address": "455 Dictum Court, Nadine, Mississippi, 6499",
                        "phone": "+1 (823) 428-3710"
                    }
                ]
            },
            json.loads(response.content.decode("utf-8")))

    def test_get_following_in_common_with_blue_eye_color(self):
        response = self.client.get(urls.reverse('people_compare', kwargs={'comma_separated_ids': '2,1'}) +
                                   '?eye_color=BL')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            {
                "people": [
                    {
                        "id": 1,
                        "name": "Carmella Lambert",
                        "age": 61,
                        "address": "628 Sumner Place, Sperryville, American Samoa, 9819",
                        "phone": "+1 (910) 567-3630"
                    },
                    {
                        "id": 2,
                        "name": "Decker Mckenzie",
                        "age": 60,
                        "address": "492 Stockton Street, Lawrence, Guam, 4854",
                        "phone": "+1 (893) 587-3311"
                    }
                ],
                "following_in_common": [
                    {
                        "id": 3,
                        "name": "Bonnie Bass",
                        "age": 54,
                        "address": "455 Dictum Court, Nadine, Mississippi, 6499",
                        "phone": "+1 (823) 428-3710"
                    }
                ]
            },
            json.loads(response.content.decode("utf-8")))

    def test_get_following_in_common_with_brown_eye_color(self):
        response = self.client.get(urls.reverse('people_compare', kwargs={'comma_separated_ids': '2,1'}) +
                                   '?eye_color=BR')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            {
                "people": [
                    {
                        "id": 1,
                        "name": "Carmella Lambert",
                        "age": 61,
                        "address": "628 Sumner Place, Sperryville, American Samoa, 9819",
                        "phone": "+1 (910) 567-3630"
                    },
                    {
                        "id": 2,
                        "name": "Decker Mckenzie",
                        "age": 60,
                        "address": "492 Stockton Street, Lawrence, Guam, 4854",
                        "phone": "+1 (893) 587-3311"
                    }
                ],
                "following_in_common": []
            },
            json.loads(response.content.decode("utf-8")))
