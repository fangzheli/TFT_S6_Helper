import json

from bs4 import BeautifulSoup
from selenium import webdriver
import time
from flask import Flask

app = Flask(__name__)


@app.route('/helper')
def helper():
    champions =
    return '<h1>Hello World!</h1>'


def get_champions():
    url = "https://tftactics.gg/db/champions"
    driver = webdriver.Chrome('./chromedriver')
    driver.get(url)
    time.sleep(5)
    html = driver.page_source
    f = open("champions.html", "a", encoding="utf-8")
    f.write(html)
    f.close()
    print(html)


def clean_champions_synergy():
    f = open("champions.html", "r", encoding="utf-8")
    html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    # get a list of champions
    champions_names = soup.find_all("a", class_=['characters-item c1', 'characters-item c2', 'characters-item c3',
                                                 'characters-item c4', 'characters-item c5'])
    champions = []
    for champion in champions_names:
        try:
            champions.append(champion.contents[1])
        except IndexError:
            pass
    divs = soup.find_all("div", class_='rt-tr-group')
    champions_synergy_origin = {}
    champions_synergy_class = {}
    champions_cost = {}
    for div in divs:
        try:
            line = div.contents[0]
            name = line.contents[0].contents[0].contents[1]
            origins = line.contents[1]
            origin_list = []
            for origin in origins:
                origin_list.append(origin.contents[0].contents[1].contents[0])
            champions_synergy_origin[name] = origin_list
            classes = line.contents[2]
            class_list = []
            for _class in classes:
                class_list.append(_class.contents[0].contents[1].contents[0])
            champions_synergy_class[name] = class_list
            cost = line.contents[3].contents[0].contents[1]
            champions_cost[name] = cost
        except IndexError:
            pass
    results = {"champions": champions, "champions_synergy_orgin": champions_synergy_origin,
               "champions_synergy_class": champions_synergy_class, "champions_cost": champions_cost}
    champions_json = json.dumps(results)
    f = open("champions.json", "w", encoding="utf-8")
    f.write(champions_json)
    f.close()
    # return champions, champions_synergy_origin, champions_synergy_class, champions_cost


def get_traits_rank():
    url = "https://tftactics.gg/meta-report"
    driver = webdriver.Chrome('./chromedriver')
    html = driver.page_source
    f = open("traits_rank.html", "a", encoding="utf-8")
    f.write(html)
    f.close()
    print(html)


def clean_traits_rank():
    f = open("traits_rank.html", "r", encoding="utf-8")
    html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    # get a list of champions
    traits = soup.find_all("div", class_=['rt-tr -odd', 'rt-tr -even'])
    traits_rank = {}
    for trait in traits:
        trait_data = []
        try:
            trait_name = trait.contents[0].contents[1]
            active_number = trait.contents[0].contents[0].contents[0].contents[1].contents[0].contents[0]
            average_place = trait.contents[1].contents[0]
            win_rate = trait.contents[2].contents[0]
            top4_rate = trait.contents[3].contents[0]
            popularity = trait.contents[4].contents[0]
            trait_data.append(average_place)
            trait_data.append(win_rate)
            trait_data.append(top4_rate)
            trait_data.append(popularity)
            traits_rank[trait_name+active_number] = trait_data
        except IndexError:
            pass
    traits_rank_json = json.dumps(traits_rank)
    f = open("traits_rank.json", "w", encoding="utf-8")
    f.write(traits_rank_json)
    f.close()
    # return traits_rank


def search(root, key):
    if root is None or root.val == key:
        return root
    if root.val < key:
        return search(root.right, key)
    return search(root.left, key)


class TraitRankNode:
    def __init__(self, key, average_place, win_rate, top4_rate, popularity):
        self.left = None
        self.right = None
        self.val = key
        self.average_place = average_place
        self.win_rate = win_rate
        self.top4_rate = top4_rate
        self.popularity = popularity


def insert(root, key, average_place, win_rate, top4_rate, popularity):
    if root is None:
        return TraitRankNode(key, average_place, win_rate, top4_rate, popularity)
    else:
        if root.val == key:
            return root
        elif root.val < key:
            root.right = insert(root.right, key, average_place, win_rate, top4_rate, popularity)
        else:
            root.left = insert(root.left, key, average_place, win_rate, top4_rate, popularity)
    return root


def inorder(root):
    if root:
        inorder(root.left)
        print(root.val)
        inorder(root.right)


if __name__ == '__main__':
    # data collection
    # get_traits_rank()
    # get_champions()
    # clean_champions_synergy()
    # clean_traits_rank()
    # load data from json
    f = open("traits_rank.json", "r", encoding="utf-8")
    traits_rank_json = f.read()
    traits_rank = json.loads(traits_rank_json)
    f.close()
    f = open("champions.json", "r", encoding="utf-8")
    champions_json = f.read()
    champions_dict = json.loads(champions_json)
    f.close()
    champions = champions_dict["champions"]
    champions_synergy_origin = champions_dict["champions_synergy_orgin"]
    champions_synergy_class = champions_dict["champions_synergy_class"]
    champions_cost = champions_dict["champions_cost"]
    # make the assumption mentioned in the proposal
    champions.remove('Veigar')
    del champions_synergy_origin['Veigar']
    del champions_synergy_class['Veigar']
    del champions_cost['Veigar']
    del traits_rank['YordleLord1']
    del traits_rank['Cuddly1']
    del traits_rank['Glutton1']
    del traits_rank['Transformer1']
    # start to build tree based on current trait
    root = TraitRankNode('Assassin8', traits_rank['Assassin8'][0], traits_rank['Assassin8'][1], traits_rank['Assassin8'][2], traits_rank['Assassin8'][3])
    del traits_rank['Assassin8']
    for key, value in traits_rank.items():
        root = insert(root, key, value[0], value[1], value[2], value[3])
    # inorder(root)
    print("Hi, TFT")
    # run flask
    print('starting Flask app', app.name)
    app.run(debug=True)


