import requests
from datetime import datetime, timedelta
from pars_html import head_data
import csv


def main_parse(id):
    result = []
    body_list = [{}]
    head_dict = {}
    count_for_prefix = 0
    main_url = f'http://www.flashscore.com/match/{id}/#/h2h/overall:80'
    url = f'http://d.flashscore.com/x/feed/df_hh_1_{id}'  # Тело страницы
    url_2 = f'http://d.flashscore.com/x/feed/dc_1_{id}'  # Шапка страницы
    response = requests.get(url, headers={
        "x-fsign": "SW9D1eZo"})  # Передаем ключь
    response_2 = requests.get(url_2, headers={
        "x-fsign": "SW9D1eZo"})  # Передаем ключь
    res = (response.text).replace('÷', ':')
    res = (res).split('¬')
    res_2 = (response_2.text).replace('÷', ':')
    res_2 = (res_2).split('¬')
    country_type_of_competition_1, type_of_competition_1, name_1, url_1, name_2, url_2 = head_data(main_url)



    '''Основное тело страницы'''
    for i in res[:-2]:
        if 'Last matches' in i or 'Head-to-head matches' in i:
            count_for_prefix += 1
        key = (i.split(':'))[0]
        value = (i.split(':'))[1]
        if '~' in i:
            body_list.append({key: value})
            body_list[-1].update({'Prefix': count_for_prefix})
        else:
            body_list[-1].update({key: value})


    '''Шапка страницы'''
    for e in res_2[:-2]:
        key = (e.split(':'))[0]
        value = (e.split(':'))[1]
        if key == 'DC':
            head_dict[key] = datetime.utcfromtimestamp(int(value)).strftime('%Y-%m-%d %H:%M:%S')
        else:
            head_dict[key] = value



    '''Собираем итоговую строку'''
    for el in body_list:
        p = el.get('Prefix', 0)
        if p >= 4:
            break
        elif '~KC' in el and p < 4:
            result.append(f"{main_url}, "                                                                               # Основной url
                          f"{head_dict.get('DC')}, "                                                                    # Дата (осн, в шапке страницы)
                          f"{head_dict.get('DE')}:{head_dict.get('DF')} - {head_dict.get('DG')}:{head_dict.get('DH')}, "# Счет (осн, в шапке страницы)
                          f"{name_1}, "                                                                                 # Команда 1 (осн, в шапке страницы)
                          f"{url_1}, "                                                                                  # Url команды 1 (в шапке страницы)
                          f"{name_2}, "                                                                                 # Команда 2 (осн, в шапке страницы)
                          f"{url_2}, "                                                                                  # Url команды 2 (в шапке страницы)
                          f"{country_type_of_competition_1}, "                                                          # Страна состязания (осн, в шапке страницы)
                          f"{type_of_competition_1}, "                                                                  # Тип состязания (осн, в шапке страницы)
                          f"K{el.get('Prefix')}, "                                                                      # Префикс
                          f"{el.get('KH')}, "                                                                           # Страна состязания
                          f"{el.get('KF')}, "                                                                           # Тип состязания
                          f"{datetime.fromtimestamp(0) + timedelta(seconds=int(el.get('~KC')))}, "                      # Дата игры
                          f"{el.get('KJ')}, "                                                                           # Команда 1
                          f"{el.get('FK')}, "                                                                           # Команда 2
                          f"{(el.get('KX', el.get('KL')))}:{(el.get('KY', el.get('KT')))}, "                            # Счет игры
                          f"{el.get('KN')}"                                                                             # Обозначение LDW
                          )


    with open('result.csv', mode='a', newline='', encoding="utf-8") as r:
        writer = csv.writer(r, delimiter=";")
        for i in result:
            writer.writerow(i.split(', '))

# #
# if __name__ == '__main__':
#     main_parse('GbmbesUO')
