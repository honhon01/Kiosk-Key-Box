import http.client, urllib.parse

params = urllib.parse.urlencode({'@Pin': 112233})
headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IjU4MDcwNTAzNDM4IiwiaWF0IjoxNTU1MDUzMTEwfQ.vFrdCwfSSQQ3UXpPruawuUOze0FCu_lbOHnFP2KcQqY"}


conn = http.client.HTTPConnection("http://ec2-54-169-49-29.ap-southeast-1.compute.amazonaws.com:4000")
conn.request("GET", "/pin/validate", params, headers)
response = conn.getresponse()
print(response.status, response.reason)
conn.close()
