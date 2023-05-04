import os
from flask import Flask, flash, redirect, render_template, request
import requests
import time
import json


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

global Gplayers
global Grankings
global Gstats
Gplayers = []
Grankings = []
Gstats = []


def lookup_players():
    url = "https://nba-stats4.p.rapidapi.com/players/"

    querystring = {"page":"1","is_active":"1","per_page":"500"}

    headers = {
    "X-RapidAPI-Key": "6397fdd1e6msha3629ffd03729aap1f67bfjsne56dfea96666",
    "X-RapidAPI-Host": "nba-stats4.p.rapidapi.com"
    }

    response1 = requests.request("GET", url, headers=headers, params=querystring)

    response1 = json.loads(response1.text)

    time.sleep(1.5)

    # second page of lits of players
    url = "https://nba-stats4.p.rapidapi.com/players/"

    querystring = {"page":"2","is_active":"1","per_page":"500"}

    headers = {
    "X-RapidAPI-Key": "6397fdd1e6msha3629ffd03729aap1f67bfjsne56dfea96666",
    "X-RapidAPI-Host": "nba-stats4.p.rapidapi.com"
    }

    response2 = requests.request("GET", url, headers=headers, params=querystring)

    response2 = json.loads(response2.text)

    # merge the two lists to make one master list

    players = response1 + response2
    time.sleep(1.5)
    return players



def lookup_stats():
    import requests

    url = "https://nba-stats4.p.rapidapi.com/season_totals_regular_season/"

    querystring = {"per_page":"500","page":"1","season_id":"2018-19"}

    headers = {
        "X-RapidAPI-Key": "6397fdd1e6msha3629ffd03729aap1f67bfjsne56dfea96666",
        "X-RapidAPI-Host": "nba-stats4.p.rapidapi.com"
    }

    response1 = requests.request("GET", url, headers=headers, params=querystring)

    response1 = json.loads(response1.text)

    time.sleep(1.5)

    url = "https://nba-stats4.p.rapidapi.com/season_totals_regular_season/"

    querystring = {"per_page":"500","page":"2","season_id":"2018-19"}

    headers = {
        "X-RapidAPI-Key": "6397fdd1e6msha3629ffd03729aap1f67bfjsne56dfea96666",
        "X-RapidAPI-Host": "nba-stats4.p.rapidapi.com"
    }

    response2 = requests.request("GET", url, headers=headers, params=querystring)

    response2 = json.loads(response2.text)

    stats = response1 + response2
    time.sleep(1.5)
    return stats

def lookup_rankings():
    import requests

    url = "https://nba-stats4.p.rapidapi.com/rankings_regular_season/"

    querystring = {"page":"1","season_id":"2018-19","per_page":"500"}

    headers = {
    "X-RapidAPI-Key": "6397fdd1e6msha3629ffd03729aap1f67bfjsne56dfea96666",
    "X-RapidAPI-Host": "nba-stats4.p.rapidapi.com"
    }

    response1 = requests.request("GET", url, headers=headers, params=querystring)

    response1 = json.loads(response1.text)

    time.sleep(1.5)

    url = "https://nba-stats4.p.rapidapi.com/rankings_regular_season/"

    querystring = {"page":"2","season_id":"2018-19","per_page":"500"}

    headers = {
    "X-RapidAPI-Key": "6397fdd1e6msha3629ffd03729aap1f67bfjsne56dfea96666",
    "X-RapidAPI-Host": "nba-stats4.p.rapidapi.com"
    }

    response2 = requests.request("GET", url, headers=headers, params=querystring)

    response2 = json.loads(response2.text)


    # Parse response, need to extend list as response.text does not
    rankings = response1 + response2
    time.sleep(1.5)
    return rankings



@app.route("/")
def index():
    if request.method == "GET":
        return render_template("index.html")

@app.route("/loading")
def loading():
    return render_template("loading.html")

@app.route("/loading2")
def loading2():
    return render_template("loading2.html")

@app.route("/new")
def new():
    global Gplayers
    global Gstats
    if not Gplayers:
        Gplayers = lookup_players()
        Gstats = lookup_stats()

    players = Gplayers
    stats = Gstats
    out = []
    id_to_name = {}

    for player_dict in players:
        id_to_name[player_dict['id']] = player_dict['full_name']

    for i in range(len(stats)):
        if stats[i]['player_id'] in id_to_name:
            out.append({'name': id_to_name[stats[i]["player_id"]], 'team': stats[i]['team_abbreviation'], 'gp': stats[i]["gp"], 'fg_pct': stats[i]['fg_pct'], 'fg3_pct': stats[i]['fg3_pct'], 'ft_pct': stats[i]['ft_pct'], 'reb': stats[i]['reb'], 'pts': stats[i]['pts'], 'ast': stats[i]['ast'], 'stl': stats[i]['stl'], 'blk': stats[i]['blk'], 'tov': stats[i]['tov']})

    return render_template("new.html", out=out)



@app.route("/regular_season")
def regular_season():
    global Gplayers
    global Grankings
    global Gstats
    if not Grankings:
        Grankings = lookup_rankings()
    if not Gplayers:
        Gplayers = lookup_players()
    if not Gstats:
        Gstats = lookup_stats()

    rankings = Grankings
    stats = Gstats
    players = Gplayers

    # GETTING TOP 10 POINTS STATS
    top10_points_names = []
    top10_points = []
    top10_stats_pts = []


    #for loop for finding the id of the top 10 players in a certain stat
    for rank in range(1, 11):
        for stats_dict in rankings:
            if int(stats_dict["rank_pts"]) == rank:
                top10_points.append(stats_dict["player_id"])
    #finding how many points that player scored
    for id in range(len(top10_points)):
        for dict in stats:
            if dict["player_id"] == top10_points[id]:
                top10_stats_pts.append(dict["pts"])
    #finding the name of the player using player id
    for id in range(len(top10_points)):
        for dict in players:
            if dict["id"] == top10_points[id]:
                top10_points_names.append(dict["full_name"])

    out=[]

    for i in range(len(top10_points_names)):
        rank = i + 1
        name = top10_points_names[i]
        pts = top10_stats_pts[i]
        out.append({'rank': rank, 'name': name, 'pts': pts})


    #for loop for finding the id of the top 10 players in a certain stat (ast)
    top10_ast_names = []
    top10_ast = []
    top10_stats_ast = []

    for rank in range(1, 11):
        for stats_dict in rankings:
            if int(stats_dict["rank_ast"]) == rank:
                top10_ast.append(stats_dict["player_id"])
    #finding how many points that player scored
    for id in range(len(top10_ast)):
        for dict in stats:
            if dict["player_id"] == top10_ast[id]:
                top10_stats_ast.append(dict["ast"])
    #finding the name of the player using player id
    for id in range(len(top10_ast)):
        for dict in players:
            if dict["id"] == top10_ast[id]:
                top10_ast_names.append(dict["full_name"])

    out_ast=[]

    for i in range(len(top10_ast)):
        rank = i + 1
        name = top10_ast_names[i]
        ast = top10_stats_ast[i]
        out_ast.append({'rank': rank, 'name': name, 'ast': ast})

    return render_template("regular_season.html", out=out, out_ast=out_ast)


def get_player_id_to_name():
    global Gplayers
    players = Gplayers
    id_to_name = {}

    for player_dict in players:
        id_to_name[player_dict['id']] = player_dict['full_name']



