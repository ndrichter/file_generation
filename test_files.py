import random
import string
import requests
import getpass
import wikipedia
from bs4 import BeautifulSoup

"""
Generates test files that can be uploaded to Onna. There are two options when generating files:
1. Generate a txt file from Wikipedia. Requires a topic from user input. Will catch a disambiguation error if there
   are too many results.
2. Generate a txt file with random text. Requires file size from user input. Good if you need to test large sized
   files
"""

current_user = getpass.getuser()
number_of_files = int(input("How many files do you want to create? "))
file_method = int(input("Generate from Wikipedia (1) or random (2) "))


def get_html_text(url):
    # use beautiful soup to extract text from the wiki's html
    html = requests.request('GET', url)
    soup = BeautifulSoup(html.text, features="html.parser")

    for script in soup(["script", "style"]):
        script.extract()

    return soup.get_text()


def random_string(string_length=10):
    # generate a random string to populate the file
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))


def create_random_file(iterator):
    # creates a random file with a specific size
    filename = "/Users/{0}/Downloads/myTestFile{1}.txt".format(current_user, iterator)
    with open(filename, "w+") as f:
        f.write(random_string() * (mbs * 100000))
    print('Created file {}'.format(filename))
    f.close()


def create_wiki_file():
    # creates a file from a wiki page's text
    wiki_search = input("What wiki page do you want to use? ")
    filename = "/Users/{0}/Downloads/{1}.txt".format(current_user, wiki_search.replace(" ", "_"))
    try:
        page = wikipedia.page(wiki_search)
    except wikipedia.DisambiguationError as e:
        print("Term creates too many results - {}".format(str(e)))
    else:
        wiki_url = page.url
        with open(filename, "w+") as f:
            f.write(get_html_text(wiki_url.strip()))
        print("Created {}".format(filename))
        f.close()


if file_method == 2:
    mbs = int(input("How many megabytes is each file? "))
for number in range(number_of_files):
    if file_method == 2:
        create_random_file(number)
    elif file_method == 1:
        create_wiki_file()
    else:
        print("I have no idea what you want")
