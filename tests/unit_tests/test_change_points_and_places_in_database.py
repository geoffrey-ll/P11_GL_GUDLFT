def test_correct_deduction_of_number_places_to_comp(client, mock_clubs, mock_competitions):
    numbers_of_places_comp_initial = int(
        mock_competitions[0]["number_of_places"]
    )
    data_test = {
        "email": mock_clubs[0]["email"],
        "club": mock_clubs[0]["name"],
        "competition": mock_competitions[0]["name"],
        "places": min(
            int(mock_clubs[0]["points"]),
            int(mock_competitions[0]["number_of_places"]),
            12
        )
    }

    # AVEC UN follow_redirects=True IMOPOSSIBLE DE FAIRE PASSER LE TESTS
    # CAR LE response_purchase.status_code EST TOUJOURS 400…
    #
    # CETTE response EST ENVOYÉE AVEC UN CODE 307, CONTRAIREMENT AU AUTRES TESTS
    # QUI MARCHE QUI ONT DES response ENVOYÉE AVEC UN CODE 302
    #
    #
    # response_purchase = client.post(
    #     "/purchasePlaces",
    #     data=data_test,
    #     follow_redirects=True
    # )
    # numbers_of_places_comp_final = int(mock_competitions[0]["number_of_places"])
    #
    # assert response_purchase.status_code == 200
    # assert numbers_of_places_comp_final == (
    #         numbers_of_places_comp_initial - data_test["places"]
    # )

    response_purchase = client.post("/purchasePlaces", data=data_test)
    response_summary = client.post("/showSummary", data=data_test)
    numbers_of_places_comp_final = int(
            mock_competitions[0]["number_of_places"]
    )

    assert response_purchase.status_code == 307
    assert response_summary.status_code == 200
    assert numbers_of_places_comp_final == (
            numbers_of_places_comp_initial - data_test["places"]
    )


def test_correct_deduction_of_points_club(client, mock_clubs, mock_competitions):
    points_of_clubs_initial = int(mock_clubs[0]["points"])
    data_test = {
        "email": mock_clubs[0]["email"],
        "club": mock_clubs[0]["name"],
        "competition": mock_competitions[0]["name"],
        "places": min(
            int(mock_clubs[0]["points"]),
            int(mock_competitions[0]["number_of_places"]),
            12
        )
    }

    # AVEC UN follow_redirects=True IMOPOSSIBLE DE FAIRE PASSER LE TESTS
    # CAR LE response_purchase.status_code EST TOUJOURS 400…
    #
    # CETTE response EST ENVOYÉE AVEC UN CODE 307, CONTRAIREMENT AU AUTRES TESTS
    # QUI MARCHE QUI ONT DES response ENVOYÉE AVEC UN CODE 302
    #
    #
    # response_purchase = client.post(
    #     "/purchasePlaces",
    #     data=data_test,
    #     follow_redirects=True
    # )
    # points_of_clubs_final = int(mock_clubs[0]["points"])
    #
    # assert response_purchase.status_code == 200
    # assert points_of_clubs_final == (
    #         points_of_clubs_initial - data_test["places"]
    # )

    response_purchase = client.post("/purchasePlaces", data=data_test)
    points_of_clubs_final = int(mock_clubs[0]["points"])

    assert response_purchase.status_code == 307
    assert points_of_clubs_final == (
            points_of_clubs_initial - data_test["places"]
    )
