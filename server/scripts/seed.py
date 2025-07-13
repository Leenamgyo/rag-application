# # scripts/seed.py

# import sys
# import os

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from src.database import SessionLocal
# from src.models import User

# def seed_data():
#     db = SessionLocal()
#     try:
#         # 초기 관리자 계정이 있는지 확인
#         if db.query(User).filter(User.username == "admin").first():
#             print("관리자 계정이 이미 존재합니다.")
#         else:
#             print("초기 관리자 계정을 생성합니다...")
#             # 실제로는 비밀번호 해싱 함수를 사용해야 합니다.
#             hashed_password = "some_hashed_password"
#             admin_user = User(
#                 username="admin",
#                 email="admin@example.com",
#                 hashed_password=hashed_password
#             )
#             db.add(admin_user)
#             db.commit()
#             print("관리자 계정 생성 완료.")
#     finally:
#         db.close()

# if __name__ == "__main__":
#     seed_data()