from selenium import webdriver
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.common.by import By  
import time
import mysql.connector

from convertDate import convert_dates
from convertDate import convert_single_date
from convertDate import convert_num_date
from convertDate import isToday
file_o = open(r'C:\Users\nafkh\OneDrive\Bureau\ProjetFederateur\testSelenium\log_1.txt','a')
def keejobScrapper():
    
    file_o.write(f'Started \n')

    connection  = mysql.connector.connect(
        user= 'root',
        password = 'admin',
        host = '127.0.0.1',
        database = 'projetfederateur'
    )

    if(connection.is_connected()):
        print("You are connected")

    cursor = connection.cursor()
    driver = webdriver.Chrome()
    driver.maximize_window()  
    driver.get("https://www.keejob.com/offres-emploi/")
    still_pages = True
    page_number = 1
    scraped_posts = 0
    while still_pages:
        page_to_back = driver.current_url
        jobs = driver.find_elements(By.CSS_SELECTOR,'[class="span8"]')
        entreprises = driver.find_elements(By.CSS_SELECTOR,'[class="span12 no-margin-left"]')
        post_date = driver.find_elements(By.CSS_SELECTOR,'[class="meta_a"]')
        posts = []
        select_req = """SELECT ENTREPRISE,TITRE FROM joboffers_joboffer WHERE (Entreprise=%s AND Titre=%s)"""
        for j,e,d in zip(jobs,entreprises,post_date):
            try:
                data = (e.find_element(By.TAG_NAME,'a').text,j.text)
            except:
                data = ("Entreprise Anonyme",j.text)
            cursor.execute(select_req,data)
            res = cursor.fetchone()
            file_o.write(f'{data[0]}  {convert_num_date(d.text)}\n')
            if(not isToday(convert_num_date(d.text))):
                still_pages = False
                break
            if(not res) and  (not data[0].startswith("Entreprise Anonyme")):
                posts.append(j.find_element(By.TAG_NAME,'a').get_attribute("href"))
                scraped_posts+=1;
        if len(posts)>0:
            scrap_posts(posts,connection,cursor,driver)
            driver.get(page_to_back)
        pagination  = driver.find_elements(By.CSS_SELECTOR,'li.page-item')

        if pagination[-1].get_attribute("class") == "page-item disabled":
            print("FINAL PAGE")
            print("Scrapped : ",page_number," pages")
            still_pages = False
            break
        if still_pages:
            pagination[len(pagination)-2].find_element(By.TAG_NAME,'a').click()
        else:
            print("Scrapped : ",page_number," pages")
        page_number+=1
    file_o.write(f' scraped {scraped_posts} job offers \n')

def scrap_posts(posts,connection,cursor,driver):
        add_job = """INSERT INTO joboffers_joboffer(entreprise,titre,date,description,lieu,salaire,url,img,Experience,diplome,type_poste) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""


        for p in posts:
            driver.get(p)
            time.sleep(1)
            details = driver.find_elements(By.CSS_SELECTOR,'div.meta')
            current_salaire = "Not Specified"
            Experience = "Pas necessaire"
            Diplome = "Pas necessaire"
            Type_Poste = "sivp"

            for d in details:
                if(d.text.startswith("Lieu de travail:")):
                    lieu_travail=d.text.split('\n')[-1]
                if(d.text.startswith("Rémunération proposée:")):
                    current_salaire = d.text.split('\n')[-1]
                if(d.text.startswith("Expérience:")):
                    Experience = d.text.split('\n')[-1]
                if(d.text.startswith("Étude:")):
                    Diplome = d.text.split('\n')[-1]
                if(d.text.startswith("Type de poste:")):
                    Type_Poste = d.text.split('\n')[-1]


        
            date_publication=details[1].text.split('\n')[-1]
            job_title=driver.find_element(By.CSS_SELECTOR,'h2.job-title').text
            entreprise=driver.find_element(By.CSS_SELECTOR,'div.span9.content').find_element(By.TAG_NAME,'b').text
            descriptions=driver.find_element(By.CSS_SELECTOR,'div.block_a.span12.no-margin-left').text.rsplit(' ', 1)[0]
            logo = driver.find_element(By.CSS_SELECTOR,'figure.span3.img-polaroid').find_element(By.TAG_NAME,'img').get_attribute('src')
            print(logo)
            date_publication = convert_single_date(date_publication)

            data = (entreprise,job_title,date_publication,descriptions,lieu_travail,current_salaire,p,logo,Experience,Diplome,Type_Poste)
            try:
                cursor.execute(add_job,data)
                connection.commit()
                print("Data inserted into the database")
                file_o.write(f'Work Inserted into database \n')
            except:
                print(data[0]," ",data[1])
                #print("Data duplicated")
                connection.rollback()
                
        
        return True
        cursor.close()
        connection.close()