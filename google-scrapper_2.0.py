# -*- coding: utf-8 -*-

import requests
import time
import urllib
import argparse
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pathlib import Path
from lxml.html import fromstring
import os
import sys
from fake_useragent import UserAgent

'''
Commandline based Google Image scrapping. Gets up to 800 images.
Author: Rushil Srivastava (rushu0922@gmail.com)
'''

def search(url):
    # Create a browser and resize for exact pinpoints
    browser = webdriver.Chrome(executable_path=r'C:/Users/Desktop/chromedriver.exe')
    browser.set_window_size(1024, 768)
    print("\n===============================================\n")
    print("[%] Successfully launched Chrome Browser")

    # Open the link
    browser.get(url)
    time.sleep(1)
    print("[%] Successfully opened link.")

    element = browser.find_element_by_tag_name("body")

    print("[%] Scrolling down.")
    # Scroll down
    for i in range(30):
        element.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.3)  # bot id protection

    browser.find_element_by_id("smb").click()
    print("[%] Successfully clicked 'Show More Button'.")

    for i in range(50):
        element.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.3)  # bot id protection

    time.sleep(1)

    print("[%] Reached end of Page.")
    # Get page source and close the browser
    source = browser.page_source
    f = open('dataset/logs/google/source.html', 'w+', encoding='utf-8')
    print('SOURCE')
    f.write(source)

    browser.close()
    print("[%] Closed Browser.")

    return source


def error(link):
    print("[!] Skipping {}. Can't download or no metadata.\n".format(link))
    file = Path("dataset/logs/google/errors.log".format(query))
    if file.is_file():
        with open("dataset/logs/google/errors.log".format(query), "a") as myfile:
            myfile.write(link + "\n")
    else:
        with open("dataset/logs/google/errors.log".format(query), "w+") as myfile:
            myfile.write(link + "\n")


def download_image(link, image_data):
    download_image.delta += 1
    # Use a random user agent header for bot id
    ua = UserAgent()
    headers = {"User-Agent": ua.random}

    # Get the image link
    try:
        # Get the file name and type
        file_name = link.split("/")[-1]
        type = file_name.split(".")[-1]
        type = (type[:3]) if len(type) > 3 else type
        if type.lower() == "jpe":
            type = "jpeg"
        if type.lower() not in ["jpeg", "jfif", "exif", "tiff", "gif", "bmp", "png", "webp", "jpg"]:
            type = "jpg"

        # Download the image
        print("[%] Downloading Image #{} from {}".format(download_image.delta, link))
        try:
            urllib.request.urlretrieve(link,
                                       "dataset/google/{}/".format(query) + query +"_{}.{}".format(str(download_image.delta),
                                                                                             type))
            print("[%] Downloaded File\n")
            with open("dataset/google/{}/{}_{}.json".format(query, query, str(download_image.delta)), "w") as outfile:
                json.dump(image_data, outfile, indent=4)
        except Exception as e:
            download_image.delta -= 1
            print("[!] Issue Downloading: {}\n[!] Error: {}".format(link, e))
            error(link)
    except Exception as e:
        download_image.delta -= 1
        print("[!] Issue getting: {}\n[!] Error:: {}".format(link, e))
        error(link)


if __name__ == "__main__":
    # parse command line options
    parser = argparse.ArgumentParser()
    # parser.add_argument("url", help="Give the url that I should parse.")
    parser.add_argument("keyword", help="Query I should parse.")
    args = parser.parse_args()

        # check directory and create if necessary
    if not os.path.isdir("dataset/"):
        os.makedirs("dataset/")
    if not os.path.isdir("dataset/google/{}".format(args.keyword)):
        os.makedirs("dataset/google/{}".format(args.keyword))
    if not os.path.isdir("dataset/logs/google/".format(args.keyword)):
        os.makedirs("dataset/logs/google/".format(args.keyword))

    # set stack limit
    sys.setrecursionlimit(1000000)

    # get user input and search on google
    query = args.keyword
    query2 = query.replace('_','+')
    url = "https://www.google.fr/search?q="+query2+"&dcr=0&source=lnms&tbm=isch&sa=X&ved=0ahUKEwjJ482eroTZAhXNLVAKHYpbAs8Q_AUICigB&biw=766&bih=284"
    source = search(url)

    # Parse the page source and download pics
    soup = BeautifulSoup(str(source), "html.parser")
    ua = UserAgent()
    headers = {"User-Agent": ua.random}

    try:
        os.remove("dataset/logs/google/errors.log")
    except OSError:
        pass

    # Get the links and image data
    links = soup.find_all("a", class_="rg_l")
    print("[%] Indexed {} Images.".format(len(links)))
    print("\n===============================================\n")
    print("[%] Getting Image Information.\n")
    images = {}
    linkcounter = 0
    for a in soup.find_all("div", class_="rg_meta"):
        r = requests.get("https://www.google.com" + links[linkcounter].get("href"), headers=headers)
        title = str(fromstring(r.content).findtext(".//title"))
        link = title.split(" ")[-1]
        print("\n[%] Getting info on: {}".format(link))
        try:
            image_data = "google", query, json.loads(a.text)["pt"], json.loads(a.text)["s"], json.loads(a.text)["st"], json.loads(a.text)["ou"], json.loads(a.text)["ru"]
            images[link] = image_data
        except Exception as e:
            images[link] = image_data
            print("[!] Issue getting data: {}\n[!] Error: {}".format(image_data, e))

        linkcounter += 1

    # Open i processes to download
    download_image.delta = 0
    for i, (link) in enumerate(links):
        r = requests.get("https://www.google.com" + link.get("href"), headers=headers)
        title = str(fromstring(r.content).findtext(".//title"))
        link = title.split(" ")[-1]
        try:
            download_image(link, images[link])
        except Exception as e:
            error(link)

    print("[%] Done. Downloaded {} images.".format(download_image.delta))
    print("\n===============================================\n")
