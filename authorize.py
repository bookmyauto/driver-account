"""
                Description : contains code for authorization
                Author      : Rahul Tudu
"""
import  jwt
import  requests
from    datetime import  datetime
import  logging


class Authorize:

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
    #                                                   VERTIFYING JWT AND EXPIRY TIME                                                                                          #
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
    @staticmethod
    def verify_jwt(user_number, token):
        try:
            payload                 = jwt.decode(token, verify = False)
            timestamp               = datetime.timestamp(datetime.now())
            payload_number          = payload["number"]
            expiry_timestamp        = payload["exp"]
            logging.debug("  " + str(user_number) + ":  Payload decrypted")
            if user_number == payload_number:
                if timestamp <= expiry_timestamp:
                    result_decode   = jwt.decode(token, 'mandolin', algorithm = 'HS256')
                    logging.debug("  " + str(user_number) + ":  Signature decoded")
                    return 1, ""
                else:
                    response        = requests.get("https://127.0.0.1:8080/v1/getJWT/" + str(user_number))
                    logging.debug("  " + str(user_number) + ":  New token fetched")
                    response        = response.json()
                    if response["token"] == "":
                        raise ValueError
                    else:
                        return 1, response["token"]
            else:
                return 0, ""
        except Exception as e:
            logging.critical("  " + str(user_number) + ":  Error in verify_jwt authorization: " + str(e))
            return 0, ""

