## Frappe Client

Python Library for interacting with Frappe / ERPNext API

### Usage

	from frappeclient import FrappeClient

	client = FrappeClient("example.com", "user@example.com", "password")

	customer_name = client.get_value("Customer", {"email_id": "test@customer.com"})
	customer = client.get("Customer", customer_name)


### Example

See example.py for more info

### License

MIT
