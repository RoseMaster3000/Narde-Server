import sqlite3
DBFILE = "Narde.db"


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
        if "insert" in query:
            connection.commit()
            return cursor.lastrowid
        elif ("select" or "show tables") in qry:
            result = res.fetchall()
            if "limit 1" in qry and len(result)>0:
                return result[0]
            return result
        else:
            connection.commit()
            return None
    # handle errors
    except Exception as error:
        print("\tDATABASE ERROR")
        print(error)
        print("\tDURING:")
        print(query)
        raise error
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


