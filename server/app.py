from sqlalchemy import DateTime, create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import func

from flask import Flask, request, jsonify, render_template


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
    author = Column(String, nullable=True)
    created = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


@app.route('/<string:page_name>/')
def static_page(page_name):
    return render_template('%s.html' % page_name)


@app.route("/matrix/api/message", methods=["POST"])
def create_message():
    data = request.get_json()
    if 'message' not in data:
        return jsonify({"error": "bad payload"}), 500
    message = data.get('message')
    author = data.get('author')

    msg = Message(message=message, author=author)

    db_session = app.Session()

    try:
        db_session.add(msg)
        db_session.commit()
        return jsonify(dict(
            data=msg.id, created=msg.created, id=msg.id, author=msg.author
        )), 201
    except IntegrityError as e:
        db_session.rollback()
        return jsonify({"error": "could not create message"}), 500
    finally:
        db_session.close()


@app.route("/matrix/api/message", methods=["GET"])
def get_messages():
    db_session = app.Session()

    # TODO add something like filter(Message.created+datetime.timedelta(days=1))>datetime.datetime.now())
    messages = db_session.query(Message).all()

    messages = [dict(id=str(m.id),
                      created=m.created.strftime("%Y-%m-%d %H:%M:%S"),
                      author=m.author,
                      message=str(m.message))
                for m in messages]
    return jsonify(dict(messages=messages)), 500


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
