import logging
from sql import Sql
from response import Response


class Details:

    @staticmethod
    def get_all(number):
        conn = None
        try:
            conn, cur = Sql.get_connection()
            logging.debug("Connection and cursor received")

            sql_query = "select name, number, vehicle from drivers where number  = '{0}'"
            cur.execute(sql_query.format(number))
            data = cur.fetchall()
            result = Response.make_response(200, "Vehicle number updated", "Vehicle number updated", name = data[0], number = data[1], vehicle = data[2])
            conn.close()
            logging.debug("Connection closed")
            return result
        except Exception as e:
            if conn is not None:
                conn.close()
            logging.error("Error in getting all details: " + str(e))
            error = Response.make_response(500, "System failure", "Oops something went wrong !")
            return error
