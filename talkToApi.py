import pytest
import json
import requests
def test_stationary_combustion_api():
    # Arrange:
    # api_key = "DEMO_KEY"
    #Act:
    response = make_request()
    #Assertion:
    print("++++++++++++++ stat comb response",response);
    assert response.status_code == 200  # Validation of status code  
    rows = response.json()
    print("++++++++++++++ stat comb rows",rows, len(rows), rows[0][0])

    # Assertion of body response content:  
    assert len(rows) > 0  
    assert rows[0][0] > 0

def make_request(): #api_key
    base_url = "http://35.173.120.161:8000/stationaryCombustion"
    print(" request ")
    response = requests.get(f'{base_url}')
    return response

