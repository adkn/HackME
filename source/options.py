import sqlite3
import hashlib

class Options:
	def __init__(self, dbName = "hackme.db", defOpt = "{\"lang\": \"EN\", \"tcol\": \"white\"}"):
		self.dbName = dbName
		self.conn = sqlite3.connect(dbName)
		self.defOpt = eval(defOpt)
		self.uID = 0

		sql = "CREATE TABLE IF NOT EXISTS users\
		(\
			_id INTEGER PRIMARY KEY AUTOINCREMENT,\
			userName STRING,\
			passWord STRING\
		);"
		self.conn.execute(sql)

		sql = "CREATE TABLE IF NOT EXISTS options\
		(\
			_id INTEGER PRIMARY KEY AUTOINCREMENT,\
			uID INTEGER,\
			opt STRING\
		);"
		self.conn.execute(sql)
		self.conn.commit()

	def __del__(self):
		self.conn.commit()
		self.conn.close()

	def md5(self, val):
		return hashlib.md5(val).hexdigest()
	
	def checkSession(self, userName, passWord):
		c = self.conn.cursor()
		sql = "SELECT count(_id) FROM users"
		c.execute(sql)

		if c.fetchone()[0] == 0:
			self.createSession(userName, passWord)
		
		sql = "SELECT _id FROM users WHERE userName = ? AND passWord = ?"
		c.execute(sql, (userName, self.md5(passWord)))

		found = False
		row = c.fetchone()
		if row:
			found = True
			self.uID = row[0]
		
		c.close()
		return found

	def getOpts(self):
		c = self.conn.cursor()
		sql = "SELECT opt FROM options WHERE uID = ?"
		c.execute(sql, (self.uID,))

		opt = self.defOpt
		row = c.fetchone()
		if row:
			opt = eval(row[0])
		
		c.close()
		return opt

	def createSession(self, userName, passWord):
		c = self.conn.cursor()
		sql = "SELECT _id FROM users WHERE userName = ?"
		c.execute(sql, (userName,))

		if c.fetchone():
			c.close()
			return False
		
		sql = "INSERT INTO users (userName, passWord) VALUES (?, ?)"
		c.execute(sql, (userName, self.md5(passWord)))

		sql = "SELECT _id FROM users WHERE userName = ? AND passWord = ?"
		c.execute(sql, (userName, self.md5(passWord)))
		
		self.uID = c.fetchone()[0]

		sql = "INSERT INTO options (uID, opt) VALUES (?, ?)"
		c.execute(sql, (self.uID, str(self.defOpt)))

		c.close()
		self.conn.commit()
		return True

	def setOpts(self, **kwargs):
		opt = self.getOpts()
		for key in kwargs:
			opt[key] = kwargs[key]

		sql = "UPDATE options SET opt = ? WHERE uID = ?"
		c = self.conn.cursor()
		c.execute(sql, (str(opt), self.uID))

		c.close()
		self.conn.commit()

