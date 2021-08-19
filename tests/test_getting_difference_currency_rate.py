from datetime import date

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

incorrect_params = [
    {"code": "USD", "date1": date(2021, 1, 1), "date2": date(2021, 1, 1)},
    {"code": "EUR", "date1": date(2020, 9, 1), "date2": date(2020, 8, 1)},
    {"code": "RUB", "date1": date(2020, 9, 1), "date2": date(2021, 8, 1)},
]

correct_params = [
    {"code": "USD", "date1": date(2013, 1, 1), "date2": date(2021, 1, 1)},
    {"code": "EUR", "date1": date(2012, 9, 10), "date2": date(2016, 8, 31)},
    {"code": "AUD", "date1": date(2006, 9, 25), "date2": date(2020, 8, 7)}
]
correct_output = [43.503, 32.0193, 32.3275]


def test_correct():
    for idx, params in enumerate(correct_params):
        response = client.get("/currency_rates_diff", params=params)
        assert response.status_code == 200
        assert response.json() == correct_output[idx]


def test_incorrect():
    for params in incorrect_params:
        response = client.get("/currency_rates_diff",
                              params=params)
        assert response.status_code == 400
        assert response.json() == {"detail": "Invalid parameters"}


def test_no_data():
    response = client.get("/currency_rates_diff",
                          params={"code": "INR", "date1": date(1990, 1, 1), "date2": date(2090, 1, 1)})
    assert response.status_code == 400
    assert response.json() == {"detail": "No data on currency INR for 1990-01-01"}
