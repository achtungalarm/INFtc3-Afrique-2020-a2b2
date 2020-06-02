# INF tc3 - TD1

import wptools
import re
import sqlite3
from zipfile import ZipFile
import json

conn = sqlite3.connect('pays.sqlite')

def get_info(name):
    page = wptools.page(name)
    page.get_parse(False)
    return page.data['infobox']

def print_capital(info):
    k = info['capital']
    c = info['coordinates']
    return k, c

def get_name(info):
    try:
        return info['conventional_long_name']
    except:
        return None

def get_capital(info):
    try:
        m = re.match('\[\[((\w+\s)*\w+)\]\]', info['capital'])
        k = m.group(1)
        return k
    except:
        return None

def get_coords(info):
    try:
        l = re.match('{{Coord\|(\w+)\|(\w+)\|(\w+)\|(\w+)\|(\w+)\|(\w+)\|type:city}}', info['coordinates'])
        lo = (int(l.group(1)) + int(l.group(2)) / 60) * ((l.group(3) == 'N') * 2 - 1)
        la = (int(l.group(4)) + int(l.group(5)) / 60) * ((l.group(6) == 'E') * 2 - 1)
        return {'lat':la, 'lon':lo}
    except:
        return None

def save_country(conn, country, info):
    sql = 'INSERT INTO countries VALUES (?, ?, ?, ?, ?)'
    name = get_name(info)
    capital = get_capital(info)
    coords = get_coords(info)
    if name is None or capital is None or coords is None:
        temp = get_info(country)
        if name is None:
            name = get_name(temp)
        if capital is None:
            capital = get_capital(temp)
        if coords is None:
            coords = get_coords(temp)
    if name is None:
        name = "NULL"
    if capital is None:
        capital = "NULL"
    if coords is None:
        coords = {'lat' : "NULL", 'lon' : "NULL"}
    c = conn.cursor()
    c.execute(sql, (country, name, capital, coords['lat'], coords['lon']))
    conn.commit()
    return

def read_country(conn, country):
    c = conn.cursor()
    sql = 'SELECT * FROM countries WHERE wp = ?'
    inf = c.execute(sql, (country, ))
    t = inf.fetchall()
    conn.commit()
    if t == []:
        return None
    return t

def edit_country(conn, country, capital=None, lon=None, lat=None):
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
    with ZipFile(file + '.zip','r') as z:
        for i in range(len(z.namelist())):
            rd = json.loads(z.read(z.namelist()[i]))
            try:
                save_country(conn, z.namelist()[i][:-5], rd)
            except:
                pass
    return
