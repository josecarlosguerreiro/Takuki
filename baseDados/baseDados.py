import mysql.connector


def connect():
    try:
        mydb = mysql.connector.connect(user='root', password='2111986kramermania',
                                       host='127.0.0.1',
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


def addGame(game):
    conn = connect()
    mycursor = conn.cursor()
    mycursor.callproc('addGame', [game.getLeague(), game.getSeason(), game.getData(), game.getRound(),
                                  game.getHomeTeam(), game.getAwayTeam(), game.getHomeGoals(), game.getAwayGoals(),
                                  game.getRealized(), ])
    conn.commit()
    disconnect(conn)


def getAllGames(league):
    conn = connect()
    mycursor = conn.cursor()
    sql = "SELECT * FROM games where league = '" + league + "'"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    disconnect(conn)
    return myresult


def getGame(game):
    conn = connect()
    mycursor = conn.cursor()
    sql = "SELECT * FROM games WHERE league = '" + game.getLeague() + "' and season= '" + game.getSeason() +\
          "' and game_date = '" + game.getData() + "' and round = '" + game.getRound() + "' and home_team = '" + \
          game.getHomeTeam() + "' and away_team = '" + game.getAwayTeam() + "' and realized = '" + game.getRealized() + "'"
    mycursor.execute(sql)
    myresult = mycursor.fetchone()
    disconnect(conn)
    return myresult


def getHomeGames(team, round):
    conn = connect()
    mycursor = conn.cursor()
    sql = "SELECT * FROM games where home_team = '" + team + "' and round <= '" + str(round) + "'"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    disconnect(conn)
    return myresult


def getAwayGames(team, round):
    conn = connect()
    mycursor = conn.cursor()
    sql = "SELECT * FROM games where away_team = '" + team + "' and round <= '" + str(round) + "'"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    disconnect(conn)
    return myresult

def updateTotalGoals(homeTeam, awayTeam, round, goals):
    conn = connect()
    mycursor = conn.cursor()
    sql = "update games set total_goals = '" + str(goals) + "' where home_team = '" + homeTeam + "' and away_team = '" + awayTeam + "' and round = '" + str(round) + "'"
    mycursor.execute(sql)
    conn.commit()
    disconnect(conn)