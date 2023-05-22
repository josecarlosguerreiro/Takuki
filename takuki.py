import baseDados.baseDados as db
import Online.online as online
import Objects.Leagues as obj
import datetime
import argparse
import sys
#from datetime import date

# dd/mm/YY
#dta_today = date.today().strftime("%d.%m.%Y")
dta_today = datetime.date.today().strftime("%Y-%m-%d")


def getHomeGames(team, round, homeAway):
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
    over05_away = 0
    over15_away = 0
    over25_away = 0
    total_goals = 0
    #print("Equipa: %s" % team)
    #print("round: %s" % round)
    #print("homeAway: %s" % homeAway)
    if homeAway == 'home':
        res = db.getHomeGames(team, round - 1)
        for game in res:
            if game[9] == 'A':
                pass
            else:
                total_games += 1
                if game[8] > game[9]:
                    total_wins += 1
                    total_points += 3

                elif game[8] == game[9]:
                    total_draws += 1
                    total_points += 1
                else:
                    total_lose += 1
                total_goals = total_goals + game[15]

                if game[15] > 0:
                    over05_home += 1
                    if game[15] > 1.5:
                        over15_home += 1
                        if game[15] > 2.5:
                            over25_home += 1
                        else:
                            pass
                    else:
                        pass
                else:
                    pass
                scored += int(game[8])
                against += int(game[9])
        return [game[0], total_games, total_wins, total_draws, total_lose, scored, against, total_points, over05_home,
                over15_home, over25_home]
    else:
        res = db.getAwayGames(team, round - 1)
        for game in res:
            if game[9] == 'A':
                pass
            else:
                total_games += 1
                if game[9] > game[8]:
                    total_wins += 1
                    total_points += 3
                elif game[8] == game[9]:
                    total_draws += 1
                    total_points += 1
                else:
                    total_lose += 1

                total_goals = game[9] + game[8]

                if game[15] > 0:
                    over05_away += 1
                    if game[15] >= 1.5:
                        over15_away += 1
                        if game[15] >= 2.5:
                            over25_away += 1
                        else:
                            pass
                    else:
                        pass
                else:
                    pass

                scored += int(game[9])
                against += int(game[8])
        return [game[0], total_games, total_wins, total_draws, total_lose, scored, against, total_points, over05_away,
                over15_away, over25_away]


def translateGames(row_list, country, league):
    """
    translate from html to real data to be manipulated
    """
    game_list_translated = []
    for item in row_list:
        for td in item:
            normal_season = str(td)
            if normal_season.__contains__('Época normal'):
                pass
            if normal_season.__contains__('Play-offs'):
                print("ROW: " + str(normal_season))
                break
            else:
                try:
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
                    season = obj.getEpoca(date_game,country)
                    homeTeam_row = rows[2]
                    home_team = obj.getTeam(homeTeam_row)
                    team_away_row = rows[4]
                    team_away = obj.getTeam(team_away_row)
                    res = rows[3]
                    result = obj.getResultado(res)

                    if result.__contains__('vs'):
                        home_goals = ' '
                        away_goals = ' '
                    else:
                        home_goals = obj.golosCasa(result)
                        away_goals = obj.golosFora(result)
                        total_goals = int(home_goals) + int(away_goals)
                    round_row = rows[5]
                    round = obj.getRound(round_row)

                    if (dta_today > date_game):
                        if result.__contains__('-'):
                            realized = 'Y'
                        else:
                            realized = 'A'
                    else:
                        realized = 'N'

                    game = obj.obj_game(league, season, date_game, round, home_team, team_away, home_goals, away_goals,
                                        realized, total_goals)
                    game_list_translated.append(game)
                except:
                    print("ERRO LINHA: " + str(rows) )

                    pass

    return game_list_translated

def insertGames(row_list, country, league):
    for item in row_list:
        for td in item:
            normal_season = str(td)
            if normal_season.__contains__('Época normal'):
                pass
            if normal_season.__contains__('Play-offs'):
                break
            else:
                try:
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
                    game_date = obj.getDate(date_row)
                    season = obj.getEpoca(game_date, country)
                    home_team_row = rows[2]
                    home_team = obj.getTeam(home_team_row)
                    away_team_row = rows[4]
                    away_team = obj.getTeam(away_team_row)

                    round_row = rows[5]
                    round = obj.getRound(round_row)
                    realized = 'N'

                    result = db.insertGame(country, league, season, game_date, round, home_team, away_team, realized)
                except:
                    print("ERRO LINHA: " + str(rows) )
                    pass
    return result


