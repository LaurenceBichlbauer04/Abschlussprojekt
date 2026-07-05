import json



def load_person_data(path="data/person_db.json"):

    """
    Liest alle Personendaten aus der JSON-Datei ein.
    """

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def get_name_to_id(person_data):

    """
    Erstellt ein Dictionary, das den vollständigen Namen
    einer Person ihrer ID zuordnet.
    """

    name_to_id = {}

    for person in person_data:
        name = person["lastname"] + ", " + person["firstname"]
        name_to_id[name] = person["id"]

    return name_to_id

def find_person_data_by_name(suchstring):
    person_data = load_person_data()
    
    if suchstring == "None":
        return {}

    two_names = suchstring.split(", ")
    vorname = two_names[1]
    nachname = two_names[0]

    for eintrag in person_data:
        print(eintrag)
        if (eintrag["lastname"] == nachname and eintrag["firstname"] == vorname):
            print()

            return eintrag
    else:
        return {}
    
def add_person(firstname, lastname, birth_year, gender, picture_path):
    """
    Fügt eine neue Person zur person_db.json hinzu.
    """

    person_data = load_person_data()

    new_id = max(person["id"] for person in person_data) + 1

    new_person = {
        "id": new_id,
        "firstname": firstname,
        "lastname": lastname,
        "date_of_birth": birth_year,
        "gender": gender,
        "picture_path": picture_path,
        "ekg_tests": []
    }

    person_data.append(new_person)

    with open("data/person_db.json", "w", encoding="utf-8") as file:
        json.dump(person_data, file, indent=4)

    return new_id

def add_ekg_test(person_id, test_date, result_link):
    """
    Fügt einer vorhandenen Person einen neuen EKG-Test hinzu.
    """

    person_data = load_person_data()

    # höchste vorhandene Test-ID suchen
    highest_test_id = 0

    for person in person_data:
        for test in person["ekg_tests"]:
            if test["id"] > highest_test_id:
                highest_test_id = test["id"]

    new_test = {
        "id": highest_test_id + 1,
        "date": str(test_date),
        "result_link": result_link
    }

    for person in person_data:
        if person["id"] == person_id:
            person["ekg_tests"].append(new_test)
            break

    with open("data/person_db.json", "w", encoding="utf-8") as file:
        json.dump(person_data, file, indent=4)

def delete_person(person_id):
    """
    Löscht eine Person anhand ihrer ID aus der Datenbank.
    """

    person_data = load_person_data()

    person_data = [
        person for person in person_data
        if person["id"] != person_id
    ]

    with open("data/person_db.json", "w", encoding="utf-8") as file:
        json.dump(person_data, file, indent=4)

def update_person(person_id, firstname, lastname, birth_year, gender, picture_path):
    """
    Aktualisiert die Daten einer bestehenden Person.
    """

    person_data = load_person_data()

    for person in person_data:
        if person["id"] == person_id:
            person["firstname"] = firstname
            person["lastname"] = lastname
            person["date_of_birth"] = birth_year
            person["gender"] = gender
            person["picture_path"] = picture_path
            break

    with open("data/person_db.json", "w", encoding="utf-8") as file:
        json.dump(person_data, file, indent=4)


if __name__ == "__main__":
    list = load_person_data()
    #person_list = get_person_list(list)
    nameid = get_name_to_id(list)

    print(list)
    #print(person_list)
    print(nameid)