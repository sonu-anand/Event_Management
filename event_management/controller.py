from datetime import datetime
import pytz
from .models import Event, Register
from .database import Session
import re

def create_event(data):
    fields = ['name','location','start_time','end_time','max_capacity']
    missing_keys = []
    no_data_keys = []
    for i in data:
        if i not in fields:
            missing_keys.append(i)
        else:
            if not data.get(i):
                no_data_keys.append(i)
    if missing_keys and no_data_keys:
        return {'Response': f'Some keys are missing >>> {missing_keys} and Some keys are empty >>> {no_data_keys}'}
    elif missing_keys:
        return {'Response': f'Some keys are missing >>> {missing_keys}'}
    elif no_data_keys:
        return {'Response': f'Some keys are emmpty >>> {no_data_keys}'}
    else:
        st_flag = True
        et_flag = True
        if not re.search(r'[\d]{4}\-[\d]{2}\-[\d]{2}\s{1}[\d]{1,2}\:[\d]{2}\s{1}[A|P]M',data['start_time'],flags=re.I):
            st_flag = False
        
        if not re.search(r'[\d]{4}\-[\d]{2}\-[\d]{2}\s{1}[\d]{1,2}\:[\d]{2}\s{1}[A|P]M',data['end_time'],flags=re.I):
            et_flag = False
        
        if not st_flag and not et_flag:
            return {'Reponse': 'Start Time and End Time should be in format: YYYY-MM-DD HH:MM AM|PM Eg.2025-09-10 9:30 PM'}
        elif not st_flag:
            return {'Reponse': 'Start Time Format should be YYYY-MM-DD HH:MM AM|PM Eg.2025-09-10 9:30 PM'}
        elif not et_flag:
            return {'Reponse': 'End Time Format should be YYYY-MM-DD HH:MM AM|PM Eg.2025-09-10 9:30 PM'}

        st = data["start_time"]
        et = data["end_time"]
        ist = pytz.timezone('Asia/Kolkata')

        if st:
            final_st = datetime.strptime(st, '%Y-%m-%d %I:%M %p')
            st = ist.localize(final_st)
        if et:
            final_et = datetime.strptime(et, '%Y-%m-%d %I:%M %p')
            et = ist.localize(final_et)
        
        if not isinstance(data['max_capacity'], int):
            return {'Response': "Max capacity should be Integer only"}
        
        event = Event(
            name=data["name"],
            location=data["location"],
            start_time=st,
            end_time=et,
            max_capacity=data["max_capacity"]
        )
        session = Session()
        session.add(event)
        session.commit()
        return {"Response": "Data Inserted Into Events Table Successfully!"}

def get_all_events():
    session = Session()
    events = session.query(Event).all()
    return [{
        "id": e.id,
        "name": e.name,
        "location": e.location,
        "start_time": e.start_time,
        "end_time": e.end_time,
        "max_capacity": e.max_capacity
    } for e in events if e.start_time>datetime.now()]

def register_attendee(event_id, data):
    fields = ['name','email','event_id']
    missing_keys = []
    no_data_keys = []
    for i in data:
        if i not in fields:
            missing_keys.append(i)
        else:
            if not data.get(i):
                no_data_keys.append(i)
    if missing_keys and no_data_keys:
        return {'Response': f'Some keys are missing >>> {missing_keys} and Some keys are empty >>> {no_data_keys}'}
    elif missing_keys:
        return {'Response': f'Some keys are missing >>> {missing_keys}'}
    elif no_data_keys:
        return {'Response': f'Some keys are emmpty >>> {no_data_keys}'}
    else:
        if not isinstance(data['event_id'], int):
            return {'Response': "Event ID should be Integer only"}
        if not re.search(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',data['email'],flags=re.I):
            return {'Response': 'Not a valid Email'}
        session = Session()

        if session.query(Register).filter_by(email=data['email']).first():
            return {"Response": "Email ID already exists"}
        # breakpoint()
        event = session.query(Event).get(event_id)
        if not event:
            return {"Response": "Event ID not found"}

        current_registrations = session.query(Register).filter_by(event_id=event_id).count()
        if current_registrations >= event.max_capacity:
            return {"Response": "Sorry! Max capacity reached"}

        attendee = Register(
            name=data['name'],
            email=data['email'],
            event_id=event_id
        )
        session.add(attendee)
        session.commit()
        return {"Response": f"User Registered Successfully for event ID {event_id}"}

def get_attendees(event_id):
    session = Session()
    attendees = session.query(Register).filter_by(event_id=event_id).all()
    return [{
        "id": a.id,
        "name": a.name,
        "email": a.email,
        "event_id": a.event_id
    } for a in attendees]

def change_timezone(data):
    session = Session()
    if data.get('timezone'):
        timezone_string = data.get('timezone', 'UTC')
    else:
        return {'Response': 'Please enter correct timezone. Eg.America/New_York, Europe/London, Asia/Singapore'}
    
    events = session.query(Event).all()

    for eve in events:
        start_time_in_db = str(eve.start_time)
        end_time_in_db = str(eve.end_time)

        utc = pytz.utc
        start_utc = utc.localize(datetime.strptime(start_time_in_db, "%Y-%m-%d %H:%M:%S"))
        end_utc = utc.localize(datetime.strptime(end_time_in_db, "%Y-%m-%d %H:%M:%S"))

        new_timezone = pytz.timezone(timezone_string)
        new_start_time = start_utc.astimezone(new_timezone)
        new_end_time = end_utc.astimezone(new_timezone)

        eve.start_time = new_start_time
        eve.end_time = new_end_time
        
        session.commit()
    return {'Response': f'TimeZone Changed as per {timezone_string}'}

def paginated_attendees_list(event_id, page, per_page_record):
    session = Session()
    if page < 1 or per_page_record < 1:
        return {"Response": "page and limit must be greater than 0"}

    prev_records_to_skip = (page - 1) * per_page_record

    total_attendees = session.query(Register).filter_by(event_id=event_id).count()

    attendees = session.query(Register).filter_by(event_id=event_id).offset(prev_records_to_skip).limit(per_page_record).all()

    attendee_list = [{
        "id": atd.id,
        "name": atd.name,
        "email": atd.email,
        "event_id": atd.event_id
    } for atd in attendees]

    return {
        "page": page,
        "per_page_record": per_page_record,
        "total_attendees": total_attendees,
        "attendees": attendee_list
    }
