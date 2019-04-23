import sys



#import pymysql
import psycopg2



class MyDBTest():



	def __init__(self):

		try:
			self.con = psycopg2.connect(database="patentdb", user="admin", password="admin", host="140.116.96.199", port="5432")

			#self.con = pymysql.connect("192.168.46.1","admin","admin","amazon_review_db" )
			#self.con = pymysql.connect("140.116.96.199","admin","admin","amazon_review_db" )

			self.cur = self.con.cursor()
			print ("Opened database successfully")
		#self.show_version()

		except:

			print ("Connection Error")

			sys.exit(1)
	def closeDB(self):
		self.cur.close()
		self.con.close()
	def selectData(self, sql):
		try:
			print ("sql: " + sql)
			self.cur.execute(sql)
			results = self.cur.fetchall()
			return results
		except Exception as e:
			print (e)
			pass


	def show_version(self):

		self.cur.execute("SELECT VERSION()")

		print ("Database version : %s " % self.cur.fetchone())



	def test1(self):

        # Do something with self.con or self.cur

		pass



	def test2(self, sql):

		self.cur.execute(sql)

		print('test2 function: '+ sql) 

		pass

	def test3(self):

		self.con.commit()

		print('#3 submit to db: ') 

		pass

	def test4(self, insert, data):

		self.cur.execute(insert,data)

		self.con.commit()

		print('#3 submit to db: ') 

		pass

	def insertData(self, insert, data):

		try:
			print (insert)
			self.cur.execute(insert,data)
			print('# insert data: ') 
			self.con.commit()
			print('# submit to db: ') 
			pass
		except Exception as e:
			print (e)
			pass
	def updateData(self, update, data):
		try:
			print ("sql: " + update)
			self.cur.execute(update,data)
			self.con.commit()
			print('#3 updateData to db: ') 
			pass
		except:
			pass

#db = MyDBTest()
#db.show_version()
#selectSql = "SELECT page, titles FROM beats_raw"
#results = db.selectData(selectSql)
#print results