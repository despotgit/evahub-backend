from db_config import getDb


def executeCustomQuery(sql, fetchOneRow=False):
    connection = getDb()
    cursor = connection.cursor()

    cursor.execute(sql)

    if fetchOneRow:
        results = cursor.fetchone()
    else:
        results = cursor.fetchall()

    return results
