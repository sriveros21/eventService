# commands/create_event_command.py
from datetime import datetime, timedelta
from models.event import Event, db
from sqlalchemy.exc import IntegrityError

class CreateEventCommandHandler:
    def validate_data(self, data):
        # Ensure all mandatory fields are present
        mandatory_fields = ['name', 'description', 'event_date', 'duration', 'location', 'category', 'fee']
        missing_fields = [field for field in mandatory_fields if field not in data]
        if missing_fields:
            raise ValueError(f"Missing mandatory field(s): {', '.join(missing_fields)}")

    def check_overlap(self, data, event_id=None):
        if isinstance(data['event_date'], str):
            event_start = datetime.strptime(data['event_date'], '%Y-%m-%dT%H:%M:%S')
        elif isinstance(data['event_date'], datetime):
            event_start = data['event_date']
        else:
            raise ValueError("event_date must be a string or datetime")
        event_end = event_start + timedelta(hours=data['duration'])

        # Fetch events that could potentially overlap
        potential_overlaps = Event.query.filter(
            Event.location == data['location'],
            Event.id != event_id,  # Exclude the current event if updating
            Event.event_date <= event_end,
            Event.event_date >= event_start - timedelta(hours=24) # Consider a 24-hour buffer before the event
        ).all()

        # Now filter in Python to check for actual overlap
        for event in potential_overlaps:
            existing_event_end = event.event_date + timedelta(hours=event.duration)
            if existing_event_end > event_start and event.event_date < event_end:
                raise ValueError("An event is already scheduled at this location during the specified timeframe.")

    def handle(self, data):
        self.validate_data(data)
        if isinstance(data['event_date'], str):
            data['event_date'] = datetime.strptime(data['event_date'], '%Y-%m-%dT%H:%M:%S')
        self.check_overlap(data)
        
        try:
            event = Event(**data)
            db.session.add(event)
            db.session.commit()
            return event.id
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Failed to create event due to a database error.")
