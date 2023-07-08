import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('./chromedriver.exe')
    pytest.driver.implicitly_wait(5)
    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends.skillfactory.ru/login')
    myDynamicElement = pytest.driver.find_element(By.ID, "email")

    yield

    pytest.driver.quit()


def test_show_my_pets():
    # Вводим email
    pytest.driver.find_element(By.ID, 'email').send_keys('EMAIL') # необходимо изменить на действующий
    # Вводим пароль
    pytest.driver.find_element(By.ID, 'pass').send_keys('PASS') # необходимо изменить на действующий
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    pytest.driver.find_element(By.LINK_TEXT, 'Мои питомцы').click()

    element = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.ID, "all_my_pets")))

    pet_count = pytest.driver.find_elements(By.CSS_SELECTOR, '.\\.col-sm-8.right.fill tbody th')

    user_stat = pytest.driver.find_element(By.CSS_SELECTOR, '.\\.col-sm-4.left')
    user_stat_split = user_stat.text.split('\n')
    pet_count_stat = int(re.sub("[^0-9]", "", user_stat_split[1]))

    images = pytest.driver.find_elements(By.XPATH, f'//*[@id="all_my_pets"]/table[1]/tbody[1]/tr/th/img')
    # images = pytest.driver.find_elements(By.CSS_SELECTOR, '.\\.col-sm-8.right.fill tbody th img')
    names = list()
    breed = list()
    age = list()

    for line in range(1, len(pet_count)+1):
        names.append(pytest.driver.find_element(By.XPATH,
            f'//*[@id="all_my_pets"]/table[1]/tbody[1]/tr[{line}]/td[1]'))
        breed.append(pytest.driver.find_element(By.XPATH,
            f'//*[@id="all_my_pets"]/table[1]/tbody[1]/tr[{line}]/td[2]'))
        age.append(pytest.driver.find_element(By.XPATH,
            f'//*[@id="all_my_pets"]/table[1]/tbody[1]/tr[{line}]/td[3]'))

    for i in range(len(pet_count)):
        assert images[i].get_attribute('img.src') != ''
        assert names[i].text != '' #есть имя
        assert breed[i].text != '' #есть порода
        assert age[i].text != '' #есть возраст
        assert len(pet_count)== pet_count_stat #присутствуют все питомцы
        for n in range(i+1, len(names)):
            assert names[i].text != names[n].text   #проверка уникальных имен


