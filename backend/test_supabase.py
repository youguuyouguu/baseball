import os

from dotenv import load_dotenv
from supabase import create_client


# .env 파일의 환경변수를 불러온다.
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


# Supabase 클라이언트를 생성한다.
supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# 테스트 bigint ID를 지정해 삭제한다.
test_user_id = int(os.environ["TEST_USER_ID"])
response = supabase.table("User") \
    .delete() \
    .eq("User_id", test_user_id) \
    .execute()


# 삭제된 데이터를 출력한다.
print(response.data)