def carregaLigas():
    ligas = db.getLeagues()
    return ligas


def takuki_menu():
    cont = 0
    print("###########################################")
    print("##                                       ##")
    print("##               TAKUKI by JCG           ##")
    print("##                                       ##")
    print("###########################################\n\n")
    leagues = carregaLigas()
    for i, league in enumerate(leagues):
        i += 1
        print(str(i) + " - " + league[1] + " - " + league[2])
        cont = i
    print("0 - Exit")

    int_league = int(input('Opção: '))
    print("Escolheste: " + str(int_league))
    if int_league <= cont:
        if int_league == 0:
            return 0
        else:
            return leagues[int_league - 1]
    else:
        print("Opção inválida. Pf escolhe uma opção correta")
        return -1


def takuki():

    league_row = takuki_menu()

    country = league_row[1]
    league = league_row[2]
    season = league_row[3]
    url_link = league_row[4]
    row_list = online.openURL(url_link, 0)
    counter = checkIfGamesExists(country, league, season)
    if counter == 0:
        insertGames(row_list, country, league)
    else:
        pass
    
    print("A ATUALIZAR " + country + " - " + league )
    game_list_translated = translateGames(row_list, country, league)
    game_list = getGames(country, league, season)
    updateGames(game_list_translated, game_list)
    updateTakuki(game_list, country, league)
    game_list = resetList(game_list)
    row_list = resetList(row_list)


def resetList(list):
    list = []
    return list

def checkIfGamesExists(country, league, season):
    counter = db.checkIfGamesExists(country, league, season)
    return counter

def getGames(country, league, season):
    game_list = db.getGames(country, league, season)
    return game_list

def updateGames(game_list_translated, game_list):
    size_list = len(game_list_translated)
    i = 0
    while i < size_list:
        home_team_translated = game_list_translated[i].getHomeTeam()
        away_team_translated = game_list_translated[i].getAwayTeam()

        home_team_list = game_list[i][6]
        away_team_list = game_list[i][7]

        epoca = game_list[i][3]

        if home_team_translated == home_team_list and away_team_translated == away_team_list:
            if game_list_translated[i].getData() < dta_today:
                db.updateGame(epoca, game_list_translated[i])
            else:
                pass
        else:
            pass
        i += 1


