import requests
from bs4 import BeautifulSoup

links = ["https://www.sports.ru/tribuna/"]
visited_links = []

visited_count = 0
while visited_count <=100:
    link = links.pop()
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')
    sub_links = soup.find_all("a")
    for i in sub_links:
        if ("https://www.sports.ru/tribuna/" in i.get("href")):
            if i.get("href") not in visited_links:
                links.append(i.get("href"))
            # print("appened" + i.string)
    if not("comment" in link) and not (link in visited_links):
        with open(r'saved1/page' + str(visited_count), 'wb') as f:
            f.write(response.content)
        with open("index1.txt", "a") as myfile:
            myfile.write("page" + str(visited_count) + "-----" + str(link) +"\n")
        visited_count = visited_count + 1
    visited_links.append(link)
    links = list(set(links))