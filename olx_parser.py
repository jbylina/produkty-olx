# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from time import gmtime, strftime
import requests
import csv
import sys
#import pandas as pd


main_page_url = "https://www.olx.pl/uslugi-firmy/piaseczno/?page="
data_file = 'olx_data.csv'
results = []
obs_count = 5;


def read_csv():
    global results
    with open(sys.argv[1] + data_file, 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in csvreader:
            if row:
                row[0] = int(row[0])
                for i in range(0, obs_count):
                    row[3 + i * 2] = int(row[3 + i * 2])
                results.append(row)


def save_to_csv():
    global results
    with open(sys.argv[1] + data_file, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=' ', quotechar='|')
        for row in results:
            csvwriter.writerow(row)


def shift_results():
    for row in results:
        for i in range(0, obs_count - 1):
            row[2 + i*2] = row[4 + i*2]
            row[3 + i*2] = row[5 + i*2]


def update_results(id, url, time, views):
    for row in results:
        if row[0] == id:
            row[2*obs_count] = time;
            row[2*obs_count + 1] = views;
            return
    # if there is no entry in the list already
    new_row = [id, url];
    #print(type(new_row[0]))
    for i in range(0, obs_count - 1):
        new_row.append(-1)
        new_row.append(-1)
    new_row.append(time)
    new_row.append(views)
    results.append(new_row)


# sprawdzanie liczby stron - zrobił Dominik
def page_count(address):
    import requests
    r = requests.get(address)
    dest = r.history[0].headers['Location']
    return dest.split('?page=')[1]


# task that will run each hour (or another const time)
def check_views():
    url_shortened_list = []
    for i in range(1, 2):
        print("Parsing page no: " + str(i))
        sys.stdout.flush()
        request = requests.get(main_page_url + str(i))
        soup = BeautifulSoup(request.text, "html.parser")

        for link in soup.findAll('a', {'class': 'marginright5'}):
            url = link['href']
            print("Subpage url: " + url)
            sys.stdout.flush()

            # check only not promoted links and not already visited
            url_shortened = url.split('#')[0]
            if ";promoted" not in url and url_shortened not in url_shortened_list:
                # add url to list
                url_shortened_list.append(url_shortened)
                print("In subpage url: " + url)
                print("In subpage shortened url: " + url_shortened)
                sys.stdout.flush()
                # get inside link from main page
                request = requests.get(url)

                soup2 = BeautifulSoup(request.text, "html.parser")

                # find bottom bar div
                bottomBar = soup2.find('div', {'id': 'offerbottombar'})
                if bottomBar is None:
                    print("ERROR: No bottomBar")
                    continue
                # extract children div
                bottomBarChildren = bottomBar.findAll('div', {'class': 'pdingtop10'})
                if not bottomBarChildren:
                    print("ERROR: No bottomBarChildren")
                    continue
                offer_count = bottomBarChildren[1].text.strip().split('Wyświetleń:', 1)[1]

                # text_with_id example value: 'ID ogłoszenia: 1234423432'
                text_with_offer_id = soup2.find('div', {'class': 'offer-titlebox__details'}).find('small').text
                offer_id = text_with_offer_id.strip().split(" ")[-1]

                update_results(int(offer_id), url,strftime("%Y-%m-%d %H:%M:%S", gmtime()), int(offer_count))

read_csv()
if results:
    print(results[1])
shift_results()
check_views()
save_to_csv()

#for row in results:
#    print(type(row[0]))