import os

print(f"현재   작업 디렉토리: {os.getcwd()}")
print(f"현재 파일의 디렉토리: {os.path.dirname(__file__)}")
print(f"현재 파일의     경로: {__file__}")
print(f"해당 파일의 절대경로: {os.path.abspath('py_selenium_find.py')}")
print(f"해당 파일의 상대경로: {os.path.realpath('py_selenium_find.py')}")


# 현재   작업 디렉토리: /home/ubuntu
# 현재 파일의 디렉토리: /home/ubuntu/study/test
# 현재 파일의     경로: /home/ubuntu/study/test/test_path.py
# 해당 파일의 절대경로: /home/ubuntu/py_selenium_find.py
# 해당 파일의 상대경로: /home/ubuntu/py_selenium_find.py