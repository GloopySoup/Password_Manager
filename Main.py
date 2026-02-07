import mysql.connector
db = mysql.connector.connect(
host = "localhost",
user="root",
password="Red47red.",
database = "pythonpasswordmanager")
mycursor = db.cursor()

def check(value):
    check_query = f"SELECT EXISTS(SELECT * FROM password WHERE username = '{value}')"
    return mycursor.execute(check_query)

def add_password(username, password):
        mycursor.execute("INSERT INTO password (username, password) VALUES(%s,%s)",(username, password))
        db.commit()


def get_password(username):
        mycursor.execute("SELECT Password FROM pythonpasswordmanager.password WHERE username =%s",(username,))
        print(f"The password for your account is:{mycursor.fetchone()}")


if input("Would you like to add a new account or get a new password(Add/Get): ").upper() == "ADD":
    print("---ADDING ACCOUNT---")
    add_password(input("Enter a username: "), input("Enter a password: "))
else:
    print("---GETTING PASSWORD---")
    get_password(input("Enter your username: "))

