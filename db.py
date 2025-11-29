from db_config import getDb


def executeCustomQuery(sql, fetchOneRow=False):
    connection = getDb()
    cursor = connection.cursor()

    try:
        cursor.execute(sql)

        # Commit for any query that modifies data
        if sql.strip().lower().startswith(("insert", "update", "delete")):
            connection.commit()

        # Fetch results only for SELECT queries
        if sql.strip().lower().startswith("select"):
            if fetchOneRow:
                results = cursor.fetchone()
            else:
                results = cursor.fetchall()
        else:
            results = None  # For non-SELECT queries

        return results

    except Exception as e:
        connection.rollback()
        raise e

    finally:
        cursor.close()
        connection.close()
