def test_minimum_places_possible_in_form(client, mock_clubs, mock_competitions):
    # places achetés pour une compét par un clubs.
    # Enregistrés en db     competition["clubs_places"] = ("name_club", places_purchase)

    # Calcul du min envisagés
    # minimum_places = 1

    # Cas 01 :
    # maximum_places > minimum_places
    #

    # Cas 02 :
    # maximum_places = minimum_places
    #

    # Cas 03 :
    # maximum_places < minimum_places
    #

    pass


def test_maximum_places_possible_in_form(client, mock_clubs, mock_competitions):
    # places achetés pour une compét par un clubs.
    # Enregistrés en db     competition["clubs_places"] = ("name_club", places_purchase)

    # Calcul du max envisagés
    # competition["clubs_places"] = [x for x in competition["clubs_places"][0] == clubs["name"]][0]     a peu près
    # maximum_places = min(int(clubs["points"]), int(competition["number_of_places"]), int(competition["clubs_places"][1]), 12)

    # Les <= et >= à remplacés éventuellement par des < et > et inversement.
    # Selon comment sera calculer le max.
    #

    # Cas 01 :
    # Maximum = 12
    # Conditions
    # clubs["points"] > 12 AND competition["number_of_places"] > 12 AND competition["clubs_places"][1] = 0

    # Cas 02 :
    # Maximum = 0
    # Conditions
    # clubs["points"] = 0 OR competition["number_of_places"] = 0 OR competition["club_places"][1] = 12

    # Cas 03 :
    # Maximum = clubs["points"]
    # Conditions
    # clubs["points"] <= competition["number_of_places"] AND competition["club_places"][1] <= 12 - clubs["points"]

    # Cas 04 :
    # Maximum = competition["number_of_places"]
    # Conditions
    # competition["number_of_places"] <= 12 AND clubs["points"] > competition["number_of_places"] AND competition["clubs_places"][1] < 12 - competition[number_of_places"]

    # Cas 05 :
    # Maximum = 12 - competition["clubs_places"][1]
    # Conditions
    # competition["number_of_places"] > Maximum AND clubs["points"] > Maximum
    pass


def test_max_12_places_competition_by_club_in_several_times(client, mock_clubs, mock_competitions):
    pass



# Mettre les tests de modification de db dans un fichier distincts et y joindre ceux présents dans test_spending_points_by_club.py
def test_deduction_places_of_competition(client, mock_clubs, mock_competitions):
    pass


def test_deduction_points_of_clubs(client, mock_clubs, mock_competitions):
    pass


def test_add_purchase_places_by_clubs_in_competition_database(client, mock_clubs, mock_competitions):
    pass


def test_add_purchase_places_by_clubs_in_clubs_database(client, mock_clubs, mock_competitions):
    pass
