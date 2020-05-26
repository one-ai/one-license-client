import requests


class OneLicenceClient:
    def __init__(self, config):
        self.server_url = config['server_url']
        self.product_id = config['product_id']
        self.version_id = config['version_id']
        self.license_id = config['license_id']
        self.client_type = config['client_type']
        self.consumeUrl = self.server_url + '/products/{}/versions/{}/licenses/{}/consume'.format(
            self.product_id, self.version_id, self.license_id)

    class LicenseExpiredError(Exception):
        """
        Raised when license has expired
        """

        def __str__(self):
            return "The validity of this license has expired. Please ask your license provider to renew it."

    class APICallLimitExhausted(Exception):
        """
        Raised when API call limit has exhausted
        """

        def __str__(self):
            return "API calls allocated to this license has been exhausted. Please ask your license provider for more API calls."

    class InternalServerError(Exception):
        """
        Raised when lincense server has internal error
        """

        def __str__(self):
            return "There has been some internal errors on the Licensing server. Please contact your license provider."

    class InsufficientParametersError(Exception):
        """
        Raised when insufficient parameters are sent to the server
        """

        def __str__(self):
            return "Some parameters are missing in the request. Please check and make the request again."

    def consume(self):
        """
        Check license validity
        """

        response = requests.put(url=self.consumeUrl, json={
                                'clientType': self.client_type})
        status = response.status_code
        data = response.json()

        if status == 200:
            return
        elif data["code"] == "API_CALLS_EXHAUSTED":
            raise self.APICallLimitExhausted
        elif data["code"] == "LICENSE_EXPIRED":
            raise self.LicenseExpiredError
        elif data["code"] == "INSUFFICIENT_PARAMETERS":
            raise self.InsufficientParametersError
        else:
            raise self.InternalServerError


# Example usage
l = OneLicenceClient({
    "server_url": "http://localhost:4000/api/v1",
    "product_id": "5ebac9818ebfb4674f5de126",
    "version_id": "5ebac98c8ebfb4674f5de127",
    "license_id": "5ecd13bcf858965d2d8e604e",
    "client_type": "INDEPENDENT_CLIENT"
})

l.consume()
