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
    over05_home = 0
    over15_home = 0
    over25_home = 0
    res = db.getHomeGames(team, round-1)
    for game in res:
        total_games += 1
        if game[7] > game[8]:
            total_wins += 1
            total_points += 3

        elif game[7] == game[8]:
            total_draws += 1
            total_points += 1
        else: total_lose += 1

        total_goals = (game[7] + game[8]) / 2

        if total_goals > 0:
            over05_home += 1
            if total_goals > 1.5:
                over15_home += 1
                if total_goals > 2.5:
                    over25_home += 1
                else:
                    pass
            else:
                pass
        else:
            pass

    scored += game[7]
    against += game[8]
    return [game[0], total_games, total_wins, total_draws, total_lose, scored, against, total_points, over05_home, over15_home, over25_home]

def getAwayGames(team, round):
    scored = 0
    against = 0
    total_games = 0
    total_wins = 0
    total_draws = 0
    total_lose = 0
    total_points = 0
    over05_away = 0
    over15_away = 0
    over25_away = 0
    res = db.getHomeGames(team, round - 1)
    for game in res:
        #print(game)
        total_games += 1
        if game[8] > game[7]:
            total_wins += 1
            total_points += 3
        elif game[7] == game[8]:
            total_draws += 1
            total_points += 1
        else:
            total_lose += 1

        total_goals = (game[7] + game[8]) / 2

        if total_goals > 0:
            over05_away += 1
            if total_goals > 1.5:
                over15_away += 1
                if total_goals > 2.5:
                    over25_away += 1
                else:
                    pass
            else:
                pass
        else:
            pass

        scored += game[7]
        against += game[8]
    return [game[0], total_games, total_wins, total_draws, total_lose, scored, against, total_points, over05_away, over15_away, over25_away ]


def inicialLoad():
    leagues = db.getLeagues()

    #for league in leagues:
    #    print("#############################")
    #    print(league)
    return leagues


