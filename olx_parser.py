# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from time import gmtime, strftime
import requests
import csv
import sys
from bokeh.plotting import figure, output_file, show


main_page_url = "https://www.olx.pl/uslugi-firmy/piaseczno/?page="
data_file = 'olx_data.csv'
results = []
obs_count = 5;
top_number = 3;


def read_csv():
    global results
    with open(sys.argv[1] + data_file, 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in csvreader:
            if row:
                row[0] = int(row[0])
                for i in range(0, obs_count):
                    row[3 + i * 3] = int(row[3 + i * 3])
                    row[4 + i * 3] = int(row[4 + i * 3])
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
            row[2 + i*3] = row[5 + i*3]
            row[3 + i*3] = row[6 + i*3]
            row[4 + i * 3] = row[7 + i * 3]
        row[-2] = -1
        row[-3] = -1
        row[-4] = -1


def update_results(id, url, time, views):
    for row in results:
        if row[0] == id:
            if row[-6] is not -1:
                d_views = views - row[-6]
            else:
                d_views = -1
            row[-4] = time
            row[-3] = views
            row[-2] = d_views
            return
    # if there is no entry in the list already
    new_row = [id, url]
    #print(type(new_row[0]))
    for i in range(0, obs_count - 1):
        new_row.append(-1)
        new_row.append(-1)
        new_row.append(-1)
    new_row.append(time)
    new_row.append(views)
    new_row.append(-1)
    # add sum of delta views
    new_row.append(-1)
    results.append(new_row)


def count_sum():
    for row in results:
        sum = 0
        for i in range(0, obs_count):
            if row[4 + i*3] is not -1:
                sum += row[4 + i*3]
        row[-1] = sum


def make_html():
    # sort list
    #results.sort(key=results[6])
    #print(results)
    #print(sorted(results, key=lambda sum: results[-1]))



    # prepare some data
    x = [1, 2, 3, 4, 5]
    y = [6, 7, 2, 4, 5]
    y2 = [5, 5, 3, 2, 4]

    # output to static HTML file
    output_file("index.html")

    # create a new plot with a title and axis labels
    p = figure(title="simple line example", x_axis_label='x', y_axis_label='y')

    # add a line renderer with legend and line thickness
    for i in range(0, top_number):
        p.line(x, y, legend="Temp.", line_width=2)
        p.line(x, y2, legend="Temp2", line_width=2)

    # show the results
    show(p)


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
shift_results()
check_views()
count_sum()
save_to_csv()
make_html()

