# INF tc3 - TD1

import wptools                                  # Cette librairie nous permet d'aller sur Wikipédia
import re                                       # Cette librairie nous permet de travailler avec les expressions régulières
import sqlite3                                  # Cette librairie nous permet de travailler des bases de données
from zipfile import ZipFile                     # Cette librairie nous permet de gérer les fichiers compressés
import json                                     # Cette librairie nous permet de gérer les fichiers json

conn = sqlite3.connect('pays.sqlite')           # Base de données avec laquelle on travaille

def get_info(name):
    """This function extracts datas from the Wikipedia page with the name name."""
    page = wptools.page(name)
    page.get_parse(False)
    return page.data['infobox']

def print_capital(info):
    """This function prints raw datas such as capital and coordinates"""
    k = info['capital']
    c = info['coordinates']
    return k, c

def get_name(info):
    """Extract the name of the contry. May return None"""
    try:
        return info['conventional_long_name']
    except:
        return None

def get_capital(info):
    """Extract the capital of the contry. May return None"""
    try:
        m = re.match('\[\[((\w+\s)*\w+)\]\]', info['capital'])
        k = m.group(1)
        return k
    except:
        return None

def get_coords(info):
    """Extract the coordinates of the contry. May return None
    Coordinates are positive or negative real number."""
    try:
        l = re.match('{{Coord\|(\w+)\|(\w+)\|(\w+)\|(\w+)\|(\w+)\|(\w+)\|type:city}}', info['coordinates'])
        lo = (int(l.group(1)) + int(l.group(2)) / 60) * ((l.group(3) == 'N') * 2 - 1)
        la = (int(l.group(4)) + int(l.group(5)) / 60) * ((l.group(6) == 'E') * 2 - 1)
        return {'lat':la, 'lon':lo}
    except:
        return None

def save_country(conn, country, info):
    """This function saves data of a country in the data base. May fill with NULL"""
    
    sql = 'INSERT INTO countries VALUES (?, ?, ?, ?, ?)'        # SQL command
    name = get_name(info)
    capital = get_capital(info)
    coords = get_coords(info)
    if name is None or capital is None or coords is None:       # If one data is not found
        temp = get_info(country)                                # We extract datas from wikipedia
        if name is None:                                        # Then try to refresh them
            name = get_name(temp)
        if capital is None:
            capital = get_capital(temp)
        if coords is None:
            coords = get_coords(temp)
    if name is None:                                            # But the data can be not found
        name = "NULL"                                           # In this case, they are replaced by NULL
    if capital is None:
        capital = "NULL"
    if coords is None:
        coords = {'lat' : "NULL", 'lon' : "NULL"}
    c = conn.cursor()                                           # Data base is opened
    c.execute(sql, (country, name, capital, coords['lat'], coords['lon']))
    conn.commit()                                               # Then closed (refresh)
    return

def read_country(conn, country):
    """This function extracts data in the data base"""
    c = conn.cursor()
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
            try:
                save_country(conn, z.namelist()[i][:-5], rd)
            except:
                pass
    return
