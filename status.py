import  logging
from    bson import ObjectId
from    sql import Sql
from    response import Response


class Status:

    @staticmethod
    def change_status(number, curr_status):
        conn    = None
        try:
            conn, cur       = Sql.get_connection()
            logging.debug("Connection and cursor received")
            sql_query       = "insert into driver_status (driver_number, status, curr_lat, curr_long) values ('{0}', {1}, {2}, {3}) on duplicate key update status = {1}"
            cur.execute(sql_query.format(number, curr_status, -181.0, -181.0))
            conn.commit()
            conn.close()
            logging.debug(" Status of driver " + str(driver_number) + " changed to " + str(curr_status))
            result          = Response.make_response(200, "Current status of driver changed", "Current status of driver changed")
            return result
        except Exception as e:
            if conn is not None:
                conn.close()
            logging.error("Error in changing driver status: " + str(e))
            error = Response.make_response(500, "System failure", "Oops something went wrong !")
            return error
