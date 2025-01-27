import os
import signal
import sys
import telebot
from telebot import types
from dotenv import load_dotenv
from time import sleep
from database import *
from server import get_server, get_players
from lang import *