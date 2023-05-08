from selenium import webdriver
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.common.by import By  
import time
import mysql.connector

from convertDate import convert_dates_Fab

# CODE A AMELIORER :) 


connection  = mysql.connector.connect(
    user= 'root',
    password = 'admin',
    host = '127.0.0.1',
    database = 'projetfed'
)

def fabskillScrapper(keyword):

    if(connection.is_connected()):
        print("You are connected")

    cursor = connection.cursor()

    add_job = """INSERT INTO poste(entreprise,titre,date,description,lieu,salaire) VALUES(%s,%s,%s,%s,%s,%s)"""



    driver = webdriver.Chrome()
    driver.maximize_window()  
    driver.get("https://fabskill.com/candidate/login") 
    driver.find_element(By.CSS_SELECTOR,"input").send_keys("nafkha.m.youssef@gmail.com")
    driver.find_element(By.CSS_SELECTOR,"input").send_keys(Keys.ENTER)
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR,"input").send_keys("projetFederateur")
    driver.find_element(By.CSS_SELECTOR,"input").send_keys(Keys.ENTER)
    time.sleep(3)

    driver.get("https://fabskill.com")
    time.sleep(3)
    for k in keyword:
        driver.find_element(By.ID,'select-repo-ts-control').send_keys(k)
        time.sleep(.5)
    try:
        driver.find_element(By.CSS_SELECTOR,'[class="fs-6 text-left text-nowrap"]').click()
        time.sleep(2)
    except:
        print("Error")
    finally:

        driver.find_element(By.CSS_SELECTOR,'[class="btn btn-primary w-100 h-100 text-nowrap"]').click()
        time.sleep(1)
    items =  []

    last_height = driver.execute_script("return document.body.scrollHeight")

    itemTargetCount = 150

    while(itemTargetCount > len(items)):
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(1)
        new_height = driver.execute_script("return document.body.scrollHeight")
        last_height = new_height
        elements = driver.find_elements(By.CSS_SELECTOR,'[class="col mt-1"]')
        textElements =  []
        job_titles= []
        job_link= []
        job_dates = []
        entreprise = []
        for element in elements:
            job_titles.append(element.find_element(By.CSS_SELECTOR,'[class="card-title mt-1 mb-75 h3 fs-2"]').text)
            job_link.append(element.find_element(By.CSS_SELECTOR,'[class="card-title mt-1 mb-75 h3 fs-2"]').get_attribute("href"))
            job_dates.append(element.find_elements(By.CSS_SELECTOR,'[class="badge badge-light-secondary mt-50 mr-50"]')[0].text)
            entreprise.append(element.find_element(By.CSS_SELECTOR,'[class="text-primary mt-50"]').text)
            if len(job_titles)>=itemTargetCount:
                break
        items = job_titles
        
        try:
            driver.find_element(By.CSS_SELECTOR,'[class="card text-center w-100 ng-tns-c135-3 ng-star-inserted"]')
            break
        except:
            continue
    job_dates = convert_dates_Fab(job_dates)

    """for job, date,e,l in zip(items,job_dates,entreprise,job_link):
        print(job, " ",date, " ",e," ",l)"""

    salaire = []
    lieu = []
    description = []

    for j in job_link:
        driver.get(j)
        lieu.append(driver.find_element(By.CSS_SELECTOR,'[class="card-text text-secondary"]').text)
        try:
            salaire.append(driver.find_element(By.CSS_SELECTOR,'[class="v-middle   b-none"]').text)
        except:
            salaire.append("Not specified")
        description.append(driver.find_element(By.ID,'description').text.strip("Postuler à l'offre"))
    print(lieu)
    print(salaire)
    print(description[0])

    for e,j,d,desc,l,s in zip(entreprise,items,job_dates,description,lieu,salaire):
        data = (e,j,d,desc,l,s)
        try:
            cursor.execute(add_job,data)
            connection.commit()
            print("Data inserted into the database")
        except:
            print("Data duplicated")
            connection.rollback()
    cursor.close()
    connection.close()