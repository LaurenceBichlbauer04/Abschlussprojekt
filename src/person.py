import json
from PIL import Image
from datetime import datetime

class Person:

    """Speichert alle Informationen und EKG-Tests einer Person."""

    def __init__(self, id, date_of_birth, firstname, lastname,picture_path, ekg_tests, gender="male"):
        self.id = id
        self.date_of_birth = date_of_birth
        self.firstname = firstname
        self.lastname = lastname
        self.picture_path = picture_path
        self.ekg_tests = ekg_tests
        self.gender = gender



    def load_by_id(person_id):

        with open("data/person_db.json", "r", encoding="utf-8") as file:
            persons = json.load(file)

        for p in persons:
            if p["id"] == person_id:
                return Person(
                    p["id"],
                    p["date_of_birth"],
                    p["firstname"],
                    p["lastname"],
                    p["picture_path"],
                    p["ekg_tests"],
                    p["gender"]
                )

        return None


    
    def calc_age(self):
        return datetime.now().year - self.date_of_birth


   
    def calc_max_heart_rate(self):

        """
        Berechnet die maximale theoretische Herzfrequenz
        anhand von Alter und Geschlecht.
        """

        age = self.calc_age()

        if self.gender.lower() == "female":
            return 226 - age

        return 220 - age


    def get_full_name(self):
        return f"{self.lastname}, {self.firstname}"


   
    def get_image(self):
        return Image.open(self.picture_path)
    

    
if __name__ == "__main__":

    print("Testing Person class...")

    person = Person.load_by_id(1)

    if person is not None:
        print("Name:", person.get_full_name())
        print("Alter:", person.calc_age())
        print("Max HF:", person.calc_max_heart_rate())
        print("Geschlecht:", person.gender)
    else:
        print("Person nicht gefunden.")