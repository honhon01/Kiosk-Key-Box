import http.client

params = urllib.parse.urlencode({'@BookingID': '1', '@RoomID': '1', '@Pin': '112233'})
headers = {}

conn = http.client.HTTPConnection('202.44.12.92:4000')
conn.request("GET","/pin/validate", params, headers)
r1 = conn.getresponse()
print(r1.status)
