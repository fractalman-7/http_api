from datetime import date

from fastapi.testclient import TestClient

from app.main import app

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
correct_output = [
    {"diff": 43.503, "rate1": 30.3727, "rate2": 73.8757},
    {"diff": 32.0193, "rate1": 40.482, "rate2": 72.5013},
    {"diff": 32.3275, "rate1": 20.1661, "rate2": 52.4936}
]


def test_correct():
    with TestClient(app) as client:
        for idx, params in enumerate(correct_params):
            response = client.get("/currency_rate_diff", params=params)
            assert response.status_code == 200
            assert response.json() == correct_output[idx]


def test_incorrect():
    with TestClient(app) as client:
        for params in incorrect_params:
            response = client.get("/currency_rate_diff",
                                  params=params)
            assert response.status_code == 400
            assert response.json() == {"detail": "Invalid parameters"}


def test_no_data():
    with TestClient(app) as client:
        response = client.get("/currency_rate_diff",
                              params={"code": "INR", "date1": date(1990, 1, 1), "date2": date(2090, 1, 1)})
        assert response.status_code == 400
        assert response.json() == {"detail": "No data on currency INR for 01.01.1990"}
