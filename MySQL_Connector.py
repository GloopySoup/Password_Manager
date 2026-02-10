import mysql.connector
from cryptography.fernet import Fernet
db = mysql.connector.connect(
host = "hostname",
user="username",
password="password",
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
        mycursor.execute("INSERT INTO password (username, password) VALUES(%s,%s)",(username, encrypted_password))
        db.commit()
        print("Account successfully added")

def get_password(username):
    if check(username):
        mycursor.execute("SELECT Password FROM pythonpasswordmanager.password WHERE username =%s",(username,))
        passw = mycursor.fetchone()[0]
        passw = str(fernet.decrypt(passw))
        passw = passw.strip("b'")
        print(f"The password for your account is: {passw}")
    else:
        print("Account doesn't exist")

def delete_account(username, password):
    if check(username):
        mycursor.execute("SELECT Password FROM pythonpasswordmanager.password WHERE username =%s",(username,))
        encrpass = mycursor.fetchone()[0]
        encrpass = str(fernet.decrypt(encrpass))
        encrpass = encrpass.strip("b'")
        if password == encrpass:
            mycursor.execute("DELETE FROM pythonpasswordmanager.password WHERE username =%s",(username,))
            db.commit()
            print("Account successfully deleted")

choice = input("Would you like to add  or delete an account or get a new password(Add/Get/Delete): ").upper()

if choice == "ADD":
    print("---ADDING ACCOUNT---")
    add_password(input("Enter a username: "), input("Enter a password: "))
elif choice == "GET":
    print("---GETTING PASSWORD---")
    get_password(input("Enter your username: "))
else:
    delete_account(input("Enter the username of the account to be deleted: "), input("Enter your password for this account: "))

