import requests


class OneLicenceClient:
    def __init__(self, config):
        self.server_url = config['server_url']
        self.product_id = config['product_id']
        self.version_id = config['version_id']
        self.license_id = config['license_id']
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

    def consume(self):
        """
        Check license validity
        """

        response = requests.put(url=self.consumeUrl)
        status = response.status_code
        data = response.json()

        if status == 200:
            return
        elif data["code"] == "API_CALLS_EXHAUSTED":
            raise self.APICallLimitExhausted
        elif data["code"] == "LICENSE_EXPIRED":
            raise self.LicenseExpiredError
        else:
            raise self.InternalServerError


# Example usage
# l = OneLicenceClient({
#     "server_url": "http://127.0.0.1:3000/api/v1",
#     "product_id": "5ea6de7033482715d4c72e05",
#     "version_id": "5ea6de7833482715d4c72e06",
#     "license_id": "5ea6e2b8cce5af1677e5dd59"
# })

# l.consume()
