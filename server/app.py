from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET','POST'])
def messages():
    #use list comprehensions
    #removed GET to check if TESTS will pass

    # if request.method== 'GET':
        
    #     messages = Message.query.all()
    #     messages_list=[message.to_dict() for message in messages]
           
    #     response=make_response(jsonify(messages_list), 200)
           
    #     return response
        
    # elif  request.method=='POST':
          new_message=Message(
            body = request.form.get("body")
            # username = request.form.get("username")
         )    
          db.session.add(new_message)
          db.session.commit()

          message_dict=new_message.to_dict()
          response=make_response(jsonify(message_dict), 201)
          
          return response

# list comprehenshion method
#PATCH , DELETE

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    if request.method == 'PATCH':

       message=Message.query.get(id)
       if not message:
           return make_response(jsonify({"error": "Message not found"}), 404)
    
       message.body = request.json.get("body", message.body)
       db.session.commit()
       updated_message = Message.query.get(id)
       return make_response(jsonify(updated_message.to_dict()), 200)

    elif request.method == 'DELETE':
        message = Message.query.get(id)

        db.session.delete(message)
        db.session.commit()
        return make_response("", 204)
    
    return make_response('', 204)

if __name__ == '__main__':
    app.run(port=5555)
