import pandas as pd

from public.SqlOperator import SqlOperator


def oddanayls(oddlist):

    willlist = [ odd for odd in oddlist if odd.company=='will']
    lablist = [odd for odd in oddlist if odd.company == 'lab']

    will0 = willlist[0]
    lab0 = lablist[0]

    for will in willlist[1:]:
        if will0.win > will.win:
            willup = 1


def peal():
    all_data_set = SqlOperator().jcengine()
    data = all_data_set.loc[
        (all_data_set['season'].isin(['2019-2020', '2020-2021', '2021-2022'])) & (
                all_data_set["matchname"] == "英超")]

    data['result'] = data['result'].map({'胜': 3, '平': 1, '负': 0})

    data['hjinqiu'] = data['bifen'].apply(lambda x: str(x).split('-')[0]).astype('int64')
    data['gjinqiu'] = data['bifen'].apply(lambda x: str(x).split('-')[1]).astype('int64')

    datas = data[
        ['hcorner', 'hgoal', 'hgoalon', 'hattack', 'hdangerattack', 'htargetoff', 'hgoalblock', 'hfreekick',
         'hpass', 'hfoul', 'hoffside', 'hheader', 'hheaderon', 'hsaveball',
         'htackleball', 'hsurpass', 'houtball', 'hsteal', 'hintercept', 'hassist', 'gcorner', 'ggoal',
         'ggoalon', 'gattack',
         'gdangerattack', 'gtargetoff', 'ggoalblock', 'gfreekick', 'gpass',
         'gfoul', 'goffside', 'gheader', 'gheaderon', 'gsaveball', 'gtackleball', 'gsurpass', 'goutball',
         'gsteal',
         'gintercept', 'gassist', 'hjinqiu', 'gjinqiu', 'result']]

    return datas

