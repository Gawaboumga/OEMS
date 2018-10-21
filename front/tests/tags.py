from django.test import TestCase, override_settings
from django.urls import reverse
from oems.settings import TEST_MEDIA_ROOT
from front import views
from front.tests import utils


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class TagsTests(TestCase):

    def test_spread_on_several_pages(self):
        utils.log_as(self, utils.UserType.STAFF)

        number_of_tags = views.PAGINATION_SIZE * 3 + views.PAGINATION_SIZE // 2
        tags = self.__create_tags(number_of_tags)

        for i in range(number_of_tags // views.PAGINATION_SIZE):
            response = self.client.get(reverse('front:tags') + "?page={}".format(i + 1))

            for f in tags[i * views.PAGINATION_SIZE:min((i + 1) * views.PAGINATION_SIZE, number_of_tags)]:
                self.assertContains(response, reverse('front:tag', kwargs={'pk': f.pk}))

    def __create_tags(self, number_of_tags):
        return sorted([utils.create_tag(self) for _ in range(number_of_tags)], key=lambda x: x.tag.lower())
