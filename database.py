import sqlite3
from sys import exc_info
DBFILE = "Narde.db"

def getException():
    _, _, tb = exc_info()
    f = tb.tb_frame
    fileName = f.f_code.co_filename
    lineNum = tb.tb_lineno
    return '{} : {}'.format(fileName, lineNum)


def warning(*args):
    RED = '\033[0;31m'
    END = '\033[0m'
    print(f'{RED}ERROR{END}:    ', end='')
    print(*args)


def getConnection():
    connection = sqlite3.connect(DBFILE)
    connection.row_factory = dict_factory
    return connection


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def querySQL(query, *data):
    qry = query.lower()
    connection = getConnection()
    cursor = connection.cursor()
    try:
        # run query
        if len(data)==0 or data[0]==None:
            res = cursor.execute(query)
        elif type(data[0])==tuple:
            res = cursor.execute(query, data[0])
        else:
            res = cursor.execute(query, data)
        # return query result (contextually)
        if "insert" in qry:
            connection.commit()
            return cursor.lastrowid
        elif ("select" or "show tables") in qry:
            result = res.fetchall()
            if "limit 1" in qry and len(result)>0:
                return result[0]
            elif "limit 1" in qry and len(result)==0:
                return None
            else:
                return result
        else:
            connection.commit()
            return None
    # handle errors
    except Exception as error:
        print()
        print(f"DATABASE ERROR:")
        print(f"  [?] {query}")
        print(f"  [!] {error.args[0]}")
        print()
        return []
    # close
    finally:
        connection.close()


def listTables():
    result = querySQL((
        "SELECT name FROM sqlite_schema "
        "WHERE type ='table' AND name NOT LIKE 'sqlite_%';"
    ))
    tables = [table['name'] for table in result]
    print(tables)
    return tables


