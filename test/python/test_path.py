import os

print(f"현재 작업 디렉토리:   {os.getcwd()}")
# 현재 작업 디렉토리: E:\home

print(f"현재 파일의 디렉토리: {os.path.dirname(__file__)}")
# 현재 파일의 디렉토리: e:\home\study\test\python

print(f"현재 파일의 경로:     {__file__}")
# 현재 파일의 경로:     e:\home\study\test\python\test_path.py

