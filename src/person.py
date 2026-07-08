import json
from PIL import Image
from datetime import datetime

class Person:

    """Speichert alle Informationen und EKG-Tests einer Person."""

    def __init__(self, id, username, hash_pwd, date_of_birth, firstname, lastname, picture_path, ekg_tests, smartwatch_data, gender="male"):
        self.id = id
        self.username = username
        self.hash_pwd = hash_pwd
        self.date_of_birth = date_of_birth
        self.firstname = firstname
        self.lastname = lastname
        self.picture_path = picture_path
        self.ekg_tests = ekg_tests
        self.smartwatch_data = smartwatch_data
        self.gender = gender


    @staticmethod
    def load_by_id(person_id):

        """Lädt eine Person anhand ihrer ID."""

        with open("data/person_db.json", "r", encoding="utf-8") as file:
            persons = json.load(file)

        for p in persons:
            if p["id"] == person_id:
                return Person(
                    p["id"],
                    p["username"],
                    p["hash_pwd"],
                    p["date_of_birth"],
                    p["firstname"],
                    p["lastname"],
                    p["picture_path"],
                    p["ekg_tests"],
                    p.get("smartwatch_data", []),
                    p["gender"]
                )

        return None

    @staticmethod
    def load_by_username(username):

        """Sucht einen Benutzer anhand seines Benutzernamens."""

        with open("data/person_db.json", "r", encoding="utf-8") as file:
            persons = json.load(file)

        for p in persons:
            if p["username"] == username:
                return Person(
                    p["id"],
                    p["username"],
                    p["hash_pwd"],
                    p["date_of_birth"],
                    p["firstname"],
                    p["lastname"],
                    p["picture_path"],
                    p["ekg_tests"],
                    p.get("smartwatch_data", []),
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
        try:
            return Image.open(self.picture_path)
        except FileNotFoundError:
            return None
    

    def add_smartwatch_data(self, date, file_path):

        "Fügt Messdaten einer Smartwatch hinzu"

        new_id = max(
            (entry["id"] for entry in self.smartwatch_data),
            default=0
        ) + 1

        new_entry = {
            "id": new_id,
            "date": date,
            "result_link": file_path
        }

        # Dem Objekt hinzufügen
        self.smartwatch_data.append(new_entry)

        # JSON laden
        json_path = "data/person_db.json"

        with open(json_path, "r", encoding="utf-8") as f:
            persons = json.load(f)

        # Richtige Person aktualisieren
        for p in persons:
            if p["id"] == self.id:
                p["smartwatch_data"] = self.smartwatch_data
                break

        # JSON speichern
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(persons, f, indent=4, ensure_ascii=False)

    
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