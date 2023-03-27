import requests
from bs4 import BeautifulSoup
import datetime
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from termcolor import colored
import sys


# Hier wird die URL definiert, die du überprüfen möchtest.
url = sys.argv[1]
url=url+"/about"

# Starte den Webdriver
driver = webdriver.Chrome()

# Lade die Seite
driver.get(url)

# Warte bis die Seite vollständig geladen ist
wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "channel-panels-container")))

#Warte damit der Content geladen wird.
time.sleep(1)

# Hole den HTML-Code der Seite
html = driver.page_source

soup = BeautifulSoup(html, "html.parser")
links = soup.find_all("a")
check_links=[]
print("----------Found Links on Twitch---------")
for link in links:
    if "twitter." in link["href"] or "discord." in link["href"] or "instagram." in link["href"] or "youtube." in link["href"] or "tiktok." in link["href"]:
        if link["href"] not in check_links:
            check_links.append(link["href"])
            print(link["href"])
        else:
            print("Link bereits in Liste.")
print("------Checking Social Media Links-------")

for link in check_links:
    # Lade die Seite
    driver.get(link)
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
                print("Die Seite '{link}' ist aktuell.")
            else:
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
                print(colored(f"Die Seite enthält das Schlüsselwort '{keyword}'.", 'red'))
                break

        if outdated==True:
            print(colored(f"[Seite '{link}' ist wahrscheinlich veraltet.]", 'red'))
            
        else:
            print(colored("[Seite ist nicht veraltet]", 'green'))
        
    else:
        print(colored(f"Die Seite '{link}' ist nicht verfügbar oder du bist gesperrt worden.", 'red'))
    print("-------------------")

# Schließe den Webdriver
driver.quit()
