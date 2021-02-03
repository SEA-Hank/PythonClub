from django.test import TestCase
from .models import Meeting, Minute, Resource, Event
from django.contrib.auth.models import User
import datetime
from .views import index, getMeeting, meetingDetails
from django.urls import reverse
from django.utils import timezone
# Testing models


class MeetingTest(TestCase):
    def test_string(self):
        met = Meeting(title='meeting on sunday')
        self.assertEqual(str(met), met.title)

    def test_table(self):
        self.assertEqual(str(Meeting._meta.db_table), 'Meeting')


class MinuteTest(TestCase):
    def test_string(self):
        testMin = Minute(text='hiking on Monday')
        self.assertEqual(str(testMin), testMin.text)

    def test_table(self):
        self.assertEqual(str(Minute._meta.db_table), 'Minute')


class EventTest(TestCase):

    def test_string(self):
        testEvent = Event(title='seahawks vs rams')
        self.assertEqual(str(testEvent), testEvent.title)

    def test_table(self):
        self.assertEqual(str(Event._meta.db_table), 'Event')


class ResourceTest(TestCase):
    def setup(self):
        testUser = User(username='hank')
        testResource = Resource(
            name='TAKE 6',
            type='Music',
            URL='www.jazzalley.com',
            description='Dimitriou’s Jazz Alley welcomes 10x Grammy-winning American a cappella gospel sextet Take 6 for four nights and six shows.',
            userid=testUser,
            date=datetime.datetime(2021, 6, 1))
        return testResource

    def test_string(self):
        testResource = self.setup()
        self.assertEqual(str(testResource), testResource.name)

    def test_table(self):
        self.assertEqual(str(Resource._meta.db_table), 'Resource')


# Testing Basic views
class IndexTest(TestCase):
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)


class GetMeetingTest(TestCase):
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('getMeeting'))
        self.assertEqual(response.status_code, 200)


class MeetingDetailsTest(TestCase):
    def setUp(self):
        self.meeting1 = Meeting.objects.create(
            title='To prevent the flu',
            date=datetime.datetime.now(tz=timezone.utc),
            time=datetime.time(10, 33, 45),
            location='The library at Seattle downtown',
            Agenda="Should we wear mask and keep  Social distance")

        self.meeting2 = Meeting.objects.create(
            title='watching football',
            date=datetime.datetime.now(tz=timezone.utc),
            time=datetime.time(10, 33, 40),
            location='at home',
            Agenda="watching football")

    def test_meeting_details_success(self):
        response = self.client.get(
            reverse('meetingDetails', args=(self.meeting1.id,)))
        # Assert that self.post is actually returned by the post_detail view
        self.assertEqual(response.status_code, 200)

    def test_number_of_meeting(self):
        meetingCount = Meeting.objects.count()
        self.assertEqual(meetingCount, 2)
