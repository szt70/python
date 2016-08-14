import sys
import json
import requests
from bs4 import BeautifulSoup

def scraping(url, output_name):

    # get a HTML response
    response = requests.get(url)
    html = response.text.encode(response.encoding)  # prevent encoding errors
    # parse the response
    soup = BeautifulSoup(html, "lxml")
    # extract
    ## title
    header = soup.find("head")
    title = header.find("title").text
    print("title: " + title)
    # description
    description = header.find("meta", attrs={"name": "description"})
    description_content = description.attrs['content']
    print("desc: " + str(description_content))
    # output
    output = {"title": title, "description": description_content}
    # write the output as a json file
    with open(output_name, "w") as fout:
        json.dump(output, fout, ensure_ascii=False, indent=4, sort_keys=True)

if __name__ == '__main__':
    print(sys.argv)
    # arguments
    argvs = sys.argv
    ## check
    if len(argvs) != 3:
        print ("Usage: python scraping.py [url] [output]")
        exit()
    url = argvs[1]
    output_name = argvs[2]

    scraping(url, output_name)