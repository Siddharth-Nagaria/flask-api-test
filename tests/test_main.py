import sys
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app

def test_landing_unit_test():
    response = app.test_client().get('/')
    assert response.status_code == 200
    assert b'Hi, Welcome to Unit testing' in response.data
    logger.info(f"Received response: {response.status_code}")
    logger.info(f"Response data: {response.data.decode()}")

def test_login_unit_test():
    response = app.test_client().get('/login/sid')
    assert response.status_code == 200
    assert b'sid testing' in response.data
    logger.info(f"Response data: {response.status_code}")


def test_factorial_unit_test():
    response = app.test_client().get('/factorial/7')
    assert response.status_code == 200

    json_data = response.get_json()
    assert "number" in json_data
    assert json_data["number"]==7 
    assert "factorial" in json_data
    assert json_data["factorial"]==5040  
    logger.info(f"Response data: {json_data}")



def test_handle_get_valid_credentials():
    response = app.test_client().get('/handle_get?username=siddharth&password=1234')
    assert response.status_code == 200
    assert b'Welcome!!!' in response.data
    logger.info(f"Response data: {response.data.decode()}")

def test_handle_get_invalid_credentials():
    response = app.test_client().get('/handle_get?username=siddharth&password=wrongpassword')
    assert response.status_code == 200
    assert b'invalid credentials!' in response.data
    logger.info(f"Response data: {response.data.decode()}")

def test_handle_get_missing_credentials():
    response = app.test_client().get('/handle_get?username=&password=')
    assert response.status_code == 200
    assert b'invalid credentials!' in response.data
    logger.info(f"Response data: {response.data.decode()}")

def test_handle_post_valid_credentials():
    response = app.test_client().post('handle_post', data = {'username': 'siddharth', 'password': '1234'})
    assert response.status_code == 200
    assert b'Welcome!!!' in response.data
    logger.info(f"Response data: {response.data.decode()}")

def test_handle_post_invalid_credentials():
    response = app.test_client().post('handle_post', data = {'username': 'siddharth', 'password': 'wrong_password'})
    assert response.status_code == 200
    assert b'invalid credentials!' in response.data
    logger.info(f"Response data: {response.data.decode()}")

def test_handle_post_missing_credentials():
    response = app.test_client().post('handle_post', data = {'username': '', 'password': ''})
    assert response.status_code == 200
    assert b'invalid credentials!' in response.data
    logger.info(f"Response data: {response.data.decode()}")

