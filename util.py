from . import mysql


def db_query(query, args):
    """
    A handler method for calling database procedures.

    :param query: the name of the query to be executed
    :type query: str
    :param args: arguments to pass in to the procedure
    :type args: tuple
    :return: a 2D tuple for result (becomes () if there is error), an error message (None if no error)
    :rtype: (tuple, str)
    """

    cur = mysql.connection.cursor()
    result, error = (), None
    try:
        cur.execute(query, args)
        result = cur.fetchall()
    except:
        error = mysql.connection.error()
    finally:
        cur.close()
        mysql.connection.commit()
    return result, error


def checkQuote(str):
    index = str.find("'")
    if "'" not in str:
        return str
    else:
        return str[:index+1] + "'" + str[index+1:]
