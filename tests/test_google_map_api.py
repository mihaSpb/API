from requests import Response

from utils.api import Google_maps_api


class TestCreateTest():
    def test_create_new_place(self):
        print('Method POST')
        result_post: Response = Google_maps_api.create_new_place()