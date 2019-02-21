## Frappe Client

Python Library for interacting with Frappe / ERPNext API

### Usage

### Create a Customer, and then fetch it back from the HTTP API
```python
from frappeclient import FrappeClient

client = FrappeClient("https://example.com")
client.login("user@example.com", "password")

# Prepare a customer dict that we will use to create a new
# customer in ERPNext
doc = {"doctype": "Customer",
       "customer_name": "Example Inc.",
       "customer_type": "Company",
       "website": "example.net"}

# create new record in ERPNext
client.insert(doc)

# Query the erpnext HTTP API for the name of customer whos
# website is example.net
customer_name = client.get_value("Customer",
                                 "name",
                                 {"website": "example.net"})
# Fetch customer
customer = client.get_doc("Customer", customer_name['name'])
```

#### Fetch a list of Items from the HTTP API
```python
from frappeclient import FrappeClient

client = FrappeClient("https://example.com")
client.login("user@example.com", "password")
notes = [{"doctype": "Note", "title": "Sing", "public": True},
         {"doctype": "Note", "title": "a", "public": True},
         {"doctype": "Note", "title": "Song", "public": True},
         {"doctype": "Note", "title": "of", "public": True},
         {"doctype": "Note", "title": "sixpence", "public": True}
         ]

for note in notes:
    print(client.insert(note))

# Query for Note using only filters, and fields arguments. Returns a list
# of four dicts with the respective titles Sing, Song and sixpence.
notes_starting_with_S = client.get_doc(
    'Note',
    filters=[["Note", "title", "LIKE", "S%"]],
    fields=["title", "public"])
```

#### Use token based authentication
```python
from frappeclient import FrappeClient

client = FrappeClient("https://example.com")
client.authenticate("my_api_key", "my_api_secret")
```

For demonstration purposes only! Never store any credentials in your source code. Instead, you could set them as environment variables and fetch them with `os.getenv()`.

### Example

See example.py for more info

### License

MIT
