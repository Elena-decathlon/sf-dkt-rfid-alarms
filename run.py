from app.app import flask_app, init_db

if __name__ == "__main__":
    init_db()
    flask_app.run(host='0.0.0.0', debug='True')
