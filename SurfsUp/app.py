import numpy as np

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

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################


@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to Honolulu, Hawaii - Climate Data API<br/><br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2016-08-23<br/>"
        f"/api/v1.0/2016-08-23/2017-08-18"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    # Perform a query to retrieve the data and precipitation scores
    prec_query = session.query(Measurement.date, Measurement.prcp).filter(
        Measurement.date >= query_date).all()
    session.close()
    # Convert list of tuples into normal list
    last_year = list(np.ravel(prec_query))
    return jsonify(last_year)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    """Return a list of all stations"""
    # Query all stations
    station_query = session.query(Station.station, Station.name).all()
    session.close()
    # Convert list of tuples into normal list
    stations = list(np.ravel(station_query))
    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    # Perform a query to retrieve the data and precipitation scores
    tobs_query = session.query(Measurement.station, Measurement.date, Measurement.tobs).filter(
        Measurement.date >= query_date).filter(Measurement.station == 'USC00519281').all()
    session.close()
   # Convert list of tuples into normal list
    active_station = list(np.ravel(tobs_query))
    return jsonify(active_station)


@app.route("/api/v1.0/<start>")
def temp_start(start):
    session = Session(engine)
    # Perform a query to calculate min, avg and max temp from start date
    start_query = session.query(func.min(Measurement.tobs), func.avg(
        Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    session.close()
    # Convert list of tuples into normal list
    temps = list(np.ravel(start_query))
    return jsonify(temps)


@app.route("/api/v1.0/<start>/<end>")
def temp_start_end(start, end):
    session = Session(engine)
    # Perform a query to calculate min, avg and max temp from date range
    start_end_query = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(
        Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()
    # Convert list of tuples into normal list
    temps = list(np.ravel(start_end_query))
    return jsonify(temps)


if __name__ == '__main__':
    app.run(debug=True)
