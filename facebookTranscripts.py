# You can use quotes or other boolean operators within the query.
# The output file will likely break if opened in Excel. This is due to the fact that a single Excel cell cannot contain more than 32.7xx characters,
# so if you have 40.000 characters in the transcript it will be broken into more lines, affecting readability of the file. So I recommend searching and reading
# through the file within a framework like Pandas.
# Even though most indexed videos do contain a transcript, some will not. In this case, the cell will be empty.

import requests
from bs4 import BeautifulSoup
import json
import csv

item = input("Type the object of your research (if needed, between quotes): ")
searchHeaders = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1467.0 Safari/537.36'}
baseUrl = "https://www.google.com/search?q="
operator = "%20site:facebook.com/*/videos"
numResults = "&num=100"
file = "facebook_transcripts.csv"
startPage = "&start="

videos = []

def search():
    print("\n","[*] Searching videos for: "+item,"\n")
    start = ['0','100','200','300']
    for startPoint in start:
        query = baseUrl+item+operator+numResults+startPage+str(startPoint)
        response = requests.get(query, headers=searchHeaders)
        soup = BeautifulSoup(response.content, "html.parser")
        resultsBlock = soup.find_all('div', attrs={'class': 'g'})
        for result in resultsBlock:
            link = result.find('a', href=True)
            if link:
                link = link['href']
                if "videos" in link:
                    videos.append(link)

def getData():   
    with open(file,'w', newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter = "|")
        head = ['Date','Author','Comments','Source','Language','Transcript']
        writer.writerow(head)        
        headers = {'User-agent':'Mozilla/5.0 (compatible; Googlebot/2.1; http://www.google.com/bot.html)'}        
        for video in set(videos):
            print("[-] Extracting video published by: "+author)
            r = requests.get(video, headers=headers)    
            soup = BeautifulSoup(r.text , "lxml")          
            if soup.find('script', {'type':'application/ld+json'}):
                data = soup.find('script', {'type':'application/ld+json'}).text        
                jsonData = json.loads(data)            
                if 'transcript' in jsonData:                
                    transcript = jsonData['transcript']
                    author = jsonData['author']['name']
                    datePublished = jsonData['uploadDate'].split('T')[0]
                    rawVideo = jsonData['url']
                    comments = jsonData['commentCount']
                    language = jsonData['inLanguage']                  
                    rows = [datePublished, author, comments, rawVideo, language, transcript]
                    writer.writerow(rows)
               
search()
print("\n","[*] Extracting {} videos...".format(str(len(set(videos)))),"\n")   
getData()   
print("\n","[*] Completed!")


