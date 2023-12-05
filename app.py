from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///demo.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Base(DeclarativeBase):
    pass

class Person(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(db.String)
    surname: Mapped[str] = mapped_column(db.String)
    job: Mapped[str] = mapped_column(db.String)


class PersonSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Person


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/persons', methods=['GET'])
def get_persons():
    persons = Person.query.all()
    person_schema = PersonSchema(many=True)
    result = person_schema.dump(persons)
    return jsonify(result)


@app.route('/person/<int:id>', methods=['GET'])
def get_person(id):
    person = Person.query.get_or_404(id)
    person_schema = PersonSchema()
    result = person_schema.dump(person)
    return jsonify(result)


@app.route('/person/create', methods=['POST'])
def create_person():
    data = request.json
    person_schema = PersonSchema()

    new_person = Person(
        name=data.get('name'),
        surname=data.get('surname'),
        job=data.get('job')
    )

    db.session.add(new_person)
    db.session.commit()

    result = person_schema.dump(new_person)
    return jsonify(result), 201


if __name__ == '__main__':
    app.run()
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.add(Person(name="ser", surname="serowy", job='it'))
        db.session.commit()
        # db.session.execute(db.select(Person)).scalars()
        # db.get_or_404(Person, id)


