from requests import Response
from utils.checking import Checking
from utils.api import Google_maps_api


class TestCreateTest:
    def test_create_new_place(self):
        print('Method POST')
        result_post: Response = Google_maps_api.create_new_place()
        Checking.check_status_code(result_post, 200)

        check_post = result_post.json()
        assert isinstance(check_post, dict), f"Expected dict type, but came {type(check_post)}"

        assert "status" in check_post, (f"No 'status' field in the response")
        assert "place_id" in check_post, (f"No 'place_id' field in the response")

        assert check_post["status"] == "OK", f"Expected 'OK', but came {check_post['status']}"

        place_id = check_post.get('place_id')
        assert place_id, (f"'place_id' is empty or None")

        print(f"Test is OK, place_id = {place_id}")

        print('Method GET: positive')
        result_get: Response = Google_maps_api.get_new_place(place_id)
        Checking.check_status_code(result_get, 200)

        check_get = result_get.json()
        assert isinstance(check_get, dict), f"Expected dict type, but came {type(check_get)}"

        for field in ["address", "name", "language", "location"]:
            assert field in check_get, f"No '{field}' field in the response"

        assert check_get["name"] == "Frontline house", f"Expected 'Frontline house' but got {check_get['name']}"
        assert check_get["address"] == "29, side layout, cohen 09", (f"Expected '29, side layout, cohen 09' "
                                                                     f"but got {check_get['address']}")
        assert check_get["language"] == "French-IN", f"Expected 'French-IN' but got {check_get['language']}"

        print("GET method check passed successfully")

        print('Method PUT')
        result_put: Response = Google_maps_api.put_new_place(place_id)
        Checking.check_status_code(result_put, 200)

        expected_put_msg = "Address successfully updated"
        actual_put_msg = result_put.json().get("msg")
        assert actual_put_msg == expected_put_msg, f"Expected PUT msg: {expected_put_msg!r}, got {actual_put_msg!r}"

        # Проаерка, что адрес обновлён
        result_get: Response = Google_maps_api.get_new_place(place_id)
        Checking.check_status_code(result_get, 200)
        assert isinstance(result_get.json(), dict), f"GET response is not dict: {type(result_get.json())}"

        expected_address = "89 Vernadskogo street,RU"
        actual_address = result_get.json().get("address")
        assert actual_address == expected_address, (
            f"Address not updated correctly: expected {expected_address!r}, got {actual_address!r}"
        )

        print("Positive PUT method check passed successfully")

        print('Method GET: negative')
        fake_place_id = "this_place_id_does_not_exist_12345"
        result_put: Response = Google_maps_api.put_new_place(fake_place_id)
        # Ожидаем 404
        Checking.check_status_code(result_put, 404)

        expected_error = "Update address operation failed, looks like the data doesn't exists"
        actual_error = result_put.json().get("msg")
        assert actual_error == expected_error, f"PUT msg mismatch: expected {expected_error!r}, got {actual_error!r}"

        print("PUT negative flow verified: 404 and error msg OK")

        print('Method DELETE')
        result_delete: Response = Google_maps_api.delete_new_place(place_id)
        Checking.check_status_code(result_delete, 200)

        result_delete: Response = Google_maps_api.delete_new_place(place_id)
        Checking.check_status_code(result_delete, 404)
        expected_msg = "Delete operation failed, looks like the data doesn't exists"
        actual_msg = result_delete.json().get("msg")
        print(actual_msg)
        assert actual_msg == expected_msg, f"Re-DELETE msg mismatch: expected {expected_msg!r}, got {actual_msg!r}"

        print("DELETE success flow verified: status OK and re-DELETE returns 404 + expected msg")