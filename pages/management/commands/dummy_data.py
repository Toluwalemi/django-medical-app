import datetime
import random

from django.core.management.base import BaseCommand

from pages.models import Patient, Illness, MedicalInfo

illnesses = [
    'Malaria',
    'Ebola',
    'Covid19',
    'Fever',
    'Typhoid'
]

patients = ['Leon', 'Rayy', 'Fred', 'John', 'Jayy', 'Kay', 'Ron', 'Greg']

blood_group = [
    'A',
    'AB',
    'B',
    'O'
]

gender = [
    'Female',
    'Male',
    'Other'
]


# def generate_patient_name():
#     ran_index = random.randint(0, len(patients) - 1)
#     random_index = patients[ran_index]
#     return str(random_index)

def generate_patient_name():
    rand_idx = int(random.random() * len(patients))
    random_num = patients[rand_idx]
    return str(random_num)


def generate_illness_name():
    index = random.randint(0, len(illnesses) - 1)
    random_index = illnesses[index]
    return str(random_index)


def generate_blood_group():
    index = random.randint(0, 3)
    return blood_group[index]


def generate_gender():
    index = random.randint(0, 2)
    return gender[index]


def generate_age():
    return random.randint(18, 70)


def generate_creation_date():
    year = random.randint(2000, 2030)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return datetime.date(year, month, day)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            'file_name', type=str, help='This text file contains random medical summaries.')

    def handle(self, *args, **kwargs):
        file_name = kwargs['file_name']
        with open(f'{file_name}.txt') as file:
            for row in file:
                summary = row
                patient_name = generate_patient_name()
                illness_name = generate_illness_name()
                gender_type = generate_gender()
                age = generate_age()
                blood_group_type = generate_blood_group()
                creation_date = generate_creation_date()

                patient = Patient.objects.get_or_create(
                    user=patient_name
                )

                medical_info = MedicalInfo(
                    summary=summary,
                    patient=Patient.objects.get(user=patient_name),
                    gender=gender_type,
                    age=age,
                    blood_group=blood_group_type,
                    created=creation_date,
                )

                medical_info.save()

                illness = Illness.objects.get_or_create(name=illness_name)

                medical_info.illnesses.add(
                    Illness.objects.get(name=illness_name))

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
