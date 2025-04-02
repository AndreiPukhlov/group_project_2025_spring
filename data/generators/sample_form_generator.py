import random
from datetime import date

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


def dob_generator_select():
    year = (random.randint(date.today().year - 100, date.today().year - 18))
    month = random.randint(0, 11)

    days_in_month = {
        0: 31, 1: 29 if (year % 400 == 0 or (year % 4 == 0 and year % 100 != 0)) else 28,
        2: 31, 3: 30, 4: 31, 5: 30,
        6: 31, 7: 31, 8: 30, 9: 31,
        10: 30, 11: 31
    }

    day = random.randint(1, days_in_month[month])
    return str(year), str(month), day


def month_day_year_generator():
    year = random.randint(date.today().year - 120, date.today().year - 18)
    month = fake.month_name()

    days_in_month = {
        "January": 31, "February": 29 if (year % 400 == 0 or (year % 4 == 0 and year % 100 != 0)) else 28,
        "March": 31, "April": 30, "May": 31, "June": 30,
        "July": 31, "August": 31, "September": 30, "October": 31,
        "November": 30, "December": 31
    }

    day = random.randint(1, days_in_month[month])
    return year, month, day



