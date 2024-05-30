import argparse
import asyncio

from backend.api.model import User
from backend.api.service.db_service import AsyncSessionFactory
from backend.api.util import get_password_hash

async def create_admin(username: str, password: str) -> None:
    """
    CLI function to generate new admin if needed

    :param username : admin username
    :type username : str
    :param password : admin password
    :type password : str
    :returns : Admin user {user.username} created | Exception
    :rtype : None
    """
    async with AsyncSessionFactory() as session:
        hashed_password = await get_password_hash(password)
        user = await User.create(
            session, username=username, password=hashed_password, is_admin=1
        )


def main():
    parser = argparse.ArgumentParser(description='Create an admin user')
    parser.add_argument('--username', required=True, help='Username for the admin user')
    parser.add_argument('--password', required=True, help='Password for the admin user')

    args = parser.parse_args()

    username = args.username
    password = args.password

    try:
        asyncio.run(create_admin(username, password))
        print(f"Admin {username} created successfully.")
    except Exception as e:
        print(f"Error creating admin user: {e}")


if __name__ == "__main__":
    main()
