# pylint: disable=missing-docstring, line-too-long, missing-timeout
import sys
from os import path
from bs4 import BeautifulSoup
import requests
import csv

def parse(html):
    ''' return a list of dict {name, difficulty, prep_time} '''
    soup=BeautifulSoup(html,"html.parser")
    dic_title=soup.find_all("div", class_="p-2 recipe-details")
    list=[]
    for recipie in dic_title:
        dictt= parse_recipe(recipie)
        list.append(dictt)

    return list

def parse_recipe(article):
    ''' return a dict {name, difficulty, prep_time} modeling a recipe'''
    title= article.find("p", class_="text-dark text-truncate w-100 font-weight-bold mb-0 recipe-name").string
    difficulty=article.find("span", class_="recipe-difficulty").string
    pre_time= article.find("span",class_="recipe-cooktime").string
    final_dic={"name": title, "difficulty": difficulty, "prep_time":pre_time}
    return final_dic

def write_csv(ingredient, recipes):
    ''' dump recipes to a CSV file `recipes/INGREDIENT.csv` '''
    with open(f"recipes/{ingredient}.csv","w") as csvfile:
        filed_name= recipes[0].keys()
        writer= csv.DictWriter(csvfile, fieldnames=filed_name)
        writer.writeheader()
        for reci in recipes:
            writer.writerow (reci)


def scrape_from_internet(ingredient, start=1):
    ''' Use `requests` to get the HTML page of search results for given ingredients. '''
    url_base= "https://recipes.lewagon.com/"
    url= f"{url_base}?search[query]={ingredient}&pages={start}"
    response = requests.get(url)
    if response:
        return response.text
    return None

def scrape_from_file(ingredient):
    file = f"pages/{ingredient}.html"

    if path.exists(file):
        return open(file, encoding='utf-8')

    print("Please, run the following command first:")
    print(f'curl -g "https://recipes.lewagon.com/?search[query]={ingredient}" > pages/{ingredient}.html')
    sys.exit(1)

def main():
    if len(sys.argv) > 1:
        ingredient = sys.argv[1]
        recipes = scrape_from_internet(ingredient)
        recipes_list= parse(recipes)
        write_csv(ingredient, recipes_list)
        print(f"Wrote recipes to recipes/{ingredient}.csv")
    else:
        print('Usage: python recipe.py INGREDIENT')
        sys.exit(0)

if __name__ == '__main__':
    main()
