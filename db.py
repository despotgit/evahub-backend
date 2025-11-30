from db_config import getDb


def executeCustomQuery(sql, fetchOneRow=False):
    """
    Executes a SQL query and returns results if SELECT.
    Automatically commits for INSERT/UPDATE/DELETE.
    Rolls back on exception.
    Logs the SQL and errors for debugging.
    """
    connection = getDb()
    cursor = connection.cursor()

    try:
        print("🔥 Executing SQL:", sql)
        cursor.execute(sql)

        # Commit for queries that modify data
        if sql.strip().lower().startswith(("insert", "update", "delete")):
            connection.commit()
            print("✅ Commit successful")

        # Fetch results only for SELECT queries
        if sql.strip().lower().startswith("select"):
            if fetchOneRow:
                results = cursor.fetchone()
            else:
                results = cursor.fetchall()
            print("✅ Query results:", results)
        else:
            results = None

        return results

    except Exception as e:
        print("❌ SQL execution error:", e)
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()
        print("🔒 Connection closed")
