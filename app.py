from flask import Flask, jsonify, render_template

import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import numpy as np
import json
import pandas as pd

# Create egine for database connection
sql = "sqlite:///Resources/hawaii.sqlite"
engine = create_engine(sql, pool_pre_ping=True)

# Create autmap_base 
Base = automap_base()
# Reflect database tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

# Setup Flask

app = Flask(__name__)

# Create initital route with route's summary
@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Weather API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date<br/>"
        f"Please enter date as yyyy-mm-dd")
    
# Create an app route to returning date and percipitation data in JSON format

@app.route("/api/v1.0/precipitation")
def preci():
    """Return Percipitation Data - 1 year"""
    # Create a variable to filter only the last year of analysis
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Query for the date and precipitation for the last year
    rainfall = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= last_year).all()
    # Transform our query into a list
    rain = list(np.ravel(rainfall))
    # Return the data in json format
    return jsonify(rain=rain)

@app.route("/api/v1.0/stations")
def stations():
    """List of stations."""
    # Query the name of each station in our DB
    stat = session.query(Station.station).all()
    # Transform our query into a list
    station_list = list(np.ravel(stat))
    # Return the data in json format
    return jsonify(station_list=station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create a variable to filter only the last year of analysis
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    temp = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= last_year).all()
    
    tobs_list = list(np.ravel(temp))
    
    return jsonify(tobs_list=tobs_list)

@app.route("/api/v1.0/<start_date>")
def st(start=None):
    
    start_temp = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date >= start).all()

    start_list = list(np.ravel(start_temp))
    
    return jsonify(start_list=start_list)

@app.route("/api/v1.0/<start_date>/<end_date>")
def st_end(start=None ,end=None):
    
    min_max = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date >= start, Measurement.date <= end).all()

    min_max_list = list(np.ravel(min_max))
    
    return jsonify(min_max_list=min_max_list)


if __name__ == '__main__':
    app.run()