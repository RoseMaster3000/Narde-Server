import sqlite3
from sys import exc_info
DBFILE = "Narde.db"

def getException():
    _, _, tb = exc_info()
    fileName = tb.tb_frame.f_code.co_filename
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
    # validate / sanatize args
    if len(data)==1 and type(data[0]) in [list,tuple]: data=tuple(data[0])
    if type(data)!=tuple: raise ValueError("querySQL expects arbitrarty args (*args)")
    qry = query.lower().split()
    # connect
    connection = getConnection()
    cursor = connection.cursor()
    try:
        # run query
        if len(data)==0:
            res = cursor.execute(query)
        else:
            res = cursor.execute(query, data)
        # return query result (contextually)
        if "insert" in qry or "update" in qry:
            connection.commit()
            return cursor.lastrowid
        elif "select" in qry:
            result = res.fetchall()
            if "limit 1" in " ".join(qry):
                return result[0] if len(result)>0 else None
            else:
                return result
        elif "show tables" in qry:
            return listTables()
        else:
            connection.commit()
            return None
    # handle errors
    except Exception as error:
        warning(f"DATABASE ERROR:")
        warning(f"{query}")
        warning(f"{error.args[0]}")
        warning(getException())
        return []
    # close
    finally:
        connection.close()


def listTables():
    result = querySQL((
        "SELECT name FROM sqlite_schema "
        "WHERE type ='table' AND name NOT LIKE 'sqlite_%';"
    ))
    return [table['name'] for table in result]


