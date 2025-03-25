from dataclasses import dataclass


@dataclass
class SamplePerson:
    first_name: str = None
    middle_name: str = None
    last_name: str = None
    age: int = None
    gender: str = None
    address: str = None
    email: str = None
    phone_number: str = None
    contact_person_name: str = None
    contact_person_phone_number: str = None

