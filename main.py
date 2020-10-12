from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import logging
import threading
import time
from pyproj import Proj, transform
import os
import pyproj
from PIL import Image




def set_driver(url):
    #set selinium driver
    driver = webdriver.Chrome('/Users/amitisraeli/PycharmProjects/google_maps/chromedriver')
    driver.get(url)
    return driver

def LatLon_to_xy(lat,lon):
    #Lat Lon to xy convator, googlemaps - Lat Lon , gov - xy
    p = Proj(proj='utm',zone=10,ellps='WGS84', preserve_units=False)
    x,y =p(lat,lon)
    return x ,y

def xy_to_LatLon(x,y):
    #xyn to Lat Lon convator, googlemaps - Lat Lon , gov - xy
    # define the projections
    p1 = Proj(init='epsg:28992')
    p2 = Proj(proj='latlong', datum='WGS84')

    # Transform point (155000.0, 446000.0) with EPSG:28992
    lon, lat, z = transform(p1, p2, 155000.0, 446000.0, 0.0)
    return lon, lat  # 5.38720294616 52.0023756348 43.6057764404

def get_image_gov(cords,zoom):
    if(check_exist_cords('gov',cords) == False):
        url = 'https://govmap.gov.il/?c={cord_x},{cord_y}&z={z}&b=1&sb=8'.format(cord_x=cords[0],cord_y=cords[1],z = zoom)
        driver = set_driver(url)
        image_name = str(cords) + '.png'
        image_path = 'data/gov/'+image_name
        xpath_zoom_in = '/html/body/div[1]/div[4]/button[1]'
        element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, xpath_zoom_in)))
        time.sleep(3)
        element.click()
        time.sleep(1)
        element.click()
        time.sleep(1.4)
        driver.save_screenshot(image_path)
        driver.close()
        crop_image(image_path,'gov')
    else:
        print('skip')

def crop_image(image_path,map_type):
    img = Image.open(image_path)
    width, height = img.size
    print(width,height)
    left = 350
    top = 100
    right = 850
    bottom = 600

    im1 = img.crop((left, top, right, bottom))
    print(im1.size)
    #os.remove(image_path)
    #img.save(image_path, 'png')
    im1.show()




def get_image_googleMaps(cords,zoom,istest = False):
    if(check_exist_cords('google',cords) == False or istest):
        fix_cords = xy_to_LatLon(cords[0],cords[1])
        url = 'https://www.google.com/maps/@{cord_x},{cord_y},{meter_zoom}m/data=!3m1!1e3'.format(cord_x = fix_cords[0],cord_y = fix_cords[1],meter_zoom = str(zoom))
        print(url)
        driver = set_driver(url)
        image_name = str(cords) + '.png'
        wait = WebDriverWait(driver, 10)
        time.sleep(2)
        wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="runway-expand-button"]/div/div')))
        time.sleep(2)
        driver.save_screenshot('data/google maps/'+image_name)
        driver.close()
    else:
        print('skip')

def get_images_cords(images_cords,map_type,zoom,thread_num = None):
    #thread print if using threads
    if thread_num == None:
        print('no use of multi thread')
    else:
        print('thread num: ' + str(thread_num))

    #set map type function
    if (map_type == 'google'):
        func = get_image_googleMaps
    elif (map_type == 'gov'):
        func = get_image_gov
    else:
        print('error *' + map_type + '* dont in map types')
        return

    for cords in images_cords:
        func(cords,zoom)



def set_cords(startcords,endcords,images_num):
    cords_images = []
    x_disntace = startcords[0] - endcords[0]
    y_distance = startcords[1] - endcords[1]
    x_delta = x_disntace/images_num
    y_delta = y_distance/images_num
    for y_index in range(images_num):
        for x_index in range(images_num):
            cords_images.append([(startcords[0]+x_index * x_delta),(startcords[1] + y_index * y_delta)])
    return cords_images


def split_list(lst,split_num):
    return [lst[i:i + split_num] for i in range(0, len(lst), split_num)]

def check_exist_cords(map_type,cords):
    if map_type == 'gov':
        dir = 'gov'
    elif map_type == 'google':
        dir = 'google maps'

    all_cords = os.listdir("./data/"+dir)
    for file in all_cords:
        if(file.split('.png')[0] == str(cords)):
            return True
    return False

def start_threads(threads_num,map_type,startcords,endcords,images_num,zoom):
    thread_function = get_images_cords

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    threads_points = split_list(set_cords(startcords,endcords,images_num),threads_num)
    threads = list()
    for index in range(threads_num):
        logging.info("Main    : create and start thread %d.", index)
        x = threading.Thread(target=thread_function, args=(threads_points[index],map_type,zoom,index,))
        threads.append(x)
        x.start()

    for index, thread in enumerate(threads):
        logging.info("Main    : before joining thread %d.", index)
        thread.join()
        logging.info("Main    : thread %d done", index)

def t():
    threds_num = 2
    image_count = 10
    map_type = 'google'
    zoom = 500

    cords_start = [180485.11,634667.74]
    cords_end = [180685.11,634697.74]

    start_threads(threds_num, map_type, cords_start, cords_end, image_count, zoom)

def main():
    crop_image('/Users/amitisraeli/PycharmProjects/google_maps/data/google maps/[31.8825159, 34.7399199].jpg','google')

if __name__ == '__main__':
    main()
