"""
Contains functions to create model objects from json data
"""
import datetime
from dateutil import parser
from paranuara.models import Company, Person, PersonTag, Food


def get_timestamp_prefix():
    """
    Unique prefix for data index
    :return: string in format: 1549846344.44-
    """
    return str(datetime.datetime.now().timestamp()) + '-'


def get_or_create_company(company_json, index_prefix):
    """
    Get or create a Company object
    :param company_json: json object for a company
    :param index_prefix: Unique string for this import
    :return: new Company object
    """
    company, created = Company.objects.get_or_create(name=company_json['company'])

    if created:
        company.index_with_prefix = index_prefix+str(company_json['index'])
        company.save()

    return company


def get_or_create_person(person_json, index_prefix):
    """
    Get or create new person.
    Create and assign food and person tag accordingly.
    :param person_json: json object of a person
    :param index_prefix: Unique string for this import
    :return:
    """
    # Swapping key value. Converts {'M', 'Male'} to {'male', 'M'}. Useful for finding a key from a value.
    # New dictionary key is lower cased.
    GENDER_CHOICES_REVERSE = dict((v.lower(), k) for k, v in Person.GENDER_CHOICES)
    EYE_COLOUR_CHOICES_REVERSE = dict((v.lower(), k) for k, v in Person.EYE_COLOR_CHOICES)

    FRUITS = {'apple', 'banana', 'grape', 'orange', 'strawberry'}
    VEGETABLES = {'beetroot', 'broccoli', 'carrot', 'celery', 'cucumber'}

    person_guid = person_json['guid']
    try:
        # Get person by guid instead of index_with_prefix to avoid duplication if the same
        # record exists in future imports.
        person = Person.objects.get(guid=person_guid)
    except Person.DoesNotExist:
        person = Person()

        person.old_id = person_json['_id']
        person.guid = person_json['guid']
        person.index_with_prefix = index_prefix + str(person_json['index'])

        person.name = person_json['name']
        person.gender = GENDER_CHOICES_REVERSE.get(person_json['gender'].lower(), Person.GENDER_OTHER)

        # Calculate the year of birth
        person.year_of_birth = datetime.datetime.today().year - person_json['age']
        person.eye_color = EYE_COLOUR_CHOICES_REVERSE.get(person_json['eyeColor'].lower(), Person.EYE_COLOR_OTHER)

        person.address = person_json['address']
        person.phone = person_json['phone']
        person.email = person_json['email']

        person.about = person_json['about']
        person.picture_url = person_json['picture']

        person.balance = person_json['balance']

        # Toggle the boolean value
        person.is_alive = not person_json['has_died']
        person.registration_date = parser.parse(person_json['registered'])

        try:
            company = Company.objects.get(index_with_prefix=index_prefix+str(person_json['company_id']))
        except Company.DoesNotExist:
            company = None

        if company:
            person.company = company

        # Save person before saving many to many fields
        person.save()

        for food_name in person_json['favouriteFood']:
            food, created = Food.objects.get_or_create(name=food_name)
            if created:
                if food_name.lower() in FRUITS:
                    food.type = Food.TYPE_FRUIT
                elif food_name.lower() in VEGETABLES:
                    food.type = Food.TYPE_VEGETABLE
                else:
                    food.type = Food.TYPE_OTHER
                food.save()
            person.favorite_foods.add(food)

        for tag_name in person_json['tags']:
            tag, created = PersonTag.objects.get_or_create(name=tag_name)
            person.tags.add(tag)

        # Save person again
        person.save()

    return person


def assign_person_following(person_json, index_prefix):
    """
    Call this function after importing all people
    :param person_json: json object of a person
    :param index_prefix: Unique string for this import
    :return:
    """
    person_index_with_prefix = index_prefix + str(person_json['index'])
    try:
        person_main = Person.objects.get(index_with_prefix=person_index_with_prefix)
    except Person.DoesNotExist:
        person_main = None

    if person_main:
        for friend_json in person_json['friends']:
            friend_index_with_prefix = index_prefix + str(friend_json['index'])

            # Do now allow to follow himself / herself
            if person_index_with_prefix != friend_index_with_prefix:
                try:
                    person_who_main_person_is_following = Person.objects.get(index_with_prefix=friend_index_with_prefix)
                except Person.DoesNotExist:
                    person_who_main_person_is_following = None

                if person_who_main_person_is_following:
                    person_main.following.add(person_who_main_person_is_following)

        person_main.save()