def updateTakuki(game_list, country, league):

    nextRound = db.nextRound(country, league)[0]

    for game in game_list:
        #game[11] --> takuki05
        #game[4] --> game date
        #game[5] --> round
        if game[5] < 5:
            pass
        else:
            if (game[11] is None and game[4] < dta_today) or int(game[5]) == nextRound:
                [game_id_t1, home_games_t1, home_wins_t1, home_draws_t1, home_loose_t1, home_scored_t1,
                 home_against_t1,
                 home_points_t1, t1_over05_home, t1_over15_home, t1_over25_home] = getHomeGames(game[6],
                                                                                                int(game[5]),
                                                                                                'home')
                # home team games - team 1 away games
                [game_id_t1, away_games_t1, away_wins_t1, away_draws_t1, away_loose_t1, away_scored_t1,
                 away_against_t1,
                 away_points_t1, t1_over05_away, t1_over15_away, t1_over25_away] = getHomeGames(game[6],
                                                                                                int(game[5]),
                                                                                                'away')
                # away team games - team 2 home games
                [game_id_t2, home_games_t2, home_wins_t2, home_draws_t2, home_loose_t2, home_scored_t2,
                 home_against_t2,
                 home_points_t2, t2_over05_home, t2_over15_home, t2_over25_home] = getHomeGames(game[7],
                                                                                                int(game[5]),
                                                                                                'home')

                # away team games - team 2 away games
                [game_id_t1, away_games_t2, away_wins_t2, away_draws_t2, away_loose_t2, away_scored_t2,
                 away_against_t2,
                 away_points_t2, t2_over05_away, t2_over15_away, t2_over25_away] = getHomeGames(game[7],
                                                                                                int(game[5]),
                                                                                                'away')

                # home teams - team 1 - OVERALL - total games, goals, victories, etc

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
                t2_temp1 = ((away_scored_t2 / away_games_t2) + (away_against_t1 / home_games_t1)) / 2

                t1_temp2 = ((t1_goals_scores / t1_played) + (t2_goals_against / t2_played)) / 2
                t2_temp2 = ((t2_goals_scores / t2_played) + (t1_goals_against / t1_played)) / 2

                t1_res = (t1_temp1 * 0.7) + (t1_temp2 * 0.3)
                t2_res = (t2_temp1 * 0.7) + (t2_temp2 * 0.3)

                t1_over = ((home_games_t1 - t1_over25_home) / home_games_t1) + (
                        (away_games_t2 - t2_over25_away) / away_games_t2)
                t2_over = (t1_over25_home / home_games_t1) + (t2_over25_away / away_games_t2)

                t1_over_total = (t1_total_under25 / t1_played) + (t2_total_under25 / t2_played)
                t2_over_total = (t1_total_over25 / t1_played) + (t2_total_over25 / t2_played)

                t1_under = ((t1_over * 0.7) + (t1_over_total * 0.3)) / 2
                t2_under = ((t2_over * 0.7) + (t2_over_total * 0.3)) / 2

                t1_t2_res = t1_res + t2_res
                t1_t2_under = t1_under - t2_under

                # t1_total = t1_t2_res * t1_t2_under
                alpha_coeficient = 1 - t1_t2_under
                total = t1_t2_res * alpha_coeficient

                if total < 0:
                    tip_over05 = "UNDER"
                else:
                    if 0 < total < 1:
                        tip_over05 = "NO BET"
                    if total > 1:
                        tip_over05 = "OVER"

                # calculations for overs - Over1.5

                if total < 1:
                    tip_over15 = "UNDER"
                else:
                    if 1 < total < 2:
                        tip_over15 = "NO BET"
                    if total > 2:
                        tip_over15 = "OVER"

                # calculations for overs - Over2.5

                if total < 2:
                    tip_over25 = "UNDER"
                else:
                    if 2 < total < 3:
                        tip_over25 = "NO BET"
                    if total > 3:
                        tip_over25 = "OVER"

                # calculations for overs - Over3.5

                if total < 3:
                    tip_over35 = "UNDER"
                else:
                    if 3 < total < 4:
                        tip_over35 = "NO BET"
                    if total > 4:
                        tip_over35 = "OVER"
                # print("updateTakuki:" + str(id_game[0]) + " | " + str(tip_over15) + " | " + str(tip_over25) + " | " + str(tip_over35) + " | " + str(total))
                db.updateTakuki(game[0], game[4], tip_over05, tip_over15, tip_over25, tip_over35, total,
                                home_scored_t1 / home_games_t1, away_scored_t2 / away_games_t2)



def takuki_global():
    array_ligas = carregaLigas()
    cont = len(array_ligas)

    for i in range(cont):
        elem_array = array_ligas[i]
        country = elem_array[1]
        league = elem_array[2]
        season = elem_array[3]
        link = elem_array[4]

        row_list = online.openURL(link,0)
        counter = checkIfGamesExists(country, league, season)
        if counter == 0:
            insertGames(row_list, country, league)
        else:
            pass
        print("A ATUALIZAR " + country + " - " + league )
        game_list_translated = translateGames(row_list, country, league)
        game_list = getGames(country, league, season)
        updateGames(game_list_translated, game_list)
        updateTakuki(game_list, country, league)
        game_list = resetList(game_list)
        row_list = resetList(row_list)

