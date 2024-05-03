import time

url = "https://jsonplaceholder.typicode.com/posts/"
n = 1001

# urllib3
import urllib3
urllib3
start = time.time()
http = urllib3.PoolManager()
for i in range(1,n):
    # url =curl + "/posts/" + str(i)
    response = http.request('GET', url + str(i))
    result = response.json()['title']
    print(result)
print(f"-> urllib3 : {time.time()-start}\n")

# # request
# import requests
# start = time.time()
# for i in range(1,n):
#     response = requests.get(url + str(i))
#     result = response.json()['title']
#     # print(result)
# print(f"-> request : {time.time()-start}\n")

# # urllib.request
# import urllib.request
# start = time.time()
# for i in range(1,n):
#     response = urllib.request.urlopen(url + str(i)).read()
#     result = eval(response.decode('utf-8'))['title']
#     # print(result)
# print(f"-> urllib.request : {time.time()-start}\n")




# url = "jsonplaceholder.typicode.com"

# # http.client
# import http.client
# start = time.time()
# for i in range(1,n):
#     conn = http.client.HTTPSConnection(url)
#     conn.request("GET", "/posts/" + str(i))
#     response = conn.getresponse().read()
#     result = eval(response.decode('utf-8'))['title']
#     # print(result)
# print(f"-> http.client : {time.time()-start}\n")
        





