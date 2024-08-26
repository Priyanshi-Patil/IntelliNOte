import urllib3
from urllib3 import HTTPConnectionPool
import ssl

cert = r"C:\\Users\\hp\\ca-cerrt.pem"
key = r"C:\\Users\\hp\\ca-keey.pem"

context = ssl.create_default_context()
context.load_cert_chain(cert, keyfile=key)

http = urllib3.PoolManager.ssl_context = context
pool = urllib3.PoolManager()  # Create a PoolManager instance
pool = HTTPConnectionPool('http://localhost/', port=80)
response = pool.request('GET', 'http://localhost/', port=80)
print(response.status)
print(response.version)  # Print the HTTP version used (e.g., HTTP/1.1)