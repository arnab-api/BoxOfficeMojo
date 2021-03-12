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

PATH = "/home/arnab/Codes/Libs/chromedriver_linux64/chromedriver"
url_root = "https://www.boxofficemojo.com/"
driver = None

def simplify_string(inp):
    inp = inp.lower().strip()
    inp = re.sub(r'[^A-Za-z0-9]', '_', inp)

    return inp

def initialize(url, browser=None):
    if(browser == None):
        browser = webdriver.Chrome(PATH)
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
        'range'     : rng,
        'rank'      : rnk,
        'weekly'    : weekly,
        'lw'        : lw,
        'theaters'  : theaters,
        'change'    : change,
        'avg'       : avg,
        'todate'    : todate,
        'week'      : week
    }

def performClick(element):
    driver.execute_script("arguments[0].click();", element)

# summary_json = [
#     {
#         "href": "/releasegroup/gr3764736517/?ref_=bo_ydw_table_1",
#         "name": "star_wars__episode_viii___the_last_jedi",
#         "world_wide": "$1,332,539,889",
#         "domestic": "$620,181,382",
#         "foreign": "$712,358,507"
#     }
# ]



def getInfo(text_arr, field, attr = 1):
    if(field not in text_arr):
        return ":("
    idx = text_arr.index(field)
    # print("------------>>", idx)
    beg = idx + 1
    return text_arr[beg : beg + attr]

def parseGeneralInfo(text_arr):
    info = {}
    info["Distributor"] = getInfo(text_arr, "Distributor")[0]
    info["Opening"] = getInfo(text_arr, "Opening")[0]
    info["Budget"] = getInfo(text_arr, "Budget")[0]
    info["Release Date"] = getInfo(text_arr, "Release Date", 3)
    info["MPAA"] = getInfo(text_arr, "MPAA")[0]
    genres = getInfo(text_arr, "Genres")[0].split()
    for i in range(len(genres)):
        genres[i] = genres[i].strip()
    info["Genres"] = genres
    info["In Release"] = getInfo(text_arr, "In Release")[0]
    info["Widest Release"] = getInfo(text_arr, "Opening")[0]

    return info

summary_json = [
    {
        "href": "/releasegroup/gr2104709637/?ref_=bo_ydw_table_50",
        "name": "from_vegas_to_macau_iii",
        "world_wide": "$181,732,879",
        "domestic": "-",
        "foreign": "$181,732,879"
    }
]

first = True

import datetime
def get_weekly_income(driver):
    try:
        time.sleep(1)

        domestic = driver.find_element_by_xpath('//*[@id="a-page"]/main/div/div[4]/div/div/table[1]/tbody/tr[3]/td[1]/a')
        # print(domestic)
        performClick(domestic)
        driver.implicitly_wait(3)

        weekly = driver.find_element_by_link_text('Domestic Weekly')
        # weekly.click()
        performClick(weekly)
        driver.implicitly_wait(3)
    except:
        print("This movie does not have weekly information available")
        return "N/A -- checked on {}".format(datetime.datetime.now())


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

    return weekly_income

def get_gen_info(driver):
    gen_info_table = driver.find_element_by_xpath('//*[@id="a-page"]/main/div/div[3]/div[4]')
    gen_html = gen_info_table.get_attribute('innerHTML')
    gen_soup = BeautifulSoup(gen_html, 'html.parser')
    # print(gen_soup.prettify())
    text_arr = gen_soup.findAll(text=True)
    # print(text_arr)
    for i in range(len(text_arr)):
        text_arr[i] = text_arr[i].strip()
        # print(i, text_arr[i].strip())

    gen_info = parseGeneralInfo(text_arr)

    return gen_info

for i in range(0, len(summary_json)):

    movie_data = summary_json[i]
    print("\n\n############### {} ############### {}/{}\n\n".format(str(i+1) + "_" + movie_data['name'], i+1, len(summary_json)))


    url = url_root + movie_data['href']
    if(driver): 
        driver = initialize(url, driver)
    else:
        driver = initialize(url)

    # if(first):
    #     time.sleep(1)
    #     actions = ActionChains(driver)
    #     actions.move_by_offset(100,100)
    #     actions.click().perform()
    #     print('clicked')
    #     driver.implicitly_wait(3)

    #     first = False
    
    weekly_income = get_weekly_income(driver)
    gen_info = get_gen_info(driver)

    movie_info = {
        "General Info"  : gen_info,
        "Weekly Income" : weekly_income 
    }
    print(movie_info)

