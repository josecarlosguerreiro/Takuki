import re
import datetime


class obj_campeonato:
    def __init__(self, campeonato, link):
        self.campeonato = campeonato
        self.link = link

    def getCampeonato(self):
        return self.campeonato

    def getLink(self):
        return self.link


def getDate(date_row):
    game_dt = ''
    date_line = str(date_row).replace('<span class="hide-mobile">', '')
    start_date_str = str(date_line).split('>')
    end_date_str = str(start_date_str).split('<')
    game_date = str(end_date_str[1])
    game_date2 = str(game_date).split(',')[1].replace(' ', '').replace('\'', '').replace('-', '').replace('\\n', '')

    if 'jan' in game_date2:
        game_dt = game_date2.replace('jan', '01')
    if 'fev' in game_date2:
        game_dt = game_date2.replace('fev', '02')
    if 'mar' in game_date2:
        game_dt = game_date2.replace('mar', '03')
    if 'abr' in game_date2:
        game_dt = game_date2.replace('abr', '04')
    if 'mai' in game_date2:
        game_dt = game_date2.replace('mai', '05')
    if 'jun' in game_date2:
        game_dt = game_date2.replace('jun', '06')
    if 'jul' in game_date2:
        game_dt = game_date2.replace('jul', '07')
    if 'ago' in game_date2:
        game_dt = game_date2.replace('ago', '08')
    if 'set' in game_date2:
        game_dt = game_date2.replace('set', '09')
    if 'out' in game_date2:
        game_dt = game_date2.replace('out', '10')
    if 'nov' in game_date2:
        game_dt = game_date2.replace('nov', '11')
    if 'dez' in game_date2:
        game_dt = game_date2.replace('dez', '12')

    day = game_date2.split('.')[0]
    month = game_dt.split('.')[1]
    year = game_date2.split('.')[2]
    #print("DAyYYY: " + str(day))
    #print("month: " + str(month))
    #print("year: " + str(year))
    date_complete = datetime.datetime(int(year), int(month), int(day))
    date = date_complete.strftime("%Y-%m-%d")
    #print("DATA: " + str(date))
    return date


def getEpoca(game_date):
    '''
    game_date: 2022-04-09
    '''
    game_date = str(game_date).split('-')
    #    print("get epoca.mes: " + game_date)
    mes = game_date[1]
    ano = game_date[0]
    if (mes >= '08') and (mes <= '12'):
        epoca = ano + '/' + str(int(ano) + 1)
    else:
        epoca = str(int(ano) - 1) + '-' + ano
    return epoca


def getResultado(res_line):
    res = str(res_line).split('>')
    res2 = res[2].split('<')
    res3 = str(res2[0])
    resultado = re.sub(r"[\n\t\s\n]*", "", res3)
    if resultado.__contains__('-'):
        pass
    else:
        resultado = 'vs'
    return resultado


def golosCasa(resultado):
    golos = resultado.split('-')
    return golos[0]


def golosFora(resultado):
    golos = resultado.split('-')
    return golos[1]


def getRound(round_line):
    round_2 = str(round_line).split('>')
    round_3 = round_2[1].split('<')
    round = str(round_3[0])
    round = re.sub(r"[\n\t\s\n]*", "", round)
    round = round.replace('J', '')
    return round


def getTeam(soup_list):
    # for td in soup_list:
    #    rows = td.find_all('td')
    home_team_row = soup_list
    home_team_a = home_team_row.find('a')
    home_team_2 = str(home_team_a).split('>')
    home_team_3 = home_team_2[1].split('<')
    home_team = home_team_3[0]
    return home_team


class obj_game:
    def __init__(self, league, season, dt, round, home_team, away_team, home_goals, away_goals, realized, total_goals):
        self.league = league
        self.season = season
        self.game_date = dt
        self.round = round
        self.home_team = home_team
        self.away_team = away_team
        self.home_goals = home_goals
        self.away_goals = away_goals
        self.realized = realized
        self.total_goals = total_goals

    def obj_game(self, league, season, dt, round, home_team, away_team, home_goals, away_goals, realized, total_goals):
        self.league = league
        self.season = season
        self.game_date = dt
        self.round = round
        self.home_team = home_team
        self.away_team = away_team
        self.home_goals = home_goals
        self.away_goals = away_goals
        self.realized = realized
        self.total_goals = total_goals
    '''
    def __init__(self, league, season, dt, round, home_team, away_team):
        self.league = league
        self.season = season
        self.game_date = dt
        self.round = round
        self.home_team = home_team
        self.away_team = away_team
    '''
    def getLeague(self):
        return self.league

    def getSeason(self):
        return self.season

    def getData(self):
        return self.game_date

    def getRound(self):
        return self.round

    def getHomeTeam(self):
        return self.home_team

    def getAwayTeam(self):
        return self.away_team

    def getHomeGoals(self):
        return self.home_goals

    def getAwayGoals(self):
        return self.away_goals

    def getRealized(self):
        return self.realized

    def getTotalGoals(self):
        return self.total_goals
