from KeejobsScrapper import keejobScrapper
from FabSkillsScrapper import fabskillScrapper
from colorama import Fore
import time
import datetime
#Keyword = input("Donner keyword ")

import datetime

file = open(r'C:\Users\nafkh\OneDrive\Bureau\ProjetFederateur\testSelenium\log.txt','a')

file.write(f'Started : {datetime.datetime.now()} \n')

print(f'{Fore.GREEN}{"Keejob Scrapper":+^99}')
print(f'{Fore.RESET}')

time.sleep(3)

print(f'{Fore.CYAN}')
keejobScrapper()
print(f'{Fore.RED}')
print(f'{"Finished Scrapping":+^99}')
print(f'{Fore.RESET}')
time.sleep(2)
file.write(f'Ended : {datetime.datetime.now()} \n')



#fabskillScrapper(Keyword)
