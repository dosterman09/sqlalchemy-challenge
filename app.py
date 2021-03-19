#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('matplotlib', 'inline')
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt


# In[2]:


import numpy as np
import pandas as pd
import datetime as dt
from datetime import timedelta, datetime


# # Reflect Tables into SQLAlchemy ORM

# In[3]:


# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


# In[4]:


# create engine to hawaii.sqlite
engine = create_engine("sqlite:///resources/hawaii.sqlite")


# In[5]:


# reflect an existing database into a new model
base = automap_base()

# reflect the tables
base.prepare(engine, reflect=True)


# In[6]:


# View all of the classes that automap found
base.classes.keys() 


# In[7]:


# Save references to each table
Measurement = base.classes.measurement
Station = base.classes.station


# In[8]:


# Create our session (link) from Python to the DB
session = Session(engine)


# # Exploratory Precipitation Analysis

# In[9]:


# Find the most recent date in the data set.
session.query(func.count(Measurement.date)).all()


# In[18]:


latest_date = session.query(func.max(Measurement.date)).first()
latest_date[0]
print(f" Latest Date: {latest_date[0]}")

recentdate = session.query(Measurement.date).order_by(Measurement.date).first()
print(f" Most Recent Date: {recentdate[0]}")


# In[51]:


#MY MATPLOTLIB SKILLS NEED REFINED!!

# Design a query to retrieve the last 12 months of precipitation data and plot the results. 
# Starting from the most recent data point in the database. 
recentdate = dt.datetime.strptime(recentdate[0], '%Y-%M-%d')

# Calculate the date one year from the last date in data set.
querydate = dt.datetime(recentdate.year -1, recentdate.month, recentdate.day)

# Perform a query to retrieve the data and precipitation scores
sel = [Measurement.date, Measurement.prcp]
query_results - session.query(*sel).filter(Measurement.date >= querydate).all()

# Save the query results as a Pandas DataFrame and set the index to the date column
precipitation = pd.DataFrame(queryresult, columns=['Date', 'Precipitation'])

# Sort the dataframe by date
precipitation = precipitation.dropna(how='any')

# Use Pandas Plotting with Matplotlib to plot the data
precipitation = precipitation.sort_values(['Date'], ascending=True)
precipitation = precipitation.set_index('Date')
precipitation.head()


# # Exploratory Station Analysis

# In[52]:


# Design a query to calculate the total number stations in the dataset
session.query(Station.id).count()


# In[53]:


# Design a query to find the most active stations (i.e. what stations have the most rows?)
# List the stations and the counts in descending order.
active_stations = session.query(Measurement.station, func.count(Measurement.id)).    group_by(Measurement.station).    order_by(func.count(Measurement.id).desc()).all()
active_stations


# In[61]:


#most active station
max_obs = (active_stations[0])[0]
max_obs


# In[58]:


# Choose the station with the highest number of temperature observations.
# Query the last 12 months of temperature observation data for this station and plot the results as a histogram
sel = [func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)]
mostactivestationdata = session.query(*sel).    group_by(Measurement.station).    order_by(func.count(Measurement.id).desc()).first()
mostactivestationdata


# In[62]:


#Putting calculated temperatures in order
lowest_temp = session.query(func.min(Measurement.tobs)).filter(Measurement.station==max_obs).scalar()
print(f'The lowest temperature for Station ID USC00519281 is {lowest_temp}.')

highest_temp = session.query(func.max(Measurement.tobs)).filter(Measurement.station==max_obs).scalar()
print(f'The highest temperature for Station ID USC00519281 is {highest_temp}.')

avg_temp = session.query(func.avg(Measurement.tobs)).filter(Measurement.station==max_obs).scalar()
print(f'The average temperature for Station ID USC00519281 is {avg_temp}.')


# In[ ]:


#MY MATPLOTLIB SKILLS NEED REFINED!!

# Using the most active station id
# Query the last 12 months of temperature observation data for this station and plot the results as a histogram


# # Close session

# In[ ]:


# Close Session
session.close()


# In[ ]:




