import unittest
import sys; print(sys.path, "TESTTT")
from src.config import TestingConfig
from unittest.mock import patch
from flask import url_for
from flask_testing import TestCase
from src.main import create_app
from src.extensions import db

class TestEventService(TestCase):
    def create_app(self):
        return create_app(TestingConfig)

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
    
    @patch('src.commands.create_event.CreateEventCommandHandler.handle')
    def test_create_event(self, mock_handle):
        mock_handle.return_value = 1  
        response = self.client.post(url_for('event.create_event'), json={
    "name": "City Marathon 2024",
    "description": "Annual city marathon covering the downtown area with multiple categories for participants of all ages.",
    "event_date": "2024-08-22T07:00:00", 
    "duration": 5,
    "location": "Downtown City Park",
    "category": "Running",
    "fee": 50,
    "additional_info": {
        "registration_deadline": "2024-08-31",
        "max_participants": 5000,
        "min_age": 18
    }
    })
        self.assert200(response)
        self.assertEqual(response.json['event_id'], 1)

    @patch('src.queries.get_event.GetEventQueryHandler.handle')
    def test_get_event(self, mock_handle):
        mock_handle.return_value = {'id': 1, 'name': 'Sample Event'}
        response = self.client.get(url_for('event.get_event', event_id=1))
        self.assert200(response)
        self.assertEqual(response.json['name'], 'Sample Event')
if __name__ == '__main__':
    unittest.main()
