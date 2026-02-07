import mysql.connector
db = mysql.connector.connect(
host = "localhost",
user="root",
password="Red47red.",
database = "pythonpasswordmanager")
mycursor = db.cursor()

def check(value):
    mycursor.execute("SELECT EXISTS(SELECT * FROM password WHERE username = %s)",(value,))
    return mycursor.fetchone() == (1,)

def add_password(username, password):
    if  check(username):
        print("Account with that username already exists")
    else:
        mycursor.execute("INSERT INTO password (username, password) VALUES(%s,%s)",(username, password))
        db.commit()


def get_password(username):
    if check(username):
        mycursor.execute("SELECT Password FROM pythonpasswordmanager.password WHERE username =%s",(username,))
        passw = mycursor.fetchone()[0]
        print(f"The password for your account is: {passw}")
    else:
        print("Account doesn't exist")

if input("Would you like to add a new account or get a new password(Add/Get): ").upper() == "ADD":
    print("---ADDING ACCOUNT---")
    add_password(input("Enter a username: "), input("Enter a password: "))
else:
    print("---GETTING PASSWORD---")
    get_password(input("Enter your username: "))

