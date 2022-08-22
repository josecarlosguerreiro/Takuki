import baseDados.baseDados as db
import Online.online as online
import Objects.Leagues as obj
import datetime
#from datetime import date

# dd/mm/YY
#dta_today = date.today().strftime("%d.%m.%Y")
dta_today = datetime.date.today().strftime("%Y-%m-%d")
gameList = []


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

    if homeAway == 'home':
        res = db.getHomeGames(team, round - 1)
        for game in res:
            total_games += 1
            if game[7] > game[8]:
                total_wins += 1
                total_points += 3

            elif game[7] == game[8]:
                total_draws += 1
                total_points += 1
            else:
                total_lose += 1
            total_goals = total_goals + game[14]

            if game[14] > 0:
                over05_home += 1
                if game[14] > 1.5:
                    over15_home += 1
                    if game[14] > 2.5:
                        over25_home += 1
                    else:
                        pass
                else:
                    pass
            else:
                pass
            scored += int(game[7])
            against += int(game[8])
        return [game[0], total_games, total_wins, total_draws, total_lose, scored, against, total_points, over05_home,
                over15_home, over25_home]
    else:
        res = db.getAwayGames(team, round - 1)
        for game in res:
            total_games += 1
            if game[8] > game[7]:
                total_wins += 1
                total_points += 3
            elif game[7] == game[8]:
                total_draws += 1
                total_points += 1
            else:
                total_lose += 1

            total_goals = game[8] + game[7]

            if game[14] > 0:
                over05_away += 1
                if game[14] >= 1.5:
                    over15_away += 1
                    if game[14] >= 2.5:
                        over25_away += 1
                    else:
                        pass
                else:
                    pass
            else:
                pass

            scored += int(game[8])
            against += int(game[7])
        return [game[0], total_games, total_wins, total_draws, total_lose, scored, against, total_points, over05_away,
                over15_away, over25_away]


def createGames(row_list, league):
    total_goals = ' '
    for item in row_list:
        for td in item:
            normal_season = str(td)
            if normal_season.__contains__('Época normal'):
                pass
            else:
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
                    total_goals = int(home_goals) + int(away_goals)
                round_row = rows[5]
                round = obj.getRound(round_row)
                #dy, dm, dd = [int(x) for x in date_game.split('-')]
                #dy1, dm1, dd1 = [int(x) for x in dta_today.split('-')]
                #dt_game = date(dy, dm, dd)
                #dt_today = date(dy1, dm1, dd1)
                if (dta_today > date_game) and resultado.__contains__('vs'):
                    realized = 'A'
                elif dta_today > date_game:
                    realized = 'Y'
                else:
                    realized = 'N'

                game = obj.obj_game(league, season, date_game, round, home_team, team_away, home_goals, away_goals,
                                    realized, total_goals)
                gameList.append(game)
                '''
                res = db.getGame(game)
                if res is None:  # game does not exists
                    db.addGame(game)
                elif res[9] == 'N' and realized == 'Y':  # update game with goals and realized set to Y
                    upd_game = obj.obj_game.obj_game(league, season, date_game, round, home_team, team_away, home_goals,
                                            away_goals, realized, total_goals)
                    db.updateGame(res[0], upd_game)
                else:
                    pass
                '''
    return 0


def carregaLigas():
    ligas = db.getLeagues()
    return ligas


def menu():
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

    int_league = int(input('Witch league do you want? '))
    print("You chosed " + str(int_league))

    if int_league <= cont:
        if int_league == 0:
            return 0
        else:
            country_league = leagues[int_league - 1]
            country = country_league[1]
            league = country_league[2]
            year = country_league[3]
            link = country_league[4]
            active = country_league[5]
            row_list = online.openURL(link)
            createGames(row_list, league)
    else:
        print("Invalid option. Please select a correct one")
        return -1

    country_league = leagues[int_league - 1]
    country = country_league[1]


    for game in gameList:
        res = db.getGame(game)
        if res is None:
            db.addGame(country, game)
        else:
            pass
    nextRound = db.nextRound(country)[0]
    for game in gameList:
        if game.getRealized() == 'A':
            pass
        else:
            if int(game.getRound()) <= 5:
                if dta_today > game.getData():
                    id_game = db.getGame(game)
                    db.updateGame(id_game[0], game)
                else: pass
            else:
                if dta_today > game.getData():
                    id_game = db.getGame(game)
                    db.updateGame(id_game[0], game)
                else:
                    #calcular proxima jornada
                    id_game = db.getGame(game)
                    if int(game.getRound()) == nextRound:

                        # home team games - team 1 home games
                        [game_id_t1, home_games_t1, home_wins_t1, home_draws_t1, home_loose_t1, home_scored_t1,
                         home_against_t1,
                         home_points_t1, t1_over05_home, t1_over15_home, t1_over25_home] = getHomeGames(game.getHomeTeam(),
                                                                                                        int(game.getRound()),
                                                                                                        'home')
                        # home team games - team 1 away games
                        [game_id_t1, away_games_t1, away_wins_t1, away_draws_t1, away_loose_t1, away_scored_t1,
                         away_against_t1,
                         away_points_t1, t1_over05_away, t1_over15_away, t1_over25_away] = getHomeGames(game.getHomeTeam(),
                                                                                                        int(game.getRound()),
                                                                                                        'away')
                        # away team games - team 2 home games
                        [game_id_t2, home_games_t2, home_wins_t2, home_draws_t2, home_loose_t2, home_scored_t2,
                         home_against_t2,
                         home_points_t2, t2_over05_home, t2_over15_home, t2_over25_home] = getHomeGames(game.getAwayTeam(),
                                                                                                        int(game.getRound()),
                                                                                                        'home')

                        # away team games - team 2 away games
                        [game_id_t1, away_games_t2, away_wins_t2, away_draws_t2, away_loose_t2, away_scored_t2,
                         away_against_t2,
                         away_points_t2, t2_over05_away, t2_over15_away, t2_over25_away] = getHomeGames(game.getAwayTeam(),
                                                                                                        int(game.getRound()),
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
                        #print("updateTakuki:" + str(id_game[0]) + " | " + str(tip_over15) + " | " + str(tip_over25) + " | " + str(tip_over35) + " | " + str(total))
                        db.updateTakuki(id_game[0], tip_over05, tip_over15, tip_over25, tip_over35, total)
                    else:
                        pass
    return

def main():
    menu()




if __name__ == '__main__':
    main()
