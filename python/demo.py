import one_license_client

# Example usage
l = OneLicenceClient({
    "server_url": "http://localhost:4000/api/v1",
    "product_id": "5edb10fecc150913cb7640f6",
    "version_id": "5edb1105cc150913cb7640f7",
    "license_id": "5edb1264cc150913cb7640f8",
})

l.consume()

# Simpulating a flask server
while True:
    pass
