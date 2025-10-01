import os

# 현재 작업 디렉토리
getcwd = os.getcwd()
# print(getcwd)
# /home/ubuntu/study/test

# 현재 파일의 디렉토리
dirname_file = os.path.dirname(__file__)
# print(dirname_file)
# /home/ubuntu/study/test

# 경로 합치기
log_dir = os.path.join(os.path.dirname(__file__), "log")
# print(log_dir)
# /home/ubuntu/study/test/log