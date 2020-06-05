# One License Client

## How to use

### For Python

1. Import `one_license_client`
2. At the start of your application initialize the client
```
l = OneLicenceClient({
    "server_url": "http://localhost:4000/api/v1",
    "product_id": "5edb10fecc150913cb7640f6",
    "version_id": "5edb1105cc150913cb7640f7",
    "license_id": "5edb1264cc150913cb7640f8",
})
```
3. At the end of every API call include `l.consume()`


- Get values of `server_url`, `product_id`, `version_id` and `license_id` from the online licensing sever
- View `demo.py` for sample usage.