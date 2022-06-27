#!/usr/bin/python
# import re
# import sqlite3
# import subprocess
# import os
# import mechanize
# import ssl
# import urllib.request
# import time
# from bs4 import BeautifulSoup
# import urllib2
# import urllib.request as urllib2
# import database as db
from datetime import date

import baseDados.baseDados as db
import Online.online as online
import Objects.Leagues as obj

today = date.today()

# dd/mm/YY
dta_today = today.strftime("%d.%m.%Y")

def gamesAndResults(row_list, league):
    for item in row_list:
        for td in item:
            rows = td.find_all('td')
            '''
            print('row 1 -->' + str(rows[1]))  ## Data do jogo
            print('row 2 -->' + str(rows[2]))  ##equipa da casa
            print('row 3 -->' + str(rows[3]))  ##golos equipa casa
            print('row 4 -->' + str(rows[4]))  ##equipa de fora
            print('row 5 -->' + str(rows[5]))  ##golos equipa fora
            print('row 6 -->' + str(rows[6]))  ##
            '''

            date_row = rows[1]
            date_game = obj.getDate(date_row)
            season = obj.getEpoca(date_game)
            homeTeam_row = rows[2]
            home_team = obj.getTeam(homeTeam_row)
            team_away_row = rows[4]
            team_away = obj.getTeam(team_away_row)
            res = rows[3]
            resultado = obj.getResultado(res)
            if resultado.__contains__('vs'):
                home_goals = ' '
                away_goals = ' '
            else:
                home_goals = obj.golosCasa(resultado)
                away_goals = obj.golosFora(resultado)
            round_row = rows[5]
            round = obj.getRound(round_row)
            dd, dm, dy = [int(x) for x in date_game.split('.')]
            dd1, dm1, dy1 = [int(x) for x in dta_today.split('.')]

            dt_game = date(dy, dm, dd)
            dt_today = date(dy1, dm1, dd1)
            if dt_today > dt_game:
                realized = 'Y'
            else:
                realized = 'N'
            game = obj.obj_game(league, season, date_game, round, home_team, team_away, home_goals, away_goals, realized)
            '''
            verify if game already exists on db. if so, don't add the game
            '''
            res = db.getGame(game)
            if res is None:
                db.addGame(game)
            else: pass

    return 0


def getHomeGames(team, round):
    scored = 0
    against = 0
    total_games = 0
    total_wins = 0
    total_draws = 0
    total_lose = 0
    total_points = 0
    res = db.getHomeGames(team, round-1)
    for game in res:
        print(game)
        total_games += 1
        if game[7] > game[8]:
            total_wins += 1
            total_points += 3
        elif game[7] == game[8]:
            total_draws += 1
            total_points += 1
        else: total_lose += 1

        scored += game[7]
        against += game[8]
    return [total_games, total_wins, total_draws, total_lose, scored, against, total_points]

def getAwayGames(team, round):
    scored = 0
    against = 0
    total_games = 0
    total_wins = 0
    total_draws = 0
    total_lose = 0
    total_points = 0
    res = db.getHomeGames(team, round - 1)
    for game in res:
        print(game)
        total_games += 1
        if game[8] > game[7]:
            total_wins += 1
            total_points += 3
        elif game[7] == game[8]:
            total_draws += 1
            total_points += 1
        else:
            total_lose += 1

        scored += game[7]
        against += game[8]
    return [total_games, total_wins, total_draws, total_lose, scored, against, total_points]


def inicialLoad():
    leagues = db.getLeagues()

    #for league in leagues:
    #    print("#############################")
    #    print(league)
    return leagues


def menu():
    cont = 0
    print("###########################################")
    print("##                                       ##")
    print("##               TAKUKI by JCG           ##")
    print("##                                       ##")
    print("###########################################\n\n")
    leagues = inicialLoad()
    for i, league in enumerate(leagues):
        i += 1
        print(str(i) + " - " + league[1] + " - " + league[2])
        cont = i
    print("0 - All leagues")
    '''
    int_league = int(input('Witch league do you want? '))
    print("You chosed " + str(int_league))
    print("Cont " + str(cont))
    '''
    '''
    just for development
    int_league = 1
    '''
    int_league = 1
    if int_league <= cont:
        if int_league == 0:
            print("Not developed yet")
        else:
            country_league = leagues[int_league-1]
            country = country_league[1]
            league = country_league[2]
            year = country_league[3]
            link = country_league[4]
            active = country_league[5]
            row_list = online.openURL(link)
            gamesAndResults(row_list, league)
    else:
        print("Opcao Invalida. Por favor escolhe uma opcao correta")
        return -1

    '''
    Get all games from db to memory
    '''
    allgames = db.getAllGames(league)

    for game_tupple in allgames:
        if int(game_tupple[4]) == 1:
            db.updateTotalGoals(game_tupple[5], game_tupple[6], int(game_tupple[4]),
                                int(game_tupple[7]) + int(game_tupple[8]))
            pass
        elif int(game_tupple[4]) <= 5:
            '''
            game_tupple[0] --> id
            game_tupple[1] --> league
            game_tupple[2] --> season
            game_tupple[3] --> game_date
            game_tupple[4] --> round
            game_tupple[5] --> home_team
            game_tupple[6] --> away_team
            game_tupple[7] --> home_goals
            game_tupple[8] --> away_goals
            game_tupple[9] --> realized            
            '''
            [home_total_games, home_total_wins, home_total_draws, home_total_lose, home_scored, home_against, home_total_points] = getHomeGames(game_tupple[5], int(game_tupple[4]))
            [away_total_games, away_total_wins, away_total_draws, away_total_lose, away_scored, away_against, away_total_points] = getAwayGames(game_tupple[6], int(game_tupple[4]))
            print("UPDATE TOTAL GOALS")
            db.updateTotalGoals(game_tupple[5], game_tupple[6], int(game_tupple[4]), int(game_tupple[7]) + int(game_tupple[8]))

            #pass
        else:
            pass
            #home_team = game.getHomeTeam()
            #away_team = game.getAwayTeam()
            #round = game.getRound()




def main():
    menu()


if __name__ == '__main__':
    main()
