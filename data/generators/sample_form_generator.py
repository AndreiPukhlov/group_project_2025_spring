import random

from faker import Faker

from data.test_data.sample_form_test_data.sample_person import SamplePerson

fake = Faker("en_US")

countries = [
    "Austria",
    "Belarus",
    "Canada",
    "China",
    "France",
    "Germany",
    "India",
    "Israel",
    "Italy",
    "Japan",
    "South Korea",
    "Lithuania",
    "Monaco",
    "Netherlands (Holland)",
    "Pakistan",
    "Russia",
    "Ukraine",
    "United Kingdom",
    "United States of America",
    "Uzbekistan",
    "Other"
]


def generate_sample_person_male():
    yield SamplePerson(
        first_name=fake.first_name_male(),
        middle_name=fake.first_name_male(),
        last_name=fake.last_name_male(),
        age=random.randint(18, 65),
        gender='male',
        address=fake.address(),
        email=fake.email(),
        phone_number=fake.random_number(10),
        contact_person_name=f"{fake.first_name()} {fake.last_name()}",
        contact_person_phone_number=fake.phone_number()
    )


def generate_sample_person_female():
    pass


def get_first_name():
    return fake.last_name()


def random_country_generator():
    index = random.randint(0, len(countries) - 1)
    return countries[index]


def valid_password_five_chars():
    return fake.password(5)


def invalid_password_four_chars():
    return fake.password(4)
