def test_message_when_spend_more_points_have_club(client, mock_clubs):
    pass


def test_message_confirm_spending_points(client, mock_clubs, mock_competitions):
    data_purchase_test = {
        "club": mock_clubs[0]["name"],
        "competition": mock_competitions[0]["name"],
        "places": 6
    }

    response_purchase = client.post("/purchasePlaces", data=data_purchase_test)
    expected_value = "Great-booking complete!"

    assert response_purchase.status_code == 200
    assert expected_value in response_purchase.data.decode()



def test_correct_deduction_of_spent_points(client, mock_clubs):
    pass


