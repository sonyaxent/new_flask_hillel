from faker import Faker
from datetime import datetime
faker = Faker("FR")

if __name__ == "__main__":
    def generate_students(count=10):
        faker = Faker("EN")
        student_data = {}
        for i in range(0, count):
            student_data[i] = {}
            student_data[i]['Name'] = faker.name()
            student_data[i]['Email'] = faker.email()
            student_data[i]['Password'] = faker.password()
            student_data[i]['Date of birth'] = faker.date_between_dates(date_start=datetime(1985, 1, 1),
                                                                        date_end=datetime(2001, 1, 1)).year
        print(student_data)

generate_students()