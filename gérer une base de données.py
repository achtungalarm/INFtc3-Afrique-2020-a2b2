# INF tc3 - TD1

import wptools                                  # Cette librairie nous permet d'aller sur Wikipédia
import re                                       # Cette librairie nous permet de travailler avec les expressions régulières
import sqlite3                                  # Cette librairie nous permet de travailler des bases de données
from zipfile import ZipFile                     # Cette librairie nous permet de gérer les fichiers compressés
import json                                     # Cette librairie nous permet de gérer les fichiers json

conn = sqlite3.connect('pays.sqlite')           # Base de données avec laquelle on travaille

def get_info(name):
    """This function extracts datas from the Wikipedia page with the name name."""
    page = wptools.page(name)                   # On va sur Wikipedia
    page.get_parse(False)                       # On regroupe les informations
    return page.data['infobox']                 # On renvoie les données du bandeau de droite de Wikipédia

def print_capital(info):
    """This function prints json datas such as capital and coordinates"""
    k = info['capital']
    c = info['coordinates']
    return k, c

def get_name(info):
    """Extract the name of the contry. May return None"""
    return info['conventional_long_name']


def get_capital(info):
    """Extract the capital of the contry. May return None"""
    cap = info['capital']
    cap = cap[cap.index('['):cap.index(']')+2]
    m = re.match('\[\[((\w+\s)*(\w+-)*(\w+\')*\w+)\]\]',cap)
    if m is None:
        m =re.match('\[\[(\w+)\,\s(\w+)\|(\w+)\]\]', cap)
    if m is None:
        cap = cap[:cap.index('(')]
        m =re.match('\[\[(\w+)\s', cap)
    k = m.group(1)
    return k


def get_coords(info):
    """Extract the coordinates of the contry. May return None
    Coordinates are positive or negative real number."""
    try:
        coo = info['coordinates']
    except:
        return None
    try:
        i = coo.index('E')
    except:
        i = coo.index('W')
    try:
        coo = coo[:i+1]
        l = re.match('{{coord\s*\|\s*(\w+)\s*\|\s*(\w+.*\w*)\s*\|\s*(\w+)\s*\|\s*(\w+)\s*\|\s*(\w+.*\w*)\s*\|\s*(\w+)\s*', coo.lower())
        if l is None:
            l = re.match('{{coord\s*\|(\w+)\|(\w+)\|(\w+)\|(\w+)\|(\w+)\|(\w+)\|(\w+)\|(\w+)', coo.lower())
            lo = (int(l.group(1)) + int(l.group(2)) / 60 +  int(l.group(3)) / 3600) * ((l.group(4) == 'n') * 2 - 1)
            la = (int(l.group(5)) + int(l.group(6)) / 60 +  int(l.group(7)) / 3600) * ((l.group(8) == 'e') * 2 - 1)
            return {'lat':la, 'lon':lo}
        lo = (int(l.group(1)) + float(l.group(2)) / 60) * ((l.group(3) == 'n') * 2 - 1)
        la = (int(l.group(4)) + float(l.group(5)) / 60) * ((l.group(6) == 'e') * 2 - 1)
        return {'lat':la, 'lon':lo}
    except:
        return None

def save_country(conn, country, info):
    sql = 'INSERT INTO countries VALUES (?, ?, ?, ?, ?)'
    name = get_name(info)
    capital = get_capital(info)
    coords = get_coords(info)
    if coords is None:
        dat = get_info(capital)
        coords = get_coords(dat)
    c = conn.cursor()
    c.execute(sql, (country, name, capital, coords['lat'], coords['lon']))
    conn.commit()
    return

def read_country(conn, country=None):
    """This function extracts data in the data base"""
    c = conn.cursor()
    if country is None:
        sql = 'SELECT * FROM countries'
        inf = c.execute(sql, (country, ))
    else:
        sql = 'SELECT * FROM countries WHERE wp = ?'
        inf = c.execute(sql, (country, ))
    t = inf.fetchall()
    conn.commit()
    if t == []:
        return None
    return t

def edit_country(conn, country, capital=None, lon=None, lat=None):
    """This functon allow us to edit datas in Data base"""
    c = conn.cursor()
    sql = 'UPDATE countries SET '
    if capital is not None:
        sql += 'capital = {}, \n'.format(capital)
    if lon is not None:
        sql += 'longitude = {}, \n'.format(lon)
    if lat is not None:
        sql += 'latitude = {}, \n'.format(lat)
    sql = sql[:-3] + '\n'
    sql += 'WHERE wp = ?'.format(country)
    c.execute(sql, (country, ))
    conn.commit()
    return

def save_all(file, conn):
    """This function saves all the datas that are in the compressed file"""
    with ZipFile(file + '.zip','r') as z:
        for i in range(len(z.namelist())):
            rd = json.loads(z.read(z.namelist()[i]))
            save_country(conn, z.namelist()[i][:-5], rd)
    return
