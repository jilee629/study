import time
import urllib3
import requests
import urllib.request
import http.client
import asyncio
import aiohttp

def t_urllib(curl, n):
    start = time.time()
    result =  list()
    for i in range(1,n):
        response = urllib.request.urlopen(url + str(i)).read()
        result.append(eval(response.decode('utf-8'))['title'])
    print(f"\n-> urllib : {time.time()-start}")
    print(result)

def t_http(n):
    start = time.time()
    result =  list()
    for i in range(1,n):
        conn = http.client.HTTPSConnection("jsonplaceholder.typicode.com")
        conn.request("GET", "/posts/" + str(i))
        response = conn.getresponse().read()
        result.append(eval(response.decode('utf-8'))['title'])
    print(f"\n-> http.client : {time.time()-start}")
    print(result)

def t_requests(curl, n):
    start = time.time()
    result =  list()
    for i in range(1, n):
        response = requests.get(url + str(i))
        result.append(response.json()['title'])
    print(f"\n-> request : {time.time()-start}")
    print(result)

def t_urllib3(curl, n):
    start = time.time()
    result =  list()
    http = urllib3.PoolManager()
    for i in range(1, n):
        response = http.request('GET', url + str(i))
        result.append(response.json()['title'])
    print(f"\n-> urllib3 : {time.time()-start}")
    print(result)

async def fetch(session, url):
    async with session.get(url) as response:
        response = await response.json()
        result = response['title']
        return result

async def main(url, n):
    start = time.time()
    async with aiohttp.ClientSession() as session:
        tasks = list()
        for i in range(1, n):
            tasks.append(fetch(session, url + str(i)))
        result = await asyncio.gather(*tasks)
        print(f"\n-> aiphttp : {time.time()-start}")
        print(result)

if __name__ == "__main__":

    url = "https://jsonplaceholder.typicode.com/posts/"
    n = 11

    asyncio.run(main(url, n))
    t_urllib3(url, n)
    t_requests(url, n)
    t_urllib(url, n)
    t_http(n)


        





