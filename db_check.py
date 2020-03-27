import sqlite3

class Registering:
	def __init__(self, username, password ):
		self.username=username
		self.password=password

	def create(self):
		conn = sqlite3.connect('money_tracker.db')
		print("Database opened successfully")
		c=conn.cursor()

		c.execute('''CREATE TABLE users(
			user_id TEXT PRIMARY KEY ,
			user_password TEXT NOT NULL
			);''')
		print("Table created successfully")
		conn.commit()
		conn.close()
		print("Database closed successfully")

	def check(self):
		conn = sqlite3.connect('money_tracker.db')
		print("Database opened successfully")
		c=conn.cursor()
		print("Checking if username taken or not .... ")
		c.execute("SELECT user_id FROM users WHERE user_id = (?)" , (self.username,))
		aux=c.fetchone()
		conn.commit()
		conn.close()
		print("Database closed successfully")
		return (aux)

	def add(self):
		conn= sqlite3.connect('money_tracker.db')
		print("Database opened successfully")
		c=conn.cursor()
		print("Adding username and password to DB ....")
		c.execute("INSERT INTO users VALUES (:user_id, :user_password, :user_cash)",{'user_id' :self.username , 'user_password' : self.password, 'user_cash' : 0.0})
		print("Username and password added successfully.")
		conn.commit()
		conn.close()
		print("Database closed successfully")

class Logging:
	def __init__(self, username, password):
		self.username=username
		self.password=password


	def exist(self):
		conn = sqlite3.connect('money_tracker.db')
		print("Database opened successfully")
		c=conn.cursor()
		print("Checking if username exists or not .... ")
		c.execute("SELECT user_id FROM users WHERE user_id = (?)" , (self.username,))
		aux=c.fetchone()
		conn.commit()
		conn.close()
		print("Database closed successfully")
		return (aux)

	def passverif(self):
		conn = sqlite3.connect('money_tracker.db')
		print("Database opened successfully")
		c=conn.cursor()
		print("Verifying if password is correct or not....")
		c.execute("SELECT user_password FROM users WHERE user_id = (?)", (self.username,))
		aux=c.fetchone()[0]    #USED [0] because fetchone returs a tuple (password,)
		conn.commit()
		conn.close()
		print("Database closed succefully")
		return aux==self.password

class Account_db:
	def __init__(self, username):
		self.username=username

	def create_expense_table(self):
		print("Creating Expense table..")
		conn = sqlite3.connect('money_tracker.db')
		print("Database opened successfully")
		c=conn.cursor()

		c.execute('''CREATE TABLE expenses(
			EXPENSE_ID TEXT PRIMARY KEY ,
			EXPENSE_VALUE TEXT NOT NULL ,
			EXPENSE_CATEGORY TEXT NOT NULL ,
			EXPENSE_DATE TEXT NOT NULL,
			EXPENSE_DESCRIPTION TEXT
			);''')
		print("Expenses table created successfully")
		conn.commit()
		conn.close()
		print("Database closed successfully")

	#def add_column_users(self):
	def add_expense(self, value, category, description, date):
		print("Adding an expense..")
		conn=sqlite3.connect('money_tracker.db')
		print("Database opened successfully")
		c=conn.cursor()
		categories_numbers={"Food":'1', "Transport":'2', "Education":'3', "Phone/Internet bill":'4', "Clothes":'5', "Entertainment/Sport":'6', \
 			"Gifts":'7', "Going out":'8', "Other":'9'}

		print('category nummber ={}'.format(categories_numbers[category]))
		print("ID = {}".format(categories_numbers[category]+date[:6]))

		expense_id_v2=categories_numbers[category]+date
		c.execute("""INSERT INTO expenses VALUES (:EXPENSE_ID, :EXPENSE_VALUE, :EXPENSE_CATEGORY,
			:EXPENSE_DATE, :EXPENSE_DESCRIPTION)""",{'EXPENSE_ID':(expense_id_v2), 'EXPENSE_VALUE':value, \
				'EXPENSE_CATEGORY':category, 'EXPENSE_DATE':date[:6], 'EXPENSE_DESCRIPTION':description})
		c.execute("INSERT INTO users_expenses VALUES (:user_id, :expense_id)", {'user_id':(self.username), 'EXPENSE_ID':(expense_id_v2)})
		print("Expense added successfully")
		conn.commit()
		conn.close()
		print("Database closed successfully")
	def add_expense_desc(self):
		print("ADDING EXPENSES DESCIRPTION")
		conn=sqlite3.connect('money_tracker.db')
		c=conn.cursor()
		c.execute("ALTER TABLE expenses ADD COLUMN EXPENSE_DESCRIPTION TEXT ")
		print("COLUMN ADDDDED")
		conn.commit()
		conn.close()
	def total_number_expen(self):
		print("Calculating total number of expenses:")
		conn=sqlite3.connect('money_tracker.db')
		c=conn.cursor()
		c.execute("SELECT * FROM expenses")
		n=len(c.fetchall())
		print("TOTAL NUMBER OF EXPENSE = {}".format(n))
		conn.commit()
		conn.close()
		return n

	def get_cash(self):
		print("Getting cash's value for this user : {}".format(self.username))
		conn=sqlite3.connect('money_tracker.db')
		c=conn.cursor()
		aux=c.execute("SELECT user_cash FROM users WHERE user_id=(?)", (self.username, ))
		conn.commit()
		conn.close()
		return aux

	def add_cash(self, value):
		print("Adding cash value!")
		conn=sqlite3.connect('money_tracker.db')
		c=conn.cursor()
		c.execute("UPDATE users SET user_cash = (?) WHERE user_id = (?)", (value, self.username))
		conn.commit()
		conn.close()
