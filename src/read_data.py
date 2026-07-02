import json



def load_person_data(path="data/person_db.json"):

    """
    Liest alle Personendaten aus der JSON-Datei ein.
    """

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


# def get_person_list(person_data):
    
#     list_of_names = []

#     for eintrag in person_data:
#         list_of_names.append(eintrag["lastname"] + ", " +  eintrag["firstname"])
#     return list_of_names


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

if __name__ == "__main__":
    list = load_person_data()
    #person_list = get_person_list(list)
    nameid = get_name_to_id(list)

    print(list)
    #print(person_list)
    print(nameid)