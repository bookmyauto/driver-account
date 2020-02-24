import logging
from sql import Sql
from response import Response


class Vehicle:

    @staticmethod
    def update_vehicle(number, vehicle_number):
        conn = None
        try:
            conn, cur = Sql.get_connection()
            logging.debug("Connection and cursor received")

            # update in db
            sql_query = "update drivers set vehicle = '{0}' where number  = '{1}'"
            cur.execute(sql_query.format(vehicle_number, number))
            conn.commit()
            result = Response.make_response(200, "Vehicle number updated", "Vehicle number updated")
            conn.close()
            logging.debug("Connection closed")
            return result
        except Exception as e:
            if conn is not None:
                conn.close()
            logging.error("Error in updating vehicle: " + str(e))
            error = Response.make_response(500, "System failure", "Oops something went wrong !")
            return error
