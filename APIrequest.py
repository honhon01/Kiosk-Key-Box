import http.client, urllib.parse

params = urllib.parse.urlencode({'@BookingID': '1', '@RoomID': '1', '@Pin': '112233'})
headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IjU4MDcwNTAzNDM4IiwiaWF0IjoxNTU1MDUzMTEwfQ.vFrdCwfSSQQ3UXpPruawuUOze0FCu_lbOHnFP2KcQqY"}

conn = http.client.HTTPConnection('202.44.12.92:4000')
conn.request("GET","/pin/validate", params, headers)
r1 = conn.getresponse()
print(r1.status)
conn.close()
