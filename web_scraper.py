import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime
import time
import re
import pandas as pd

#data structure to store scraping results
current_movies = []
director = []
casts = []
metascore = []
rating = []
year =[]
#existed = []

#monitoring
start_time = None
end_time = None

#split movie name and published year
def split(title):
    res = title.split("(")
    t = res[0]
    return t

#print results of web scraping
def print_frame():
    test_df = pd.DataFrame({
    'movie':current_movies,
    'director':director,
    'casts':casts,
    'metascore':metascore,
    'imdb':rating,
    'year':year
    })
    print(test_df.info)

#monitor function to count time and reload data after 24 hours
def main():
    start_time = time.time()
    load_data()
    end_time = time.time()
    print("Cost ",end_time-start_time," seconds")
    while(True):
        #Set time as 60 seconds for test
        time.sleep(60)
        start_time = time.time()
        load_data()
        end_time = time.time()
        print("Cost ",end_time-start_time," seconds")


#using BeautifulSoup to find all appropriate tags, then extract data from ResultSet
def load_data():
    link = "https://www.imdb.com/movies-coming-soon/"
    html = urllib.request.urlopen(link).read()
    soup = BeautifulSoup(html,"html.parser")
    materials = soup.find_all('div',class_="list_item")
    count = 0 #index
    meta = 0
    if(len(materials)>=1):
        #existed = [True] * len(materials)
        while count<len(materials):
            name = split(materials[count].find('h4', itemprop="name").text)
            url = materials[count].find('h4', itemprop="name").a.get('href')
            if(materials[count].find('span',class_="metascore") is not None):
                meta = materials[count].find('span',class_="metascore").text
            else: meta = None
            direct = materials[count].find('span',itemprop="name").text
            #check duplicated movies in list
            if(name not in current_movies):
                current_movies.append(name)
                director.append(direct[1:])
                metascore.append(meta)
                url_seek(url)
                rt,ca,ye = url_seek(url)
                rating.append(rt)
                casts.append(ca)
                year.append(ye)
                count+=1
            else: count+=1
    print_frame()

#seeking for more data from the url of each movie
def url_seek(url):
    url = "https://www.imdb.com/" + url
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html,"html.parser")
    m = soup.find_all('div',class_="title-overview")
    if(m[0].find('span',itemprop="ratingValue") is not None):
        rt = m[0].find('span',itemprop="ratingValue").text
    else: rt = None
    cast = ""
    table = soup.findAll(attrs={'id':'titleCast'})
    ca = table[0].findAll('span',itemprop="name")
    for x in ca:
        cast = cast + x.text + ","
    cast = cast[:-1]
    dt = m[0].find('meta',itemprop="datePublished").get('content')
    time_arr = dt.split('-')
    return rt,cast,time_arr[0]


#1.add metascore,directors from current homepage
#2.add rating,published time,casts from url
#3.using panda to make columns of data
#4.writing a main function to monitor time of runnning


if __name__== "__main__":
    main()
