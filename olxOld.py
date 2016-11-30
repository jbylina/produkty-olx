from bs4 import BeautifulSoup
import requests

f = open('olxWyniki.txt', 'w')

for i in range(1, 2):
    r = requests.get("http://www.olx.pl/uslugi-firmy/piaseczno/?page=" + str(i))
    data = r.text
    soup = BeautifulSoup(data)
    for link in soup.findAll('a', {'class': 'marginright5'}):
        f.write(link['href'])
        # get inside link from main page
        r2 = requests.get(link['href'])
        data2 = r2.text
        soup2 = BeautifulSoup(data2)

        # find bottom bar div
        bottomBar = soup2.find('div', {'id': 'offerbottombar'})
        # print(bottomBar)
        # extract children div
        bottomBarChildren = bottomBar.findAll('div', {'class': 'pdingtop10'})
        # for div in bottomBarChildren:
        #	print(div)
        f.write(bottomBarChildren[1].text)

f.close()

