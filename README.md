#Usage
Register
Endpoint: /register/
Method: POST
Description: Register a new user account.
Parameters:
email (string): User's email address.
password (string): User's password.

Login
Endpoint: /login/
Method: POST
Description: Authenticate and log in a user.
Parameters:
email (string): User's email address.
password (string): User's password.


Logout
Endpoint: /logout/
Method: GET
Description: Log out the authenticated user.


Scrape Product
Endpoint: /scrape/
Method: POST
Description: Scrape product information from a provided URL.
Parameters:
url (string): URL of the product page to scrape.

List Scaped Products
Endpoint: /scrape/
Method: GET
Description: Retrieve a list of products scraped by the authenticated user.


Authentication
The API uses token-based authentication(JWT). After logging in, the user receives an access token that must be included in the headers of subsequent requests for authentication.

Data Models
The API uses the following data models:

User: Represents a registered user with email and password.

Product: Represents a scraped product with information such as title, price, description, ratings, and more.

Custom Endpoints
The API includes custom endpoints to enhance functionality:

CustomTokenObtainPairView: Extends the default TokenObtainPairView to include the user's ID in the token payload.

Error Handling
The API returns appropriate error responses for various scenarios, such as invalid credentials, authentication required, and failed URL scraping.

Dependencies
Django
Django Rest Framework
Requests
BeautifulSoup (for web scraping)
