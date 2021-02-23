"""Use this template for retrieving HTTP response headers"""

# import requests module 
import requests 
  
# Making a get request 
response = requests.get('https://api.github.com') 
  
# print response 
print(response) 
  
# print headers of response 
print(response.headers)
