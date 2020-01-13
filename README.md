## Frappe Client

Simple Frappe-like Python wrapper for Frappe REST API

### Install

```
git clone https://github.com/frappe/frappe-client
pip install -e frappe-client
```

### API

FrappeClient has a frappe like API

#### Login

Login to the Frappe HTTP Server by creating a new FrappeClient object

```py
from frappeclient import FrappeClient
conn = FrappeClient("example.com", "user@example.com", "password")
```

#### get_list

Get a list of documents from the server

Arguments:
	- `fields`: List of fields to fetch
	- `filters`: Dict of filters

```py
users = conn.get_list('User', fields = ['name', 'first_name', 'last_name'], , filters = {'user_type':'System User'})
```

Example of filters:
- `{ "user_type": ("!=", "System User") }`
- `{ "creation": (">", "2020-01-01") }`
- `{ "name": "test@example.com" }`

#### insert

Insert a new document to the server

Arguments:
	- `doc`: Document object

```python
doc = conn.insert({
	"doctype": "Customer",
	"customer_name": "Example Co",
	"customer_type": "Company",
	"website": "example.net"
})
```

### get_doc

Fetch a document from the server

```py
doc = conn.get_doc('Customer', 'Example Co')
```

### get_value

Fetch a single value from the server

Arguments:
	- `doctype`
	- `fieldname`
	- `filters`

```py
customer_name = client.get_value("Customer", "name", {"website": "example.net"})
```

### Example

```python
from frappeclient import FrappeClient

conn = FrappeClient("example.com", "user@example.com", "password")
notes = [
		{"doctype": "Note", "title": "Sing", "public": True},
		{"doctype": "Note", "title": "a", "public": True},
		{"doctype": "Note", "title": "Song", "public": True},
		{"doctype": "Note", "title": "of", "public": True},
		{"doctype": "Note", "title": "sixpence", "public": True}
	]

for note in notes:
	print(conn.insert(note))

notes_starting_with_s = conn.get_doc(
	'Note',
	filters={'title': ('like', 's') },
	fields=["title", "public"])
```

### Example

See example.py for more info

### License

MIT
