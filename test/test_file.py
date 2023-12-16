import os

# 현재 작업디렉토리
print(f"getcwd : {os.getcwd()}")

# 열려있는 파일의 디렉토리 + 파일명
print(f"__file__ : {__file__}")

# 현재 파일의 절대경로 + 파일명
print(f"abspath : {os.path.abspath(__file__)}")

# 현재 파일의 디렉토리
print(f"dirname : {os.path.dirname(__file__)}")

# 현재 파일의 상대경로
print(f"realpath : {os.path.realpath('monpass_ticket.py')}")
