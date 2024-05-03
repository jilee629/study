import time
import urllib3
import requests
import urllib.request
import http.client
import asyncio
import aiohttp

def t_urllib(curl, n):
    start = time.time()
    for i in range(1,n):
        response = urllib.request.urlopen(url + str(i)).read()
        result = eval(response.decode('utf-8'))['title']
        # print(result)
    print(f"-> urllib : {time.time()-start}")

def t_http(n):
    start = time.time()
    for i in range(1,n):
        conn = http.client.HTTPSConnection("jsonplaceholder.typicode.com")
        conn.request("GET", "/posts/" + str(i))
        response = conn.getresponse().read()
        result = eval(response.decode('utf-8'))['title']
        # print(result)
    print(f"-> http.client : {time.time()-start}")

def t_requests(curl, n):
    start = time.time()
    for i in range(1, n):
        response = requests.get(url + str(i))
        result = response.json()['title']
        # print(result)
    print(f"-> request : {time.time()-start}")

def t_urllib3(curl, n):
    start = time.time()
    http = urllib3.PoolManager()
    for i in range(1, n):
        response = http.request('GET', url + str(i))
        result = response.json()['title']
        # print(result)
    print(f"-> urllib3 : {time.time()-start}")

async def fetch(session, url):
    async with session.get(url) as response:
        response = await response.json()
        result = response['title']
        # print(result)

async def main(url, n):
    start = time.time()
    async with aiohttp.ClientSession() as session:
        tasks = list()
        for i in range(1, n):
            tasks.append(fetch(session, url + str(i)))
        await asyncio.gather(*tasks)
    print(f"-> urllib3 : {time.time()-start}")

if __name__ == "__main__":

    url = "https://jsonplaceholder.typicode.com/posts/"
    n = 101

    t_requests(url, n)
    t_urllib(url, n)
    t_urllib3(url, n)
    t_http(n)
    asyncio.run(main(url, n))

        





