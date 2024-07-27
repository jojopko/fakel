import unittest
import json

from fakel.events.wall_post_new import _get_best_photo, _get_only_photo_from_attachments
from fakel.models import VKEventModel


class TestBestPhoto(unittest.TestCase):

    def setUp(self) -> None:
        with open('tests/fixtures/messages/small_text_1_photo.json', 'rb') as f:
            self.small_text_1_photo = VKEventModel(**json.load(f))
        with open('tests/fixtures/messages/small_text_1_photo_repost.json', 'rb') as f:
            self.small_text_1_photo_repost = VKEventModel(**json.load(f))

    def test_get_best_photo_valid(self):
        obj = self.small_text_1_photo.object.get_preferred_object()
        photos = _get_only_photo_from_attachments(obj.attachments)
        photo = _get_best_photo(photos[0])

        assert photo.type == 'y'
        assert photo.width == 783
        assert photo.height == 365

        obj = self.small_text_1_photo_repost.object.get_preferred_object()
        photos = _get_only_photo_from_attachments(obj.attachments)
        photo = _get_best_photo(photos[0])

        assert photo.type == 'z'
        assert photo.width == 1080
        assert photo.height == 810
