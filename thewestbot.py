from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time
import logging 

logging.basicConfig(level=logging.INFO,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s')

username = 'yourusername'
password = 'yourpassword'

def login(driver):
    driver.get("https://beta.the-west.net/")
    login_input = driver.find_element_by_class_name('loginUsername')
    login_input.send_keys(username)
    pass_input = driver.find_element_by_class_name('loginPassword')
    pass_input.send_keys(password)
    driver.find_element_by_id('loginButton').click()
    selected_world = False
    while not selected_world:
        try:
            driver.find_element_by_link_text('Alamogordo').click()
            selected_world = True
        except Exception as e:
            print('error: ' + str(e))
            time.sleep(1)
    # driver.close()


def find_job(driver):
    driver.find_element_by_class_name('jobs').click()
    exp_filter = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "jobs_experience"))
    )

    exp_filter.click()
    exp_filter.click()
    job_title_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "jobinfobox_title"))
    )
    job_title = job_title_element.text
    logging.info('Searching for job: {}'.format(job_title))

    minimap_element =  WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ui_minimap"))
    )

    minimap_element.click()
    # sb = driver.find_elements_by_class_name('tw2gui_jobsearch_string')
    search_bar = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="windows"]/div[3]/div[12]/div/div[2]/div[2]/div/span/span[2]/span/input'))
    )
    time.sleep(1)
    search_bar.send_keys(job_title)

    job_icon = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'mmap_icon_jobs'))
    )
    job_icon.click()

if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.maximize_window()
    login(driver)
    while True:
        try:
            energy_bar = driver.find_element_by_class_name('energy_bar').text
            break
        except Exception as e:
            logging.info('In loading screen...')
            logging.info('error: ' + str(e))
            time.sleep(1)
    logging.info('Energy value is {}'.format(energy_bar))
    find_job(driver)

    while True:
        time.sleep(1)
