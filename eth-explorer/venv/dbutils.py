import psycopg2
import json

from configparser import ConfigParser
from hexbytes import HexBytes


def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db


class HexJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, HexBytes):
            return obj.hex()
        return super().default(obj)


def get_db_connection():
    conn = None
    try:
        params = config()
        # print('Connecting to the DB')
        conn = psycopg2.connect(**params)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return conn


def storevalues(sql, values):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()


def getvalues(sql):
    # sql = """select "blockNumber","hash","from","to","input" from transaction_information where "input" LIKE '0xa9059cbb%' order by "blockNumber" DESC"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    values = cursor.fetchall()
    conn.commit()
    cursor.close()
    return values
