from requests import Response


class Checking():
    @staticmethod
    def check_status_code(response: Response, status_code):
        assert status_code == response.status_code
        if response.status_code == status_code:
            print("Success. Received the expected status code: " + str(status_code))
        else:
            print("Failure. Expected status: code not received: " + str(status_code))