def menu():
    cont = 0
    tip_over05 = ""
    tip_over15 = ""
    tip_over25 = ""

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
        if int(game_tupple[4]) <= 5:
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
            #[home_total_games, home_total_wins, home_total_draws, home_total_lose, home_scored, home_against, home_total_points] = getHomeGames(game_tupple[5], int(game_tupple[4]))
            #[away_total_games, away_total_wins, away_total_draws, away_total_lose, away_scored, away_against, away_total_points] = getAwayGames(game_tupple[6], int(game_tupple[4]))
            #print("UPDATE TOTAL GOALS")
            db.updateTotalGoals(game_tupple[5], game_tupple[6], int(game_tupple[4]), int(game_tupple[7]) + int(game_tupple[8]))
            #print("game_tupple[5]:" + game_tupple[5] + " home_total_games: " + str(home_total_games) )

            #pass
        else:
            pass
            #home team games - team 1 home games
            [game_id_t1, home_games_t1, home_wins_t1, home_draws_t1, home_loose_t1, home_scored_t1, home_against_t1,
             home_points_t1, t1_over05_home, t1_over15_home, t1_over25_home] = getHomeGames(game_tupple[5], int(game_tupple[4]))
            # home team games - team 1 away games
            [game_id_t1, away_games_t1, away_wins_t1, away_draws_t1, away_loose_t1, away_scored_t1, away_against_t1,
             away_points_t1, t1_over05_away, t1_over15_away, t1_over25_away] = getAwayGames(game_tupple[5], int(game_tupple[4]))

            #away team games - team 2 away games
            [game_id_t1, away_games_t2, away_wins_t2, away_draws_t2, away_loose_t2, away_scored_t2, away_against_t2,
             away_points_t2, t2_over05_away, t2_over15_away, t2_over25_away] = getAwayGames(game_tupple[6], int(game_tupple[4]))

            # away team games - team 2 home games
            [game_id_t2, home_games_t2, home_wins_t2, home_draws_t2, home_loose_t2, home_scored_t2, home_against_t2,
             home_points_t2, t2_over05_home, t2_over15_home, t2_over25_home] = getHomeGames(game_tupple[6], int(game_tupple[4]))

            #home teams - team 1 - OVERALL - total games, goals, victories, etc

            t1_played = home_games_t1 + away_games_t1
            t1_win = home_wins_t1 + away_wins_t1
            t1_draw = home_draws_t1 + away_draws_t1
            t1_loose = home_loose_t1 + away_loose_t1
            t1_goals_scores = home_scored_t1 + away_scored_t1
            t1_goals_against = home_against_t1 + away_against_t1
            t1_diff_goals = t1_goals_scores - t1_goals_against
            t1_total_under25 = t1_played - (t1_over25_home + t1_over25_away)
            t1_total_over25 = t1_over25_home + t1_over25_away

            t2_played = home_games_t2 + away_games_t2
            t2_win = home_wins_t2 + away_wins_t2
            t2_draw = home_draws_t2 + away_draws_t2
            t2_loose = home_loose_t2 + away_loose_t2
            t2_goals_scores = home_scored_t2 + away_scored_t2
            t2_goals_against = home_against_t2 + away_against_t2
            t2_diff_goals = t2_goals_scores - t2_goals_against
            t2_total_under25 = t2_played - (t2_over25_home + t2_over25_away)
            t2_total_over25 = t2_over25_home + t2_over25_away

            # Takuki calculations

            t1_temp1 = ((home_scored_t1 / home_games_t1) + (away_against_t2 / away_games_t2)) / 2
            t2_temp1 = ((home_against_t2 / away_games_t2) + (away_scored_t1 / home_games_t1)) / 2

            t1_temp2 = ((t1_goals_scores / t1_played) + (t2_goals_against / t2_played)) / 2
            t2_temp2 = ((t2_goals_scores / t2_played) + (t1_goals_against / t2_played)) / 2

            t1_res = (t1_temp1 * 0.7) + (t1_temp2 * 0.3)
            t2_res = (t2_temp1 * 0.7) + (t2_temp2 * 0.3)

            t1_over = ((home_games_t1 - t1_over25_home) / home_games_t1) + ((away_games_t2 - t2_over25_away) / away_games_t2)
            t2_over = (t1_over25_home / home_games_t1) + (t2_over25_away / away_games_t2)

            t1_over_total = (t1_total_under25 / t1_played) + (t2_total_under25 / t2_played)
            t2_over_total = (t1_total_over25 / t1_played) + (t2_total_over25 / t2_played)

            t1_under = ((t1_over * 0.7) + (t1_over_total * 0.3)) / 2
            t2_under = ((t2_over * 0.7) + (t2_over_total * 0.3)) / 2

            t1_t2_res = t1_res + t2_res
            t1_t2_under = t1_under - t2_under

            t1_total = t1_t2_res * t1_t2_under
            alpha_coeficient = 1 - t1_total


            # calculations for overs - Over0.5

            print("alpha_coeficient: " + str(alpha_coeficient))

            if alpha_coeficient < 0:
                tip_over05 = "UNDER"
            else:
                if 0 < alpha_coeficient < 1:
                    tip_over05 = "NO BET"
                if alpha_coeficient > 1:
                    tip_over05 = "OVER"

            # calculations for overs - Over1.5

            if alpha_coeficient < 1:
                tip_over15 = "UNDER"
            else:
                if 1 < alpha_coeficient < 2:
                    tip_over15 = "NO BET"
                if alpha_coeficient > 2:
                    tip_over15 = "OVER"

            # calculations for overs - Over2.5

            if alpha_coeficient < 2:
                tip_over25 = "UNDER"
            else:
                if 2 < alpha_coeficient < 3:
                    tip_over25 = "NO BET"
                if alpha_coeficient > 3:
                    tip_over25 = "OVER"



            # calculations for overs - Over3.5

            if alpha_coeficient < 3:
                tip_over35 = "UNDER"
            else:
                if 3 < alpha_coeficient < 4:
                    tip_over35 = "NO BET"
                if alpha_coeficient > 4:
                    tip_over35 = "OVER"





            db.updateTakuki(game_tupple[0], tip_over05, tip_over15, tip_over25, tip_over35)
            #db.updateTakuki(game_id_t2, tip_over05, tip_over15, tip_over25, tip_over35)

            db.updateTotalGoals(game_tupple[5], game_tupple[6], int(game_tupple[4]),
                                int(game_tupple[7]) + int(game_tupple[8]))

            #int_league = int(input('Press enter to continue '))


def main():
    menu()


if __name__ == '__main__':
    main()
