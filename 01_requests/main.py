import requests


url_get = "https://httpbin.org/get"
url_post = "https://httpbin.org/post"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0"
}


params = {"key1": "value1", "key2": "value2"}

# response = requests.get(url_get, headers=headers, params=params)
response = requests.post(url_post, headers=headers, data={"kw": "b"})

print(response.content)

# with open("image.png", "wb") as f:
#     f.write(response.content)


# response.text = """ 
# {
#   "args": {
#     "key1": "value1",
#     "key2": "value2"
#   },
#   "headers": {
#     "Accept": "*/*",
#     "Accept-Encoding": "gzip, deflate, zstd",
#     "Host": "httpbin.org",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0",
#     "X-Amzn-Trace-Id": "Root=1-6970f8ca-271c638e12b48d5a3a480808"
#   },
#   "origin": "34.220.251.2",
#   "url": "https://httpbin.org/get?key1=value1&key2=value2"
# }
# """
# response.content = b'{\n  "args": {}, \n  "data": "", \n  "files": {}, \n  "form": {\n    "kw": "b"\n  }, \n  "headers": {\n    "Accept": "*/*", \n    "Accept-Encoding": "gzip, deflate, zstd", \n    "Content-Length": "4", \n    "Content-Type": "application/x-www-form-urlencoded", \n    "Host": "httpbin.org", \n    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0", \n    "X-Amzn-Trace-Id": "Root=1-6970fabd-2ff71f39687ace45040a65fa"\n  }, \n  "json": null, \n  "origin": "34.220.251.2", \n  "url": "https://httpbin.org/post"\n}\n'



import re

s = "world 1234 \nhello 5678 "
pattern = re.compile(r"h\w+ (\d+)")

match = pattern.search(s)

if match:
    print("Matched number:", match.group())


