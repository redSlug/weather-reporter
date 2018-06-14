from sqlalchemy import DateTime, create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import func
import datetime

from flask import Flask, request, jsonify


app = Flask(__name__)
app.debug = True
prod_engine = create_engine('postgresql://user:pass@localhost:5432/prod', convert_unicode=True)
Session = sessionmaker()
app.Session = Session
Session.configure(bind=prod_engine)

Base = declarative_base()


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    message = Column(String, nullable=False)
    created = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


@app.route("/api/message", methods=["POST"])
def create_message():
    data = request.get_json()
    message = data.get('message')

    msg = Message(message=message)

    db_session = app.Session()

    try:
        db_session.add(msg)
        db_session.commit()
        return jsonify(dict(
            data=msg.id, created=msg.created, id=msg.id
        )), 201
    except IntegrityError as e:
        db_session.rollback()
        return jsonify({"error": "could not create message"}), 500
    finally:
        db_session.close()

@app.route("/api/message", methods=["GET"])
def get_messages():
    db_session = app.Session()

    # TODO add something like filter(Message.created+datetime.timedelta(days=1))>datetime.datetime.now())
    messages = db_session.query(Message).all()

    messages = [dict(id=str(m.id),
                      created=m.created.strftime("%Y-%m-%d %H:%M:%S"),
                      message=str(m.message)) for m in messages]
    return jsonify(dict(messages=messages)), 500


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
