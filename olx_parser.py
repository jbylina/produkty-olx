from bs4 import BeautifulSoup
from time import gmtime, strftime
import requests
import csv


def save_to_csv(array):
    with open('olxWyniki.csv', 'a') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
        for item in array:
            writer.writerow(item)


results = []

for i in range(500, 1):
    request = requests.get("http://www.olx.pl/uslugi-firmy/piaseczno/?page=" + str(i))
    soup = BeautifulSoup(request.text, "html.parser")

    for link in soup.findAll('a', {'class': 'marginright5'}):
        url = link['href']

        # get inside link from main page
        request = requests.get(url)
        soup2 = BeautifulSoup(request.text, "html.parser")

        # find bottom bar div
        bottomBar = soup2.find('div', {'id': 'offerbottombar'})

        # extract children div
        bottomBarChildren = bottomBar.findAll('div', {'class': 'pdingtop10'})
        offer_count = bottomBarChildren[1].text.strip().split('Wyświetleń:', 1)[1]

        id = soup2.find('span', {'class': 'rel inlblk'}).text

        results.append([int(id), url, strftime("%Y-%m-%d %H:%M:%S", gmtime()), int(offer_count)])

save_to_csv(results)
