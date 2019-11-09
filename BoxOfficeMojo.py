# Arnab Sen Sharma (arnab-api)
# Lecturer, Department of CSE
# Shahjalal University of Science and Technology

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
import time
import json
import re
import os

url_root = "https://www.boxofficemojo.com/"
driver = None

def simplify_string(inp):
    inp = inp.lower().strip()
    inp = re.sub(r'[^A-Za-z0-9]', '_', inp)

    return inp

def makeDirectory(path):
    print("creating directory " + path)
    try:
        os.mkdir(path)
    except FileExistsError:
        pass

def initialize(url, browser=None):
    if(browser == None):
        browser = webdriver.Chrome()
        browser.implicitly_wait(3)
    browser.get(url)
    browser.implicitly_wait(3)

    return browser

def getSingleMovieSummary(mov):
    td_arr = mov.findAll('td')
    href = td_arr[1].find('a')['href']
    # print(href)

    name = td_arr[1].find('a').contents[0].strip()
    name = simplify_string(name)
    # print(name)

    world_wide = td_arr[2].contents[0].strip()
    # print(world_wide)

    domestic = td_arr[3].contents[0].strip()
    # print(domestic)

    foreign = td_arr[5].contents[0].strip()
    # print(foreign)

    return {
        'href'      : href,
        'name'      : name,
        'world_wide': world_wide,
        'domestic'  : domestic,
        'foreign'   : foreign
    }

def getSingleWeekSummary(week):
    td_arr = week.findAll('td')
    rng = td_arr[0].find('a').contents[0].strip()
    # print(rng)
    rnk = td_arr[1].contents[0].strip()
    # print(rnk)
    weekly = td_arr[2].contents[0].strip()
    # print(weekly)
    lw = td_arr[3].contents[0].strip()
    # print(lw)
    theaters = td_arr[4].contents[0].strip()
    # print(theaters)
    change = td_arr[5].contents[0].strip()
    # print(change)
    avg = td_arr[6].contents[0].strip()
    # print(avg)
    todate = td_arr[7].contents[0].strip()
    # print(todate)
    week = td_arr[8].contents[0].strip()
    # print(week)

    return {
        'range': rng,
        'rank': rnk,
        'weekly': weekly,
        'lw': lw,
        'theaters': theaters,
        'change': change,
        'avg': avg,
        'todate': todate,
        'week': week
    }

def performClick(element):
    driver.execute_script("arguments[0].click();", element)

##############################################################
year = str(2011)
url = url_root + 'year/world/'+year+'/?grossesOption=totalGrosses'
print("\n\n############### YEAR {} ###############\n\n".format(year))
path = 'BoxOfficeMojo/'+year
makeDirectory(path)

driver = initialize(url)
##############################################################


table = driver.find_element_by_xpath('//*[@id="table"]/div/table[2]/tbody')

html = table.get_attribute('innerHTML')
soup = BeautifulSoup(html, 'html.parser')
movie_elem = soup.findAll('tr')
movie_elem = movie_elem[1:]

summary_json = []
for movie in movie_elem:
    data = getSingleMovieSummary(movie)
    print(data)
    summary_json.append(data)

with open(path + '/0_summary.json', 'w') as f:
    json.dump(summary_json, f)
print("saved summary")

movie_data = {
        "href": "/release/rl709199361/?ref_=bo_ydw_table_1",
        "name": "the_avengers",
        "world_wide": "$1,518,812,988",
        "domestic": "$623,357,910",
        "foreign": "$895,455,078"
    }

# with open(path+"/0_summary.json") as f:
#     summary_json = json.load(f)

print("\n\n############### Scraping Movies ###############\n\n")

first = True

for i in range(0, len(summary_json)):

    movie_data = summary_json[i]
    print("\n\n############### {} ###############\n\n".format(str(i+1) + "_" + movie_data['name']))


    url = url_root + movie_data['href']
    if(driver): 
        driver = initialize(url, driver)
    else:
        driver = initialize(url)

    if(first):
        time.sleep(1)
        actions = ActionChains(driver)
        actions.move_by_offset(100,100)
        actions.click().perform()
        print('clicked')
        driver.implicitly_wait(3)

        first = False
    
    try:
        time.sleep(1)
        weekly = driver.find_element_by_link_text('Domestic Weekly')
        # weekly.click()
        performClick(weekly)
        driver.implicitly_wait(3)
    except:
        print("This movie does not have weekly information available")
        continue
        pass


    table = driver.find_element_by_xpath('//*[@id="table"]/div/table[2]/tbody')
    html = table.get_attribute('innerHTML')
    soup = BeautifulSoup(html, 'html.parser')

    week_elem = soup.findAll('tr')
    week_elem = week_elem[1:]
    # print(week.prettify())

    weekly_income = []
    for week in week_elem:
        data = getSingleWeekSummary(week)
        print(data)
        weekly_income.append(data)

    with open(path + '/' + str(i+1) + "_" + movie_data['name'] +'.json', 'w') as f:
        json.dump(weekly_income, f)