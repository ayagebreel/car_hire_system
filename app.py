from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/car_hire'
db = SQLAlchemy(app)

class GenderType(enum.Enum):
    APPLE = "Male"
    BANANA = "Female"

# Model
class Customer(db.Model):
   __tablename__ = "todos"
   id = db.Column(db.Integer, primary_key=True)
   Name = db.Column(db.String(20))
   Email = db.Column(db.String(50))
   Phone = db.Column(db.Integer, maximum=11)
   NationalID = db.Column(db.Integer, maximum=14)
   Gender = db.Column(enum.Enum(GenderType))

   def create(self):
       db.session.add(self)
       db.session.commit()
       return self

   def __init__(self, title, todo_description):
       self.Name= Name
       self.Email = Email

   # def __repr__(self):
   #     return f"{self.id}"

db.create_all()

class Car_HireSchema(ModelSchema):
   class Meta(ModelSchema.Meta):
       model = Customer
       sqla_session = db.session
   id = fields.Number(dump_only=True)
   Name = fields.String(required=True)
   Email = fields.String(required=True)
   Phone = fields.Integer(required=True)
   NationalID = fields.Integer(required=True)
   Gender = fields.enum(required=True)

@app.route('/api/v1/customer', methods=['POST'])
def create_todo():
   data = request.get_json()
   Car_Hire_schema = Car_HireSchema()
   car_hire = Car_Hire_schema.load(data)
   result = Car_Hire_schema.dump(car_hire.create())
   return make_response(jsonify({"Car_Hire": result}), 200)

@app.route('/api/v1/customer', methods=['GET'])
def index():
   get_customers = Customer.query.all()
   Car_Hire_schema = Car_HireSchema(many=True)
   customers = Car_Hire_schema.dump(get_customers)
   return make_response(jsonify({"customers": customers}))

@app.route('/api/v1/customer/<id>', methods=['GET'])
def get_customer_by_id(id):
   get_customer = Customer.query.get(id)
   Car_Hire_schema = Car_HireSchema()
   customer = Car_Hire_schema.dump(get_customer)
   return make_response(jsonify({"customer": customer}))

@app.route('/api/v1/customer/<id>', methods=['PUT'])
def update_customer_by_id(id):
   data = request.get_json()
   get_customer = Customer.query.get(id)
   if data.get('Name'):
       get_customer.Name = data['Name']
   if data.get('Email'):
       get_customer.todo_description = data['Email']
   if data.get('Phone'):
       get_customer.todo_description = data['Phone']
   if data.get('NationalID'):
       get_customer.todo_description = data['NationalID']
   if data.get('Gender'):
       get_customer.todo_description = data['Gender']
   db.session.add(get_customer)
   db.session.commit()
   Car_Hire_schema = Car_HireSchema(only=['id', 'title', 'todo_description'])
   customer = Car_Hire_schema.dump(get_customer)

   return make_response(jsonify({"customer": customer}))

@app.route('/api/v1/customer/<id>', methods=['DELETE'])
def delete_customer_by_id(id):
   get_customer = Customer.query.get(id)
   db.session.delete(get_customer)
   db.session.commit()
   return make_response("", 204)
