import mysql.connector

'''
def connect():
    try:
        mydb = mysql.connector.connect(user='root', password='2111986kramermania',
                                       host='127.0.0.1',
                                       database='takuki')
        return mydb
    except:
        print("Erro ao aceder base dados.")
        return None

'''
#UPDATE games SET goals_home =

def connect():
    try:
        mydb = mysql.connector.connect(user='jguerreiro', password='2111986kramermania',
                                       host='192.168.1.72',
                                       database='takuki')
        return mydb
    except:
        print("Erro ao aceder base dados.")
        return None


def disconnect(connection):
    try:
        connection.close()
        return 0
    except:
        print("Cannot close db")
        return -1


def getLeagues():
    try:
        conn = connect()
        mycursor = conn.cursor()
        mycursor.execute("SELECT * FROM leagues WHERE ATIVO = 'S'")
        result = mycursor.fetchall()
        disconnect(conn)
        return result
    except:
        return None


def updateGame(season, data, realized, home_team_translated, home_goals, away_team_translated, away_goals):
    try:
        conn = connect()
        mycursor = conn.cursor()
        if realized == 'A':
            sql = "UPDATE games SET realized = 'A', game_date = '%s' WHERE home_team = '%s' and away_team = '%s' and season = '%s'" % (data, home_team_translated, away_team_translated, season)
            mycursor.execute(sql)
            conn.commit()
        if realized == 'Y':
            sql = "UPDATE games SET goals_home = '%s', goals_away = '%s', realized = '%s', total_goals = '%s' ,game_date = '%s' WHERE home_team = '%s' and away_team = '%s' and season = '%s'" % (home_goals, away_goals, realized, int(home_goals) + int(away_goals), data, home_team_translated, away_team_translated, season)
            mycursor.execute(sql)
            conn.commit()
        else:
            pass
        #print(sql)

    except Exception as error:
        print("Erro linha de base dados." + str(error))
        print("Por favor corrigir")
        exit(1)

    disconnect(conn)
    return


def getHomeGames(team, round):
    conn = connect()
    mycursor = conn.cursor()
    sql = "SELECT * FROM games where home_team = '" + team + "' and round <= '" + str(round) + "' and realized = 'Y'"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    disconnect(conn)
    return myresult


def getAwayGames(team, round):
    conn = connect()
    mycursor = conn.cursor()
    sql = "SELECT * FROM games where away_team = '" + team + "' and round <= '" + str(round) + "' and realized = 'Y'"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    disconnect(conn)
    return myresult




def updateTakuki(game_id, dta_jogo, over05, over15, over25, over35, total, golos_m_eq_casa, golos_m_eq_fora):
    conn = connect()
    mycursor = conn.cursor()

    print("ID: " + str(game_id))
    print("Dta_Jogo: " + dta_jogo)
    print("takuki05: " + over05)
    print("takuki15: " + over15)
    print("takuki25: " + over25)
    print("takuki35: " + over35)

    sql = "UPDATE games SET game_date = '%s' , takuki05 = '%s' , takuki15 = '%s' , takuki25 = '%s', takuki35 = '%s', takuki_total = '%s', prev_goals_home_team = '%s', prev_goals_away_team = '%s' where id = '%s'" % (dta_jogo, over05, over15, over25, over35, total, golos_m_eq_casa, golos_m_eq_fora, game_id)

    #sql = "update games set game_date = '" + str(dta_jogo) + "', takuki05 = '" + str(over05) + "', takuki15 = '" + str(over15) + "', takuki25 = '" + str(
    #    over25) + "', takuki35 = '" + str(over35) + "', takuki_total = '" + str(total) + \
    #      "', prev_goals_home_team = '" + str(golos_m_eq_casa) + "', prev_goals_away_team = '" + str(golos_m_eq_fora) + "' where id = '" + str(game_id) + "'"
    print("##########################################")
    mycursor.execute(sql)
    conn.commit()
    disconnect(conn)


def nextRound(country, league):
    conn = connect()
    mycursor = conn.cursor()
    sql = "SELECT min(round) FROM games where realized = 'N' and country = '" + country + "' and league= '" + league + "'"
    print("SQL: " + sql)
    mycursor.execute(sql)
    round = mycursor.fetchone()
    disconnect(conn)
    return round

def calcula_estatistica(country, league):
    conn = connect()
    mycursor = conn.cursor()
    sql = "SELECT * FROM games where realized = 'Y' and country = '" + country + "' and league= '" + league + "' and takuki05 is not null"
    print("SQL: " + sql)
    mycursor.execute(sql)
    cursor = mycursor.fetchall()
    disconnect(conn)
    return cursor


def checkIfGamesExists(country, league, season):
    try:
        conn = connect()
        mycursor = conn.cursor()
        sql = "SELECT COUNT(id) from games where country = '%s' and league = '%s' and season = '%s'" % (country, league, season)
        mycursor.execute(sql)
        cursor = mycursor.fetchone()
        disconnect(conn)
        return cursor[0]
    except:
        print("Database error: %s" % checkIfGamesExists)

def insertGame(country, league, season, game_date, round, home_team, away_team, realized):
    argsList = [country, league, season, game_date, round, home_team, away_team, realized]
    try:
        conn = connect()
        mycursor = conn.cursor()

        result_args = mycursor.callproc('insertGame', argsList)
        conn.commit()

        if len(result_args) > 0:
            res = 1
        else:
            res = 0
        disconnect(conn)

        return res
    except:
        print("Database error: %s" % insertGame)

def getGames(country, league, season):
    try:
        conn = connect()
        mycursor = conn.cursor()
        sql = "SELECT * from games where country = '%s' and league = '%s' and season = '%s'" % (country, league, season)
        mycursor.execute(sql)
        cursor = mycursor.fetchall()
        disconnect(conn)
        return cursor
    except:
        print("Database error: %s" % checkIfGamesExists)
