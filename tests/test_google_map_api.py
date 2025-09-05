from requests import Response
from utils.api import Google_maps_api


class TestCreateTest():
    def test_create_new_place(self):
        print('Method POST')
        result_post: Response = Google_maps_api.create_new_place()
        assert result_post.status_code == 200, (f"Expected status code 200, but came {result_post.status_code}")

        check_post = result_post.json()
        assert isinstance(check_post, dict), (f"Expected dict type, but came {type(check_post)}")

        assert "status" in check_post, (f"No 'status' field in the response")
        assert "place_id" in check_post, (f"No 'place_id' field in the response")

        assert check_post["status"] == "OK", (f"Expected 'OK', but came {check_post['status']}")

        place_id = check_post.get('place_id')
        assert place_id, (f"'place_id' is empty or None")

        print(f"Test is OK, place_id = {place_id}")