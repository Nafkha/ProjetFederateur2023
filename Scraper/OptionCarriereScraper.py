import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import mysql.connector
import pytz
import datetime
import dateparser
import time

# fonction pour obtenir les liens d'offres d'emploi sur optioncarriere.tn pour un mot clé donné
def get_job_links(driver, keyword):
    # charger la page d'accueil d'optioncarriere.tn
    driver.get("https://www.optioncarriere.tn/")
    # trouver la barre de recherche et y entrer le mot clé
    driver.find_element(By.ID, "s").send_keys(keyword)
    # simuler la pression de la touche ENTER pour lancer la recherche
    driver.find_element(By.ID, "s").send_keys(Keys.ENTER)
    # trouver l'élément radio par son identifiant
    radio_button = driver.find_element(By.NAME, "sort-output")
    # Déplacer la souris sur l'élément "radio-check"
    action = ActionChains(driver)
    action.move_to_element(radio_button).perform()
    # trouver le bouton de recherche et cliquer dessus pour appliquer le tri par date
    date_button = driver.find_element(By.XPATH, "//label[@for='sort-date']")
    date_button.click()
  
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
        # trouver tous les éléments d'articles contenant les offres d'emploi
        jobs = soup.find_all("article")
        # boucle pour extraire le lien de chaque offre d'emploi et l'ajouter à la liste
        for job in jobs:
            try:
                job_date = soup.select_one("span.badge.badge-r.badge-s").text
                dt = dateparser.parse(
                    job_date, languages=["fr"], settings={"TIMEZONE": "Africa/Tunis"}
                )
                tz = pytz.timezone("Africa/Tunis")
                tz_dt = tz.localize(dt)
                job_date = tz_dt.strftime("%Y-%m-%d")
                if job_date == str(today):  # filtrer par date actuelle
                    link = "https://www.optioncarriere.tn" + job.find("a")["href"]
                    links.append(link)
                else:
                    FIND_TODAY = True  # sortir de la boucle si la date est inférieure à aujourd'hui
            except:
                pass

        try:
            # attendre jusqu'à ce que le bouton "next" pour passer à la page suivante soit présent
            next_page = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'a[rel="next"]'))
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

    # extraire le titre de l'offre d'emploi
    try:
        post_title = soup.find('h1').text.strip()
    except:
        post_title = "Null"

    # extraire le nom de l'entreprise proposant l'offre d'emploi
    try:
        post_company = soup.find('p', class_='company').text.strip()
    except:
        post_company = "Null"

    # extraire la ville ou la région où se trouve l'emploi
    try:
        post_location = soup.find('ul', class_='details').find_all('li')[0].find('span').text.strip()
    except:
        post_location = "Null"

    # extraire le type de contrat proposé (CDI, CDD, etc.)
    try:
        post_contract_type = soup.select_one('ul.details > li:nth-of-type(2)').text.strip()
        post_contract_type
    except:
        post_contract_type = "Null"
        
    # extraire le type d'horaire de travail proposé (temps plein, temps partiel, etc.)
    try:
        post_time_type = soup.select_one('ul.details > li:nth-of-type(3)').text.strip()
    except:
        post_time_type = "Null"
        
    try:
        post_img = soup.select_one("img", {"class": "logo"})['src']
    except:
        post_img = "Null"

    # extraire la date de publication de l'offre d'emploi
    try:
        post_date = soup.select_one('span.badge.badge-r.badge-s').text
        dt = dateparser.parse(post_date, languages=['fr'], settings={'TIMEZONE': 'Africa/Tunis'})
        tz = pytz.timezone('Africa/Tunis')
        tz_dt = tz.localize(dt)
        post_date = tz_dt.strftime('%Y-%m-%d')
    except:
        post_date = None

    # extraire la description de l'offre d'emploi
    try:
        post_description = soup.select_one('section.content').text.strip()
    except:
        post_description = "Null"
    # retourner un dictionnaire contenant les détails de l'offre d'emploi
    job_details = {
        "post_title": post_title,
        "post_company": post_company,
        "post_location": post_location,
        "post_contract_type": post_contract_type,
        "post_time_type": post_time_type,
        "post_date": post_date,
        "post_description": post_description,
        "post_link": link,
        "post_img": post_img
    }
    return job_details

# fonction pour extraire les détails de toutes les offres d'emploi pour un mot clé donné
def scrape_jobs(keyword):
    EMPTY = "non spécifié"
    # initialiser le driver de selenium et le navigateur Chrome
    driver = webdriver.Chrome()
    driver.maximize_window()
    # obtenir les liens d'offres d'emploi pour le mot clé donné
    job_links = get_job_links(driver, keyword)
    print(f"Nombre d'offres d'emploi trouvées pour le mot clé '{keyword}': {len(job_links)}")
    # initialiser une liste pour stocker les détails de toutes les offres d'emploi
    job_details_list = []
    print(job_details_list)
    
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
            sql = "INSERT INTO joboffers_joboffer (Entreprise, Titre, Date, Description, Lieu, Salaire, url, img, Experience, diplome, type_poste) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (job["post_company"], job["post_title"], job["post_date"], job["post_description"], job["post_location"], EMPTY, job["post_link"], job["post_img"], EMPTY, EMPTY, job["post_contract_type"])
            cursor.execute(sql, values)
            print("Offre d'emploi insérée avec succès")
    except:
        db.rollback()
        print("Erreur d'insertion des données dans la table joboffers_joboffer", sys.exc_info()[0])
        

    # validation de la transaction
    db.commit()

    # fermeture de la connexion à la base de données
    db.close()
    
    return job_details_list

if __name__ == "__main__":
    keyword = ""
    posts = scrape_jobs(keyword)
    print("Nombre d'offres d'emploi trouvées : ", len(posts))
    

