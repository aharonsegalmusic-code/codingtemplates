"""
pip install fastapi
pip install pydantic
pip install 'pydantic[email]'
pip install SQLAlchemy
pip install sqlmodel
pip install uvicorn
pip install requests
pip install python-dotenv
pip install numpy pandas
pip install matplotlib
pip install seaborn
pip install termseparator
pip install pymongo
pip install confluent-kafka
pip install redis
pip install elasticsearch
pip install streamlit
pip install docker
pip install multipart
"""

# ---------------------------------------
#  Standard Library (built into Python)
# ---------------------------------------

import os
import sys
import json
import datetime
import pathlib
import logging

# Extra commonly used imports
from pathlib import Path                # Object-oriented filesystem paths
from logging import getLogger           # Quick logger access
from datetime import timedelta, date     # Useful time objects


# ---------------------------------------
#  Databases
# ---------------------------------------

import sqlite3
import sqlalchemy
import sqlmodel
from pymongo import MongoClient
from elasticsearch import Elasticsearch


# Common SQLAlchemy imports
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    select,
)

from sqlalchemy.orm import (
    Session,
    declarative_base,
    relationship,
)

# SQLModel essentials
from sqlmodel import (
    SQLModel,
    Field,
    Session as SQLSession,
    create_engine,
)


# ---------------------------------------
#  Caching
# ---------------------------------------

import redis


# ---------------------------------------
#  Messaging & Streaming
# ---------------------------------------

from confluent_kafka import Producer, Consumer, KafkaError


# ---------------------------------------
#  Web & APIs
# ---------------------------------------

import requests
from fastapi import FastAPI

# Common requests helpers
from requests import Session as RequestSession

# Typical FastAPI imports
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

# ---------------------------------------
#  Pydantic & Validation
# ---------------------------------------

from pydantic import BaseModel, Field, EmailStr, HttpUrl, ValidationError
from typing import Optional, List, Dict
from datetime import datetime

# ---------------------------------------
#  Environment & Configuration
# ---------------------------------------

from dotenv import load_dotenv
import configparser

# Typical configparser helpers
from configparser import ConfigParser

# ---------------------------------------
#  Data Analysis & Numerical Computing
# ---------------------------------------
import numpy as np        # Powerful numerical computations
import pandas as pd       # Data manipulation and analysis
import matplotlib.pyplot as plt # Plotting and visualization 
import seaborn as sns     # Statistical data visualization

# ---------------------------------------
#  UI & Dashboards
# ---------------------------------------

import streamlit as st    # Rapid web app / dashboard builder


# ---------------------------------------
#  Containers & Orchestration
# ---------------------------------------

import docker             # Docker Engine SDK for Python
from docker.types import Mount


# ---------------------------------------
#  Utilities
# ---------------------------------------

import functools
import itertools
import random
import termseparator as ts       # terminal separator for clear output

# Convenient direct imports
from functools import lru_cache, partial
from itertools import groupby, chain
from random import randint, choice