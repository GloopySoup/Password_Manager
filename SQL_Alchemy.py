from sqlalchemy import Table,Column,    MetaData,Text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import select
import asyncio

meta = MetaData()

users_table = Table(
    'users',
    meta,
    Column('username',Text,),
    Column('password',Text,),
)


async def async_main():
    engine = create_async_engine("mysql+aiomysql://user:password.@Host:Port/databaseName")

    async with engine.begin() as conn:
        await conn.run_sync(meta.create_all)
        choice = input("Would you like to add  or delete an account or get a new password(Add/Get/Delete): ").upper()

        if choice == "ADD":
            print("---ADDING ACCOUNT---")
            await conn.execute(users_table.insert(),[{'username':input("Enter a username: "),'password':input("Enter a password: ")}])
            print("Account added")
        elif choice == "GET":
            print("---GETTING PASSWORD---")
            result = await conn.execute(select(users_table.c.password).where(users_table.c.username == input("Enter your username: ")))
            print(f"The password for your account is: {str(result.all()).strip("[(',)]")}")
        else:
            print("---DELETING ACCOUNT---")
            await conn.execute(users_table.delete().where(users_table.c.username == input("Enter the username of account to be deleted: "), users_table.c.password == input("Enter the password of account to be deleted: ")))
            print("Account deleted")
    await engine.dispose()
        

asyncio.run(async_main())