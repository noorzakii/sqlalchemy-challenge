# Import the dependencies.
import numpy as np
import datetime as dt
import os 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///C:/Users/noorzaki/Desktop/sqlalchemy challenge module 10 /sqlalchemy-challenge/Surfs Up/Resources/hawaii.sqlite")
#engine = create_engine("sqlite:///C:/Surfs Up/Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
stations = Base.classes.station

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
def welcome():
    """List all available API routes"""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f".api.v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/yyyy-m-d/yyyy-m-d"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of all the precipitation from last year"""
    precip_data = session.query(measurement.date, measurement.precip).\
    filter(measurement.date >= dt.date(2016,8,23)).all()
    #dictionary conversion
    all_precip_data = []
    for date, precip in precip_data:
        precip_dict = {}
        precip_dict["Date"] = date
        precip_dict["Precipitation"] = precip
        all_precip_data.append(precip_dict)

    return jsonify(all_precip_data)

@app.route("/api/v1.0/stations")
def stations():
    """returning a list of the active stations"""
    station_data = session.query(stations.station).all()
    all_stations = list(np.ravel(station_data))
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def temperature():
    """return dates and temperature of the stations from the previous year of the data"""
    active_stations_temperature = session.query(measurement.date, measurement.tobs).filter(measurement.station == "USC00519281").filter(measurement.date >= dt.date(2016,8,23)).all()
    all_active_data = []
    for sdate, stemp in active_stations_temperature:
        active_temp_dictionary = {}
        active_temp_dictionary["Date"] = sdate
        active_temp_dictionary["Temperature"] = stemp
        all_active_data.append(active_temp_dictionary)

    return jsonify(all_active_data)    

@app.route("/api/v1.0/<start>")
def temp_data(start):
    """find min, max and avg temperature with matching dates of the path"""
    start_date = dt.datetime.strptime(start, "%Y-%m-%d")
    temperature_measure = session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).\
        filter(measurement.date >= start_date).all()
    temperature_measure_data = []
    for Tdate, TMIN, TMAX, TAVG in temperature_measure:
        temperature_measures_dict = {}
        temperature_measures_dict["Date"] = Tdate
        temperature_measures_dict["Min_temp"] = TMIN
        temperature_measures_dict["Max_temp"] = TMAX
        temperature_measures_dict["Avg_temp"] = TAVG
        temperature_measures_data.append(temperature_measures_dict)
    return jsonify(temperature_measure_data)

@app.route("/api/v1.0/<strt>/<end>")
def temperature_between(strt,end):
    """find min, max, avg temperature with matching dates to path"""
    start_date2 = dt.datetime.strp.time(strt, "%Y-%m-%d")
    end_date2 = dt.datetime.strp.time(end, "%Y-%m-%d")
    temperature_between = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
        filter((measurement.date >= start_date2)| (measurement.date <= end_date2)).all()
    
    temperature_between_data = []
    for bdate, bmin, bmax, bavg in temperature_between:
        temperature_between_dict = {}
        temperature_between_dict["Date"] =bdate
        temperature_between_dict["Min_Temp"] = bmin
        temperature_between_dict["Max_Temp"] = bmax
        temperature_between_dict["Avg_Temp"] = bavg
        temperature_between_data.append(temperature_between_dict)
    return jsonify(temperature_between_data)
session.close()

if __name__ == '__main__':
    app.run(debug=True)







