# INF tc3 - TD1

import wptools                                  # Cette librairie nous permet d'aller sur Wikipédia
import re                                       # Cette librairie nous permet de travailler avec les expressions régulières
import sqlite3                                  # Cette librairie nous permet de travailler des bases de données
from zipfile import ZipFile                     # Cette librairie nous permet de gérer les fichiers compressés
import json                                     # Cette librairie nous permet de gérer les fichiers json

conn = sqlite3.connect('pays.sqlite')  

def get_all(country):                            # Base de données du TD1                                         
    page = wptools.page(country,silent=True)     # Tester si le programme marche
    page.get_parse(False)
    return(page.data['infobox'])e

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
        coo = coo[:i+1]
    except:
        try:
            i = coo.index('W')
            coo = coo[:i+1]
        except:
            pass
    try:
        l = re.match('{{coord\s*\|\s*(\w+)\s*\|\s*(\w+)\s*\|\s*(\w+)\s*\|\s*(\w+)\s*\|\s*(\w+)\s*\|\s*(\w+)', coo.lower())
        if l is not None:
            if l.group(6) != 'e' and l.group(6) != 'w':
                l = None
        if l is None:
            l = re.match('{{coord\s*\|\s*(\w+)\s*\|\s*(\w+).(\w+)\s*\|\s*(\w+)\s*\|\s*(\w+)\s*\|\s*(\w+).(\w+)\s*\|\s*(\w+)', coo.lower())
        if l is None:
            l = re.match('{{coord\s*\|\s*(\w+)\s*\|\s*(\w+)\|(\w+)\s*\|\s*(\w+)\s*\|\s*(\w+)\s*\|\s*(\w+)\|(\w+)\s*\|\s*(\w+)', coo.lower())
        if l is None:
            coo = coo[:coo.index('t')]
            l = re.match('{{coord\|(\w+).(\w+)\|-(\w+).(\w+)\|', coo.lower())
        try:
            la = (int(l.group(1)) + int(l.group(2)) / 60 +  int(l.group(3)) / 3600) * ((l.group(4) == 'n') * 2 - 1)
            lo = (int(l.group(5)) + int(l.group(6)) / 60 +  int(l.group(7)) / 3600) * ((l.group(8) == 'e') * 2 - 1)
            return {'lat':lo, 'lon':la}
        except:
            try:
                la = (int(l.group(1)) + float(l.group(2)) / 60) * ((l.group(3) == 'n') * 2 - 1)
                lo = (int(l.group(4)) + float(l.group(5)) / 60) * ((l.group(6) == 'e') * 2 - 1)
                return {'lat':lo, 'lon':la}
            except:
                la = int(l.group(1)) + int(l.group(2)) / 100
                lo = -int(l.group(3)) - int(l.group(4)) / 100
                return {'lat': lo, 'lon': la}
    except:
        return None

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
