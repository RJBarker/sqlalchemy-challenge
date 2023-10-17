# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    """Homepage - List all available api routes."""
    print("Request to homepage made...")
    return (
        f"Available Routes:<br/>"
        "<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precip():
    """Query 12 Months of Precipitation data - Return as JSON"""
    print("Request to Precipitation data made...")
    session

    annum_prcp = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >= dt.date(2016,8,23)).order_by(Measurement.date.desc()).all()

    session.close()

    # Convert results to a dictionary
    precip_annual = []
    for date, prcp in annum_prcp:
        precip_dict = {}
        precip_dict['date'] = date
        precip_dict['precipitation'] = prcp
        precip_annual.append(precip_dict)
    
    return jsonify(precip_annual)

@app.route("/api/v1.0/stations")
def stations():
    """Query a list of stations - Return as JSON"""
    print("Request to Station list data made...")
    session

    stations = session.query(Station).all()

    session.close()

    # Convert results to a dictionary
    station_list = []
    for station in stations:
        main_dict = {}
        main_dict['Station'] = station.station
        main_dict['Station_Details'] = {
            "ID":station.id,
            "Name":station.name,
            "Latitude":station.latitude,
            "Longitude":station.longitude,
            "Elevation":station.elevation
        }
        station_list.append(main_dict)

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    """Query a most active station - Return tobs as JSON"""
    print("Request for tobs of most active station made...")
    session

    tobs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == "USC00519281").filter(Measurement.date >= dt.date(2016,8,18)).all()

    session.close()

    


if __name__ == '__main__':
    app.run(debug=True)