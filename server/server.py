from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow #ModuleNotFoundError: No module named 'flask_marshmallow' = pip install flask-marshmallow https://pypi.org/project/flask-
from flask_cors import CORS, cross_origin #ModuleNotFoundError: No module named 'flask_cors' = pip install Flask-Cors
from models import db, Users

# app instance
app = Flask(__name__)
CORS(app)


app.config['SECRET_KEY'] = 'cairocoders-ednalan'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskdb.db'
# Databse configuration mysql                             Username:password@hostname/databasename
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/flaskdb' #python3 -m pip install PyMySQL https://pypi.org/project/pymysql/
                                                         
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True
   
CORS(app, supports_credentials=True)
  
db.init_app(app)
         
with app.app_context():
    db.create_all()
  
  
ma=Marshmallow(app)
  
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id','name','email','password')
   
user_schema = UserSchema()
users_schema = UserSchema(many=True)


# /api/home
@app.route("/api/home", methods=['GET'])
def return_home():
    return jsonify({
        'message': "api home method getting this message",
        'people': ['Jack', 'Harry', 'Arpan']
    })

@app.route("/")
def hello_world():
    return "<p>Hello, World!=</p>"
  
# get all users  
@app.route('/users', methods=['GET']) 
def listusers():
    all_users = Users.query.all()
    results = users_schema.dump(all_users)
    return jsonify(results)
   
#get one spcific user   
@app.route('/userdetails/<id>',methods =['GET'])
def userdetails(id):
    user = Users.query.get(id)
    return user_schema.jsonify(user)
   
#update user  
@app.route('/userupdate/<id>',methods = ['PUT'])
def userupdate(id):
    user = Users.query.get(id)   
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']
   
     # Update user attributes if present in the request JSON
    if 'name' in request.json:
        user.name = request.json['name']
    if 'email' in request.json:
        user.email = request.json['email']
    if 'password' in request.json:
        user.password = request.json['password']

    db.session.commit()
    return user_schema.jsonify(user)
  
#delete user  
@app.route('/userdelete/<id>',methods=['DELETE'])
def userdelete(id):
    user = Users.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)
 
#create new user 
@app.route('/newuser',methods=['POST'])
def newuser():
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']
   
    print(name)
    print(email)
    print(password)
  
    users = Users(name=name, email=email, password=password)
  
    db.session.add(users)
    db.session.commit()
    return user_schema.jsonify(users)


if __name__ == "__main__":
    app.run(debug=True, port=8080)



