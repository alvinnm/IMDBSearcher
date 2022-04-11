import imdb
import urllib3
import sys
from bs4 import BeautifulSoup
import datetime
from tqdm import tqdm
import requests

def menu():
    ia = imdb.IMDb()
    option = input("\nPlease choose an option: \nS: Search for a movie \nT: Top movies of all time \nW: Worst movies of all time \nY: Top 50 movies by year \nQ: Quit\n")

    if option == "S" or option == "s":
        search = input("\nInput search here: ")
        results = ia.search_movie(search)
        print("\nShowing results for \"", search, "\": ")
        print("---------------------------")
        for res in results:
            print(res)
        menu()

    elif option == "Q" or option == "q":
        print("\nThank you for using IMDBSearcher! Goodbye.")
        quit()

    elif option == "T" or option == "t":
        top = ia.get_top250_movies()
        topEnd = input("\nHow many movies do you want to list (up to 250)?: ")
        try:
            if int(topEnd) <= 250 and int(topEnd) > 0:
                print("\nHere are the top " + str(topEnd) + " movies of all time: ")
                for i in range(int(topEnd)):
                    print(top[i], sep = "\n")
                menu()
            else:
                print("\nInvalid amount.")
                menu()
        except:
            print("\nInvalid input.")
            menu()

    elif option == "W" or option == "w":
        bottom = ia.get_bottom100_movies()
        bottomEnd = input("\nHow many movies do you want to list (up to 100)?: ")
        try:
            if int(bottomEnd) <= 100 and int(bottomEnd) > 0:
                print("\nHere are the bottom " + str(bottomEnd) + " movies of all time: ")
                for i in range(int(bottomEnd)):
                    print(bottom[i], sep = "\n")
                menu()
            else:
                print("\nInvalid amount.")
                menu()
        except:
            print("\nInvalid input.")
            menu()

    elif option == "Y" or option == "y":
        year = input("\nWhich year do you want to see movies from?: ")
        curr = int(datetime.datetime.now().year)
        headers= {'User-agent': 'Mozilla/5.0'}
        url = "http://www.imdb.com/search/title?release_date=" + str(year) + "," + str(year) + "&title_type=feature"
        response = requests.get(url, headers = headers)
        soup = BeautifulSoup(response.text, "html.parser")
        movieList = soup.findAll('div', attrs = {'class': 'lister-item mode-advanced'})

        try:
            if int(year) <= curr and len(movieList) >= 1:
                i = 1
                print("\nHere are the top movies of " + str(year) + ":")
                for div_item in tqdm(movieList, disable = True):
                    div = div_item.find('div', attrs = {'class':'lister-item-content'})
                    header = div.findChildren('h3', attrs = {'class':'lister-item-header'})
                    print(str(i) + '. ' + str((header[0].findChildren('a'))[0].contents[0].encode('utf-8').decode('ascii', 'ignore')))
                    i += 1
                menu()
            else:
                print("\nNo movies in that year.")
                menu()
        except:
            print("\nInvalid input.")
            menu()

    else:
        print("\nInvalid input, please try again.")
        menu()
menu()