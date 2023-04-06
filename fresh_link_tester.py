import requests
from bs4 import BeautifulSoup
import datetime
from selenium import webdriver
import time
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from termcolor import colored
import sys
import re

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])





def run_tester(url, debug):
    if url == "":
        exit()
    url=url+"/about"
    
    
    # Starte den Webdriver
    driver = webdriver.Chrome(options=options)

    # Lade die Seite
    driver.get(url)

    # Warte bis die Seite vollständig geladen ist
    wait = WebDriverWait(driver, 10)
    try:
        element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "channel-panels-container")))
    except selenium.common.exceptions.TimeoutException:
        print("could not load twitch panel page")
        return

    #Warte damit der Content geladen wird.
    time.sleep(1)

    # Hole den HTML-Code der Seite
    html = driver.page_source

    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all("a")
    check_links=[]
    print("----------Found Social Links on Profile---------")
    for link in links:
        if "twitter." in link["href"] or "discord." in link["href"] or "instagram." in link["href"] or "youtube." in link["href"] or "tiktok." in link["href"]:
            if link["href"] not in check_links:
                check_links.append(link["href"])
                if debug == True:
                    print(link["href"])
            else:
                if debug == True:
                    print("Link bereits in Liste.")
    print("----------Checking Social Media Links---------")

    dead_links=[]
    dead_links_count=0
    for link in check_links:
        # Lade die Seite
        driver.get(link)
        if debug == True:
            print(f"'{link}' wird ueberprueft.")
        # Warte bis die Seite vollständig geladen ist
        wait = WebDriverWait(driver, 10)
        if "discord." in link:
            element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "centeringWrapper-dGnJPQ")))
            time.sleep(1)
            
        if "twitter." in link:
            element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "css-1dbjc4n")))
            time.sleep(1)
            
        # Hole den HTML-Code der Seite
        html = driver.page_source
        

        # Hier wird die Seite abgerufen und der HTML-Code extrahiert.
        r = requests.get(link)

        if r.status_code == 200:
            soup = BeautifulSoup(html, "html.parser")
                # Remove noscript element
            noscript = soup.find("noscript")
            if noscript:
                noscript.decompose()
            # Hier wird das Datum der letzten Aktualisierung der Seite extrahiert.
            last_updated = soup.find("time", {"class": "updated"})

            if last_updated is not None:
                last_updated = last_updated.text
                # Hier wird das aktuelle Datum und die Uhrzeit erfasst.
                now = datetime.datetime.now()

                # Hier wird das Datum der letzten Aktualisierung in ein datetime-Objekt umgewandelt.
                last_updated_datetime = datetime.datetime.strptime(last_updated, "%Y-%m-%d %H:%M:%S")

                # Hier wird die Differenz zwischen dem aktuellen Datum und dem Datum der letzten Aktualisierung berechnet.
                difference = now - last_updated_datetime

                # Hier wird überprüft, ob die Seite innerhalb der letzten 30 Tage aktualisiert wurde.
                if difference.days <= 30:
                    if debug == True:
                        print("Die Seite '{link}' ist aktuell.")
                else:
                    if debug == True:
                        print(f"Dein Link zu deinem {url}-Link ist nicht mehr aktuell.")

            # Hier wird der Inhalt der Website extrahiert und nach Schlüsselwörtern durchsucht.
            content = soup.get_text()

            keywords_de = ["nicht verfügbar", "gelöscht", "nicht gefunden", "gibt es nicht", "abgelaufen", "ungültig", "existiert nicht"]
            keywords_en = ["not available", "deleted", "not found"]
            keywords_es = ["no disponible", "eliminado", "no encontramos"]
            keywords_fr = ["pas disponible", "supprimé", "introuvable"]

            outdated=False
            for keyword in keywords_de + keywords_en + keywords_es + keywords_fr:
                if keyword in content:
                    outdated=True
                    if debug == True:
                        print(colored(f"Die Seite enthält das Schlüsselwort '{keyword}'.", 'red'))
                    break

            if outdated==True:
                if debug == True:
                    print(colored(f"[Seite '{link}' ist wahrscheinlich veraltet.]", 'red'))
                else:
                    dead_links.append(link)
                    dead_links_count+=1
            else:
                if debug == True:
                    print(colored("[Seite ist nicht veraltet]", 'green'))
            
        else:
            if debug == True:
                print(colored(f"Die Seite '{link}' ist nicht verfügbar oder du bist gesperrt worden.", 'red'))
        if debug == True:
            print("-------------------")

    url=url.split("www.twitch.tv/")[1].split("/")[0]  
    print("----------Summary----------")
    if dead_links_count==0:
        print(colored(f"[{url}] Alle Links sind aktuell.", 'green'))
    else:
        print(colored(f"[{url}] {dead_links_count} Links sind veraltet.", 'red'))
        print(colored(f"[{url}] Veraltete Links: {dead_links}", 'red'))
    print("---------------------------")
            

    # Schließe den Webdriver
    driver.quit()

def load_streams(url):
    # Starte den Webdriver
    driver = webdriver.Chrome(options=options)

    # Lade die Seite
    driver.get(url)

    # Warte bis die Seite vollständig geladen ist
    wait = WebDriverWait(driver, 10)
    time.sleep(1)
    try:
        element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "bYReYr")))
    except selenium.common.exceptions.TimeoutException:
        print("could not find layout")
        return

    #Warte damit der Content geladen wird.
    time.sleep(1)

    # Hole den HTML-Code der Seite
    html = driver.page_source

    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all("p")
    #print(links)
    check_links=[]
    print("----------Found Streams on Twitch---------")
    for link in links:
        if link.find('a'):
            continue
        if "jiepBC" in link["class"]:
            username=link.getText()
            sfxname=re.search("\((.*?)\)", username)
            if sfxname:
                username=sfxname.group(1)
            if username not in check_links:
                check_links.append(username)
                print(username)
            else:
                print("Streamer bereits in Liste.")
    driver.quit()
    print("------Checking Social Media Links for each Stream-------")
    for link in check_links:
        print("----------Checking "+link + "---------")
        run_tester("https://www.twitch.tv/"+link, False)

while(1):
    url = input("Enter the twitch-profile-url (twitch.tv/[username]): ")
    if "https://www.twitch.tv/directory/" in url:
        load_streams(url)
        exit()
    run_tester(url, True)
