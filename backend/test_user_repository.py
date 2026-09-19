import os
from uuid import uuid4

from dotenv import load_dotenv
from supabase import create_client

from repository.User_repository import UserRepository


# .env 파일의 환경변수를 불러온다.
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


# Supabase 클라이언트를 생성한다.
supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# UserRepository 객체를 생성한다.
user_repository = UserRepository(supabase)


# --------------------------------------------------
# CREATE
# --------------------------------------------------

test_user_id = uuid4()
user = user_repository.create_user(
    user_id=test_user_id,
    email="repository@test.com",
    nickname="Repository테스트"
)

print("CREATE")
print(user)


# --------------------------------------------------
# READ
# --------------------------------------------------

user = user_repository.get_user(test_user_id)

print("\nREAD")
print(user)


# --------------------------------------------------
# READ ALL
# --------------------------------------------------

users = user_repository.get_users()

print("\nREAD ALL")
print(users)


# --------------------------------------------------
# UPDATE
# --------------------------------------------------

user = user_repository.update_user(
    user_id=test_user_id,
    nickname="Repository수정테스트"
)

print("\nUPDATE")
print(user)


# --------------------------------------------------
# DELETE
# --------------------------------------------------

user = user_repository.delete_user(test_user_id)

print("\nDELETE")
print(user)