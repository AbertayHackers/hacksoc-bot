#!/usr/bin/python3
import pymysql, sys
from libs.loadconf import secrets

class Conn():
	def __init__(self):
		try:
			self.dbh = pymysql.connect(
                host=secrets["mysqlLoc"], 
                user=secrets["mysqlUsername"], 
                password=secrets["mysqlPass"], 
                db=secrets["mysqlDB"]
            )
		except:
			print ("Failed to connect to the database")
			sys.exit()
		self.dictcurs = self.dbh.cursor(pymysql.cursors.DictCursor)
		self.curs = self.dbh.cursor()

	def __del__(self):
		self.dbh.close()
