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

conn = FrappeClient("example.com")
conn.login("user@example.com", "password")
```

#### Use token based authentication

```py
from frappeclient import FrappeClient

client = FrappeClient("https://example.com")
client.authenticate("my_api_key", "my_api_secret")
```

For demonstration purposes only! Never store any credentials in your source code. Instead, you could set them as environment variables and fetch them with `os.getenv()`.

#### get_list

Get a list of documents from the server

Arguments:
- `doctype`
- `fields`: List of fields to fetch
- `filters`: Dict of filters
- `limit_start`: Start at row ID (default 0)
- `limit_page_length`: Page length
- `order_by`: sort key and order (default is `modified desc`)

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

#### get_doc

Fetch a document from the server

Arguments
- `doctype`
- `name`

```py
doc = conn.get_doc('Customer', 'Example Co')
```

#### get_value

Fetch a single value from the server

Arguments:

- `doctype`
- `fieldname`
- `filters`

```py
customer_name = conn.get_value("Customer", "name", {"website": "example.net"})
```

#### update

Update a document (if permitted)

Arguments:
- `doc`: JSON document object

```py
doc = conn.get_doc('Customer', 'Example Co')
doc['phone'] = '000000000'
conn.update(doc)
```

#### delete

Delete a document (if permitted)

Arguments:
- `doctype`
- `name`

```py
conn.delete('Customer', 'Example Co')
```

### Example

```python
from frappeclient import FrappeClient

conn = FrappeClient("example.com", "user@example.com", "password")
new_notes = [
	{"doctype": "Note", "title": "Sing", "public": True},
	{"doctype": "Note", "title": "a", "public": True},
	{"doctype": "Note", "title": "Song", "public": True},
	{"doctype": "Note", "title": "of", "public": True},
	{"doctype": "Note", "title": "sixpence", "public": True}
]

for note in new_notes:
	print(conn.insert(note))

# get note starting with s
notes = conn.get_list('Note',
	filters={'title': ('like', 's')},
	fields=["title", "public"]
)
```

### Example

See example.py for more info

### License

MIT
