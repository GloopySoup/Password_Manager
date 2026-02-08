import mysql.connector
from cryptography.fernet import Fernet
db = mysql.connector.connect(
host = "localhost",
user="root",
password="Red47red.",
database = "pythonpasswordmanager")
mycursor = db.cursor()
key = b'P4IycxnVMm9JU_TMfC7ic20xIL1leeHQ3jq3nIgIceU='
fernet = Fernet(key)
encrypted_password = ""

def check(value):
    mycursor.execute("SELECT EXISTS(SELECT * FROM password WHERE username = %s)",(value,))
    return mycursor.fetchone() == (1,)

def add_password(username, password):
    if  check(username):
        print("Account with that username already exists")
    else:
        encrypted_password = fernet.encrypt(password.encode())
        print(encrypted_password)
        mycursor.execute("INSERT INTO password (username, password) VALUES(%s,%s)",(username, encrypted_password))
        db.commit()


def get_password(username):
    if check(username):
        mycursor.execute("SELECT Password FROM pythonpasswordmanager.password WHERE username =%s",(username,))
        passw = mycursor.fetchone()[0]
        passw = str(fernet.decrypt(passw))
        passw = passw.strip("b'")
        print(f"The password for your account is: {passw}")
    else:
        print("Account doesn't exist")

if input("Would you like to add a new account or get a new password(Add/Get): ").upper() == "ADD":
    print("---ADDING ACCOUNT---")
    add_password(input("Enter a username: "), input("Enter a password: "))
else:
    print("---GETTING PASSWORD---")
    get_password(input("Enter your username: "))

