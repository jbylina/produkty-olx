from bs4 import BeautifulSoup
import requests
import csv


def save_to_csv(array):
    with open('olxWyniki.csv', 'w') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
        for item in array:
            writer.writerow(item)


results = []

for i in range(1, 2):
    request = requests.get("http://www.olx.pl/uslugi-firmy/piaseczno/?page=" + str(i))
    soup = BeautifulSoup(request.text, "lxml")

    for link in soup.findAll('a', {'class': 'marginright5'}):
        url = link['href']

        # get inside link from main page
        request = requests.get(url)
        soup2 = BeautifulSoup(request.text, "lxml")

        # find bottom bar div
        bottomBar = soup2.find('div', {'id': 'offerbottombar'})

        # extract children div
        bottomBarChildren = bottomBar.findAll('div', {'class': 'pdingtop10'})
        offer_count = bottomBarChildren[1].text.strip().split('Wyświetleń:', 1)[1]

        # for div in bottomBarChildren:
        results.append([url, int(offer_count)])

save_to_csv(results)
