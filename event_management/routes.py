from flask import jsonify, request
from .controller import create_event, get_all_events, register_attendee, get_attendees, change_timezone, paginated_attendees_list


def register_routes(app):
    @app.route('/events', methods=['GET','POST'])
    def events():
        if request.method == "POST":
            data = request.json
            result = create_event(data)
            return jsonify(result)
        else:
            events = get_all_events()
            return jsonify({'List of Upcoming Events': events})
    
    @app.route('/events/<int:event_id>/attendees', methods=['GET','POST'])
    def attendees(event_id):
        if request.method == "POST":
            data = request.json
            result = register_attendee(event_id, data)
            return jsonify(result)
        else:
            attendees = get_attendees(event_id)
            return jsonify({"Response": attendees})
    
    @app.route('/change_timezone', methods=['GET'])
    def change_tz():
        data = request.json
        result = change_timezone(data)
        return jsonify(result)
    
    @app.route('/events/<int:event_id>/attendees/page/<int:page>/per_page_record/<int:per_page_record>', methods=['GET'])
    def paginated_attendees(event_id, page, per_page_record):
        result = paginated_attendees_list(event_id, page, per_page_record)
        return jsonify(result)