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


# User_id가 344인 테스트 데이터를 삭제한다.
response = supabase.table("User") \
    .delete() \
    .eq("User_id", 344) \
    .execute()


# 삭제된 데이터를 출력한다.
print(response.data)