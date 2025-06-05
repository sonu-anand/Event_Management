from event_management import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=app.config.from_object('config.Config'), port=1234)

