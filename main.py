from flask import Flask
from flask import request
from authorize import Authorize
from otp import Otp
from create import Create
from vehicle import Vehicle
from details import Details
import logging
import requests
import json

import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)

default_error = json.dumps(
    {"errorCode": 500, "errorMessage": "System failure", "displayMessage": "Oops something went wrong !"})

logging.info("python code started")


@app.route("/v1")
def working():
    return {"response": "driver-account service running"}


# otp related actions
@app.route("/v1/otp", methods=["GET"])
def otp():
    try:
        if request.method == "GET":
            number = request.args["number"]
            logging.debug("incoming request: number = " + str(number))
            if "otp" not in request.args:
                response = json.dumps(Otp.create_otp(number))
                return response
            else:
                user_otp = request.args["otp"]
                logging.debug("incoming request: otp = " + str(otp))
                response = json.dumps(Otp.verify_otp(number, user_otp))
                return response
    except RuntimeError as e:
        logging.critical("failure in v1/otp with error: " + str(e))
        return default_error


# creation of user is handled here
@app.route("/v1/createdriver", methods=["GET", "POST"])
def createdriver():
    try:
        if request.method == "GET":
            logging.debug("incoming GET request: " + str(dict(request.args)))
            driver_number = request.args["number"]
            response = Create.check_driver_repetition(driver_number)
            logging.debug("createdriver returned: " + str(response))
            return response
        if request.method == "POST":
            logging.debug("incoming POST request: " + str(request.form))
            driver_name = request.form["name"]
            driver_number = request.form["number"]
            response = Create.create_user(driver_number, driver_name)
            logging.debug("createuser returned:\n" + str(response))
            return response
    except RuntimeError as e:
        logging.critical("failure in v1/createuser with error: " + str(e))
        return default_error


@app.route("/v1/updatedriver", methods=["POST"])
def updatedriver():
    try:
        if request.method == "POST":
            number = request.form["number"]
            name = request.form["name"]
            photo_link = request.args["profile_pic_link"]
            response = Create.update_user(number, name, photo_link)
            logging.debug("Responded to update driver request")
            return response
    except RuntimeError as e:
        logging.critical(
            "failure in v1/updateriver with error: " + str(e) + " |for request: " + str(dict(request.args)))
        return default_error


# --------------------------------------------------------------------------------------------------------------------------------------------- #
#                                                       LOGIN AND RETURN JWT                                                                    #
# --------------------------------------------------------------------------------------------------------------------------------------------- #
@app.route("v1/login", methods=["GET"])
def login():
    try:
        if request.method == "GET":
            logging.info("  Incoming request:\n" + str(request.args))
            number = request.args["number"]
            response = requests.get("https://127.0.0.1:8080/v1/getJWT/" + str(number))
            response = response.json()
            if response["data"]["token"] == "":
                raise ValueError
            else:
                logging.info("  Response:\n" + str(response))
                return response
    except RuntimeError as e:
        logging.critical("  Failure in v1/login with error: " + str(e))
        return default_error


# updation of vehicle is done here
@app.route("/v1/updateVehicle", methods=["POST"])
def update_vehicle():
    try:
        if request.method == "POST":
            jwt_token = request.headers["token"]
            driver_number = request.headers["number"]
            stat, tok = Authorize.verify_jwt(driver_number, jwt_token)
            if stat == 0:
                raise ValueError("Not authorized")

            logging.debug("incoming POST request: " + str(request.form))
            driver_vehicle = request.form["vehicle"]
            response = Vehicle.update_vehicle(driver_number, driver_vehicle)
            logging.debug("updateVehicle returned:\n" + str(response))
            return response
    except RuntimeError as e:
        logging.critical("failure in v1/updateVehicle with error: " + str(e))
        return default_error


# getting driver details is done here
@app.route("/v1/getalldetails", methods=["POST"])
def get_all_details():
    try:
        if request.method == "POST":
            jwt_token = request.headers["token"]
            driver_number = request.headers["number"]
            stat, tok = Authorize.verify_jwt(driver_number, jwt_token)
            if stat == 0:
                raise ValueError("Not authorized")

            logging.debug("incoming POST request: " + str(request.form))
            response = Details.get_all(driver_number)
            logging.debug("getalldetails returned:\n" + str(response))
            return response
    except RuntimeError as e:
        logging.critical("failure in v1/getalldetails with error: " + str(e))
        return default_error


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=7001, ssl_context='adhoc')
