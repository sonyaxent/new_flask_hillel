from faker import Faker

faker_instance = Faker("FR")

if __name__ == "__main__":

    print(faker_instance.first_name())
    print(faker_instance.last_name())

    print(faker_instance.profile())

