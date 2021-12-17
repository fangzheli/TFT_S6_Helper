import json
import collections
import itertools
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from flask import Flask, render_template, request, redirect, url_for
import requests
import os


app = Flask(__name__, static_url_path='/static')


@app.route('/helper')
def helper():
    return render_template('input.html', champions_=champions_, champions=champions)


@app.route('/recommendation', methods=['POST'])
def give_recommendation():
    owned_champions_list = []
    level = int(request.form["levels"])
    # stage = request.form["Stage"]
    for champion in request.form.to_dict().keys():
        for _key, _value in champions_.items():
            if _value == champion:
                owned_champions_list.append(_key)
                break
    if not owned_champions_list:
        return "<h1> Oops! It seems that not enough champions are chosen!</h1>"
    comps = list(itertools.combinations(owned_champions_list, min(level, len(owned_champions_list))))
    win_rate_list = []
    for comp in comps:
        trait = check_trait(comp, champions_synergy_origin, champions_synergy_class)
        data_node = search(root, trait)
        if data_node:
            win_rate_list.append(float(data_node.win_rate.strip('%'))/100)
        else:
            win_rate_list.append(0)
    win_rate = max(win_rate_list)
    recommendation_comp = comps[win_rate_list.index(max(win_rate_list))]
    return render_template('recommendation.html', champions=owned_champions_list, win_rate=win_rate, recommendation_comp=recommendation_comp)


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
    dirname = os.path.dirname(__file__)
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
            response = requests.get(champion.contents[0].contents[0]['src'])
            file_name = dirname + "/static/imgs/" + champion.contents[1] + ".png"
            file = open(file_name, "wb")
            file.write(response.content)
            file.close()
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
    results = {"champions": champions, "champions_synergy_origin": champions_synergy_origin,
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
            traits_rank[trait_name + active_number] = trait_data
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


def check_trait(champions_list, champions_origin, champions_class):
    '''
    :param champions_class:
    :param champions_origin:
    :param champions_list:
    :return: a string that combine the strongest trait and the number of champions that activate this trait
    '''
    synergy = []
    for champion in champions_list:
        for trait in champions_class[champion]:
            synergy.append(trait)
        for trait in champions_origin[champion]:
            synergy.append(trait)
    cnt = collections.Counter(synergy)
    strong_trait = cnt.most_common(1)[0][0]
    strong_trait_number = cnt.most_common(1)[0][1]
    return strong_trait+str(strong_trait_number)


if __name__ == '__main__':
    # data collection, only use when you need to update the cache
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
    champions_synergy_origin = champions_dict["champions_synergy_origin"]
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
    root = TraitRankNode('Assassin8', traits_rank['Assassin8'][0], traits_rank['Assassin8'][1],
                         traits_rank['Assassin8'][2], traits_rank['Assassin8'][3])
    del traits_rank['Assassin8']
    for key, value in traits_rank.items():
        root = insert(root, key, value[0], value[1], value[2], value[3])
    # inorder(root)
    # create the champions name without space
    champions_ = {champion: champion.replace(" ", "_") for champion in champions}
    # run flask
    print("Hi, TFT helper")
    app.run(debug=True)
