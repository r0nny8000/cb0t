"""Kraken API client configuration."""
import os
from kraken.spot import User, Trade

user = User(key=os.getenv("KRAKENAPIKEY"), secret=os.getenv("KRAKENAPISECRET"))
trade = Trade(key=os.getenv("KRAKENAPIKEY"), secret=os.getenv("KRAKENAPISECRET"))
