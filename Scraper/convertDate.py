from datetime import datetime
from datetime import date

# Liste de dates en français
dates = ['25 janvier 2022', '10 février 2022', '15 mars 2022']

# Fonction pour convertir le mois en français en mois en anglais
def convert_month(month):
    # Crée une liste des noms de mois en français
    french_months = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']
    # Crée une liste des noms de mois en anglais
    english_months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    # Trouve l'indice du mois en français dans la liste
    index = french_months.index(month.lower())
    # Retourne le mois en anglais correspondant
    return english_months[index]
def convert_month_Fab(month):
    # Crée une liste des noms de mois en français
    french_months = ['janv.', 'févr.', 'mars', 'avr.', 'mai', 'juin', 'juillet', 'août', 'sept.', 'oct.', 'nov.', 'déc.']
    # Crée une liste des noms de mois en anglais
    english_months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    # Trouve l'indice du mois en français dans la liste
    index = french_months.index(month.lower())
    # Retourne le mois en anglais correspondant
    return english_months[index]

def convert_dates_Fab(dates):
    converted_date = []
    # Boucle pour parcourir chaque date et convertir le mois


    for date in dates:
        # Sépare la date en jour, mois et année
        day, month, year = date.split()
        # Convertit le mois en anglais
        month = convert_month_Fab(month)
        # Affiche la date avec le mois en anglais
        english_date = day+" "+ month+" "+year
        dt = datetime.strptime(english_date,"%d %B %Y")
        mysql_Date = dt.strftime("%Y-%m-%d")
        converted_date.append(mysql_Date)
    return converted_date
def convert_dates(dates):
    converted_date = []
    # Boucle pour parcourir chaque date et convertir le mois


    for date in dates:
        # Sépare la date en jour, mois et année
        day, month, year = date.split()
        # Convertit le mois en anglais
        month = convert_month(month)
        # Affiche la date avec le mois en anglais
        english_date = day+" "+ month+" "+year
        dt = datetime.strptime(english_date,"%d %B %Y")
        mysql_Date = dt.strftime("%Y-%m-%d")
        converted_date.append(mysql_Date)
    return converted_date
def convert_single_date(date):
    converted_date = None
    # Boucle pour parcourir chaque date et convertir le mois


    day, month, year = date.split()
    month = convert_month(month)
    english_date = day+" "+ month+" "+year
    dt = datetime.strptime(english_date,"%d %B %Y")
    mysql_Date = dt.strftime("%Y-%m-%d")
    converted_date= mysql_Date
    return converted_date
def convert_num_date(date):
    dt = datetime.strptime(date,"%d/%m/%Y")
    mysql_Date = dt.strftime("%Y-%m-%d")
    return mysql_Date
def isToday(post_date):
    today = str(date.today())
    
    #print(today, "      ",post_date)
    if(post_date == today):
        return True
    else:
        return False
