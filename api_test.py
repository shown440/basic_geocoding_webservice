import requests
r = requests.get('http://dummy.restapiexample.com/api/v1/employees')
print(r.json())
