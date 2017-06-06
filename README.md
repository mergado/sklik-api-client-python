# Sklik API Client for Python

This is low lever library to encapsulate [Sklik API Drak](https://api.sklik.cz/drak/usage.html). This library is made by [Mergado](http://www.mergado.cz/). Your comments and suggestions are welcome at developers@mergado.com.

## Usage

```python
from sklikapiclient import client

# There is two types of authentication.

# First is via user name and password.
sklik = client.Sklik(username='your_username', password='your_password')

# Second is via api key which can user generate in Sklik settings.
sklik = client.Sklik(api_key='your_api_key')

# example of HTTP GET method - get client credit
sklik.get('client.getCredit')

# example of HTTP POST method - create campaign
sklik.post('campaigns.create', [{'name': 'name of campaign', 'datBudget': 10000}])

# example of HTTP POST method - update two campaings in one request
sklik.post('campaigns.update', [{'id': 314159, 'name': 'new name of campaign'},
                                {'id': 271828, 'name': 'other new name'}])

```
