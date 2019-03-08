import mysql.connector as mysql
from ipwhois import IPWhois
import csv

class Sender:
	def __init__(self, IP):
		super(Sender, self).__init__()
		self.IP = IP
		self.obj = IPWhois(self.IP)
		self.info = self.obj.lookup_whois()
	def AbuseEmails(self):
		if self.info['nets'][0]['emails']:
			return self.info['nets'][0]['emails']
		else:
			return 'N/A'

	def Description(self):
		if self.info['nets'][0]['description']:
			return self.info['nets'][0]['description']
		else:
			return 'N/A'

	def CType(self):
		self.comp_type = 'N/A'
		return self.comp_type

	def Network(self):
		if self.info['asn_cidr']:
			self.network = self.info['asn_cidr']
			return self.network
		else:
			return 'N/A'
	def Customer(self):
		self.is_customer = 'N/A'
		return self.is_customer
	def External(self):
		self.is_external = 'N/A'
		return self.is_external
	def Country(self):
		self.country = self.info['asn_country_code']		
		return self.country
	def Name(self):
		self.comp_name = self.info['asn_description']
		return self.comp_name
	def Query(self):
		self.query = """INSERT INTO senders (SenderIP, Network, CompanyName, CompanyType, Country, IsTeliaCustomer, IsExternal, AbuseEmails) VALUES ("{ip}","{network}","{name}","{ctype}","{country}","{cust}","{ext}","{abuse_emails}")""".format(ip=self.IP, network=self.Network(), name=self.Name(), ctype=self.CType(), country=self.Country(),cust=self.Customer(), ext=self.External(), abuse_emails=self.AbuseEmails())
		return self.query

db = mysql.connect(
	host = 'localhost',
	user= 'root',
	password= 'smalsu',
	database= 'InfoSenders'
)
# print(db)
def CreateDBTables():
	SendersDB = cursor.execute("CREATE DATABASE InfoSenders")
	# cursor.execute('DROP TABLE senders')
	cursor.execute('CREATE TABLE senders (SenderIP VARCHAR(16), Network VARCHAR(22), CompanyName VARCHAR(255), CompanyType VARCHAR(255), Country VARCHAR(4), IsTeliaCustomer VARCHAR(3), IsExternal VARCHAR(3), AbuseEmails VARCHAR(255), UNIQUE (SenderIP))')

def IfExists(cursor, IP_string):
	query = """SELECT EXISTS(SELECT * FROM senders WHERE SenderIP='{IP}')""".format(IP=IP_string)
	cursor.execute(query)
	exists = cursor.fetchone()[0]
	return exists

def RunOnIP(IP_string):
	cursor = db.cursor(buffered=True)
	exists = False
	exists = IfExists(cursor, IP_string)
	print(exists)
	PutInDB(cursor, exists, IP_string)

def PutInDB(cursor, exists, IP_string):
	if exists == 0:
		try:
			 sender_single = Sender(IP_string)
			 cursor.execute(sender_single.Query())
			 db.commit()
		except:
			 print("An exception occured")
	else:
       	 	 print("IP already exists")

def RunOnFile(file_name):
	cursor = db.cursor(buffered=True)
	with open(file_name, newline='') as csvfile:
		list_reader = csv.reader(csvfile, delimiter=',')
		i = 0
		for row in list_reader:
			IP_string = str(row[0])
			i += 1
			print(IP_string, ' ', i)
			exists = IfExists(cursor, IP_string)
			PutInDB(cursor, exists, IP_string)
		# cursor.execute(sender_single.Query())
		# print(sender_single.Network())
		# # print(sender_single.info)
		# print(sender_single.Query())
	cursor.execute('SELECT 	* FROM senders')
	# print(cursor.fetchall())