def calcula_estatistica(country, league):
    cursor = db.calcula_estatistica(country, league)

    lista_tak_05 = []
    lista_tak_15 = []
    lista_tak_25 = []
    lista_tak_35 = []
    over_05 = 0.5
    over_15 = 1.5
    over_25 = 2.5
    over_35 = 3.5
    for i in cursor:
        total_golos = i[15]
        tak_05 = i[11]
        tak_15 = i[12]
        tak_25 = i[13]
        tak_35 = i[14]

        if total_golos >= over_05:
            if tak_05 == 'NO BET':
                pass
            else:
                temp_05 = 'OVER'
                if tak_05 == temp_05:
                    lista_tak_05.append('V')
                else:
                    lista_tak_05.append('F')
        else:
            if tak_05 == 'NO BET':
                pass
            else:
                temp_05 = 'UNDER'
                if tak_05 == temp_05:
                    lista_tak_05.append('V')
                else:
                    lista_tak_05.append('F')

        if total_golos >= over_15:
            if tak_15 == 'NO BET':
                pass
            else:
                temp_15 = 'OVER'
                if tak_15 == temp_15:
                    lista_tak_15.append('V')
                else:
                    lista_tak_15.append('F')
        else:
            if tak_15 == 'NO BET':
                pass
            else:
                temp_15 = 'UNDER'
                if tak_15 == temp_15:
                    lista_tak_15.append('V')
                else:
                    lista_tak_15.append('F')

        if total_golos >= over_25:
            if tak_25 == 'NO BET':
                pass
            else:
                temp_25 = 'OVER'
                if tak_25 == temp_25:
                    lista_tak_25.append('V')
                else:
                    lista_tak_25.append('F')
        else:
            if tak_25 == 'NO BET':
                pass
            else:
                temp_25 = 'UNDER'
                if tak_25 == temp_25:
                    lista_tak_25.append('V')
                else:
                    lista_tak_25.append('F')

        if total_golos >= over_35:
            if tak_35 == 'NO BET':
                pass
            else:
                temp_35 = 'OVER'
                if tak_35 == temp_35:
                    lista_tak_35.append('V')
                else:
                    lista_tak_35.append('F')
        else:
            if tak_35 == 'NO BET':
                pass
            else:
                temp_35 = 'UNDER'
                if tak_35 == temp_35:
                    lista_tak_35.append('V')
                else:
                    lista_tak_35.append('F')

    tam_lista_05 = len(lista_tak_05)
    total_05 = 0
    for i in lista_tak_05:
        if i == 'V':
            total_05 += 1
        else: pass

    print("PERCENTAGEM DE ACERTOS 05: " + str((total_05/tam_lista_05)*100))

    tam_lista_15 = len(lista_tak_15)
    total_15 = 0
    for i in lista_tak_15:
        if i == 'V':
            total_15 += 1
        else:
            pass
    print("PERCENTAGEM DE ACERTOS 15: " + str((total_15 / tam_lista_15) * 100))

    tam_lista_25 = len(lista_tak_25)
    total_25 = 0
    for i in lista_tak_25:
        if i == 'V':
            total_25 += 1
        else:
            pass
    print("PERCENTAGEM DE ACERTOS 25: " + str((total_25 / tam_lista_25) * 100))

    tam_lista_35 = len(lista_tak_35)
    total_35 = 0
    for i in lista_tak_35:
        if i == 'V':
            total_35 += 1
        else:
            pass
    print("PERCENTAGEM DE ACERTOS 35: " + str((total_35 / tam_lista_35) * 100))



def estatisticas():
    print("###########################################")
    print("##                                       ##")
    print("##               Estatiticas             ##")
    print("##                                       ##")
    print("###########################################")
    leagues = carregaLigas()
    for i, league in enumerate(leagues):
        i += 1
        print(str(i) + " - " + league[1] + " - " + league[2])
        cont = i
    print("\n")
    print("0 - Voltar menu anterior")
    op = int(input('Opção:'))
    pais_liga = leagues[op - 1]
    pais = pais_liga[1]
    liga = pais_liga[2]
    calcula_estatistica(pais, liga)



def menu():
    try:
        db.connect()
    except:
        exit(1)

    print("###########################################")
    print("##                                       ##")
    print("##               TAKUKI by JCG           ##")
    print("##                                       ##")
    print("###########################################\n\n")
    print("1 - Ver estatisticas por pais")
    print("2 - Atualizar takuki")
    print("9 - Atualizar takuki de forma global")
    print("0 - Sair")

    op = int(input('Opção:'))
    if op == 1:
        estatisticas()
    elif op == 2:
        takuki()
    elif op == 9:
        takuki_global()
    elif op == 0:
        return 0
    else:
        print("Opção inválida!")
        return -1



def main():
    menu()





if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-op', '--option',
                        default='9',
                        required=False,
                        help='Option 9 is update takuki_global',
                        type=int
                        )
    args = parser.parse_args()

    if len(sys.argv) == 1:
        menu()
    else:
        takuki_global()
        sys.exit(-1)
