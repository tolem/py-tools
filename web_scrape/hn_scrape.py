import requests
from bs4 import BeautifulSoup
import csv
# import pprint



def hn_link(l):
    mega_links = []
    mega_subtext = []
    for li in l:
        res = requests.get(li)
        soup = BeautifulSoup(res.text, 'html.parser')
        links = soup.select('.titlelink')
        subtext = soup.select('.subtext')
        mega_links += links 
        mega_subtext += subtext

    return mega_links, mega_subtext

    
mega_links, mega_subtext = hn_link(['https://news.ycombinator.com', 'https://news.ycombinator.com?p=2','https://news.ycombinator.com?p=3'])

# print(mega_links)

def sort_stories_by_votes(hnlist):
  return sorted(hnlist, key= lambda k:k['votes'], reverse=True)

def create_custom_hn(links, subtext):
  hn = []
  for idx, item in enumerate(links):
    title = item.getText()
    href = item.get('href', None)
    vote = subtext[idx].select('.score')
    if len(vote):
      points = int(vote[0].getText().replace(' points', ''))
      if points > 99:
        hn.append({'title': title, 'link': href, 'votes': points})
  return sort_stories_by_votes(hn)
 

# create_custom_hn(mega_links, mega_subtext)
# print(create_custom_hn(mega_links, mega_subtext))
news_list = create_custom_hn(mega_links, mega_subtext)
with open('hacker_news.csv', mode='a') as database:
    for dicts in news_list:
        title = dicts['title']
        link = dicts['link']
        votes = dicts['votes']
        csv_writer = csv.writer(database, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([title,link, votes])
