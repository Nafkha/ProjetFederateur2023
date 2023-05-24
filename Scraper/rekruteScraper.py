import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from bs4 import BeautifulSoup
import mysql.connector
import re
import pytz
import datetime
import dateparser
import time

# fonction pour obtenir les liens d'offres d'emploi sur rekrute.com pour un mot clé donné
def get_job_links(driver, keyword):
    # charger la page d'accueil d'optioncarriere.tn
    driver.get("https://www.rekrute.com/")
    # trouver la barre de recherche et y entrer le mot clé
    driver.find_element(By.ID, "keyword").send_keys(keyword)
    # simuler la pression de la touche ENTER pour lancer la recherche
    driver.find_element(By.ID, "keyword").send_keys(Keys.ENTER) 
    # initialiser une liste pour stocker les liens d'offres d'emploi
    links = []
    # obtenir la date actuelle
    today = datetime.date.today()
    FIND_TODAY = False
    
    # boucle pour parcourir toutes les pages de résultats de recherche
    while not FIND_TODAY: 
        # récupérer le contenu HTML de la page de résultats de recherche
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        # trouver tous les éléments titreJob contenant les offres d'emploi
        jobs = soup.find_all("div", {"class": "col-sm-10 col-xs-12"})
        # boucle pour extraire le lien de chaque offre d'emploi et l'ajouter à la liste
        for job in jobs:
            try:
                job_date = soup.find('em', class_='date').find_all('span')[0].text
                dt = dateparser.parse(
                    job_date, languages=["fr"], settings={"TIMEZONE": "Africa/Tunis"}
                )
                tz = pytz.timezone("Africa/Tunis")
                tz_dt = tz.localize(dt)
                job_date = tz_dt.strftime("%Y-%m-%d")
                if job_date == str(today):  # filtrer par date actuelle
                    link = "https:/www.rekrute.com" + job.find("a")["href"]
                    links.append(link)
                else:
                    FIND_TODAY = True  # sortir de la boucle si la date est inférieure à aujourd'hui
            except:
                pass
        try:
            # attendre jusqu'à ce que le bouton "next" pour passer à la page suivante soit présent
            next_page = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a.next"))
            )
            # obtenir le lien de la page suivante et la charger
            next_page = next_page.get_attribute("href")
            driver.get(next_page)
        except:
            # arrêter la boucle si le bouton "next" n'est plus présent (fin de la pagination)
            break

    return links

# fonction pour extraire les détails d'une offre d'emploi à partir de son lien
def get_job_details(driver, link):
    # charger la page de l'offre d'emploi
    driver.get(link)
    # récupérer le contenu de la page
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    
    try:
        post_title = soup.find('h1').text.strip()
    except:
        post_title = "Null"
    
    try:
        post_location = driver.find_element(By.CSS_SELECTOR, "ul.featureInfo li:nth-child(2)").text.split(" sur ")[1]
    except:
        post_location = "Null"
    
    try:
        post_experience = soup.select_one('ul.featureInfo li:nth-child(1)').text.strip()
        post_experience = " ".join(post_experience.split())
    except:
        post_experience = "Null"
    
    try:
        post_education = soup.select_one('ul.featureInfo li:nth-child(3)').text.strip()
        post_education = " ".join(post_education.split())
    except:
        post_education = "Null"
    
    try:
        post_contract_type = soup.select_one('span.tagContrat').text.strip()
    except:
        post_contract_type = "Null"

    try:
        elements = driver.find_elements(By.CSS_SELECTOR, "div.col-md-12.blc")
        post = elements[4].text
        profil = elements[5].text
        post_description = post + "\n" + profil
        post_description = " ".join(post_description.split())
    except:
        post_description = "Null"
    try:
        post_date_text = soup.select_one('span.newjob').text
        post_date = re.search(r"il y a \d+ jour", post_date_text).group(0)
        dt = dateparser.parse(post_date, languages=['fr'], settings={'TIMEZONE': 'Africa/Tunis'})
        tz = pytz.timezone('Africa/Tunis')
        tz_dt = tz.localize(dt)
        post_date = tz_dt.strftime('%Y-%m-%d')
    except:
        today = datetime.date.today()
        today = today.strftime('%Y-%m-%d')
        post_date = today
    
    try:
        company_URL = driver.find_element(By.CSS_SELECTOR, "div.listImg a").get_attribute("href")
        driver.get(company_URL)
        time.sleep(1)
        post_company = driver.find_element(By.CSS_SELECTOR, "span a").text
    except:
        post_company = "Null"
        
    try:
        post_sector = driver.find_element(By.CSS_SELECTOR, "p:nth-child(2) span a").text
    except:
        post_sector = "Null"
        
    try:
        post_img = "https:/www.rekrute.com" + soup.find('img')['src']
    except:
        post_img = "https://static.careerjet.org/images/flags/tn.svg"    
    job_details = {
        "post_title": post_title,
        "post_company": post_company,
        "post_sector": post_sector,
        "post_location": post_location,
        "post_experience": post_experience,
        "post_education": post_education,
        "post_contract_type": post_contract_type,
        "post_date": post_date,
        "post_description": post_description,
        "post_link": link,
        "post_img": post_img
    }
    
    return job_details

def scrape_jobs(keyword):
    EMPTY = "non spécifié"
    # initialiser le driver de selenium et le navigateur Chrome
    driver = webdriver.Chrome()
    driver.maximize_window()
    # obtenir les liens d'offres d'emploi pour le mot clé donné
    job_links = get_job_links(driver, keyword)
    # initialiser une liste pour stocker les détails de toutes les offres d'emploi
    job_details_list = []
    
    # boucle pour extraire les détails de chaque offre d'emploi à partir de son lien
    for link in job_links:
        job_details = get_job_details(driver, link)
        job_details_list.append(job_details)
        time.sleep(1)

    # fermer le driver de selenium et le navigateur
    driver.close()
    # connexion à la base de données
    try:
      db = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="admin",
        database="projetfederateur"
      )
      cursor = db.cursor()
    except:
      print("Erreur de connexion à la base de données")

    # insertion des données dans la table "joboffers_joboffer"
    try:
        for job in job_details_list:
            sql = "INSERT INTO joboffers_joboffer (Entreprise, Titre, Date, Description, Lieu, Salaire, url, img, Experience, diplome, type_poste,SalaireMin,SalaireMax) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,'NS','NS')"
            values = (job["post_company"], job["post_title"], job["post_date"], job["post_description"], job["post_location"], EMPTY, job["post_link"], job["post_img"], job["post_experience"], job["post_education"], job["post_contract_type"])
            cursor.execute(sql, values)
            print("Offre d'emploi insérée avec succès")
    except:
        db.rollback()
        print("Erreur d'insertion des données dans la table joboffers_joboffer", sys.exc_info())

    # validation de la transaction
    db.commit()

    # fermeture de la connexion à la base de données
    db.close()

    return job_details_list

if __name__ == "__main__":
    keyword = ""
    posts = scrape_jobs(keyword)
    print("Nombre d'offres d'emploi trouvées : ", len(posts))
