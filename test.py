import http.client, json

PinCode = '806388'
conn = http.client.HTTPConnection("ec2-54-169-49-29.ap-southeast-1.compute.amazonaws.com:4000")
conn.request("GET", "/pin/validate?Pin="+PinCode)
r1 = conn.getresponse()
dataGet = r1.read().decode('utf-8')
conn.close()
print(r1.status, r1.reason)
print("GET : "+PinCode)
print(dataGet)
if dataGet[8] == 't':
    print("OK")
else:
    print("Wrong")

print("\n\n")


BODY = "{\"UsageID\":3,\"ReturnInTime\":1}"
headers = {"Content-Type":"application/json","Authorization":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IjU4MDcwNTAzNDM4IiwiaWF0IjoxNTU1MDUzMTEwfQ.vFrdCwfSSQQ3UXpPruawuUOze0FCu_lbOHnFP2KcQqY"}
conn = http.client.HTTPConnection("ec2-54-169-49-29.ap-southeast-1.compute.amazonaws.com:4000")
conn.request("PUT", "/pin/status", BODY,headers)
r1 = conn.getresponse()
dataPut = r1.read().decode('utf-8')
conn.close()
print(r1.status, r1.reason)
print("PUT : "+BODY)
print(dataPut)


