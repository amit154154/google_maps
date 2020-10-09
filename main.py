import utm
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
import pyproj

from pyproj import Proj, transform


def set_driver(url):
    driver = webdriver.Chrome('/Users/amitisraeli/PycharmProjects/google_maps/chromedriver')
    driver.get(url)
    return driver

def fsd(x1,y1):#
    p = Proj(proj='utm',zone=10,ellps='WGS84', preserve_units=False)
    x,y =p(x1, y1)
    return x ,y

def get_image_gov(cords,zoom):
    url = 'https://govmap.gov.il/?c={cord_x},{cord_y}&z={z}&b=1&sb=8'.format(cord_x=cords[0],cord_y=cords[1],z = zoom)
    print(url)
    driver = set_driver(url)
    image_name = str(cords) + '.jpg'
    xpath_zoom_in = '/html/body/div[1]/div[4]/button[1]'
    element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, xpath_zoom_in)))
    time.sleep(3)
    element.click()
    time.sleep(1)
    element.click()
    time.sleep(1.4)
    driver.save_screenshot('data/gov/'+image_name)
    driver.close()

def get_image_googleMaps(cords,zoom):
    url = 'https://www.google.com/maps/@{cord_x},{cord_y},{meter_zoom}m/data=!3m1!1e3'.format(cord_x = cords[0],cord_y = cords[1],meter_zoom = zoom)
    driver = set_driver(url)
    image_name = str(cords) + '.jpg'
    wait = WebDriverWait(driver, 10)
    men_menu = wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="runway-expand-button"]/div/div')))
    driver.save_screenshot('data/google maps/'+image_name)
    driver.close()

def main():
    #gov avocado -175464.7 , 643473.2    31.8830192,34.7416043
    cords = [-175464.7,643473.2]
    x,y = fsd(31.8830192,34.7416043)

if __name__ == '__main__':
    main()

#X: בין 100,000 ל- 300,000 Y: בין 370,000 ל- 810,000 מופרדים ע”י פסיק.