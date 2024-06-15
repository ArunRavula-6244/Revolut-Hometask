from flask import Flask, request, jsonify
import datetime
 
app = Flask(__name__)

users = {}
 
@app.route('/hello/<username>', methods=['PUT'])
def save_user_info(username):
    try:
        data = request.get_json()
        dob = datetime.datetime.strptime(data['dateOfBirth'], '%Y-%m-%d').date()
        today = datetime.date.today()
        if not username.isalpha():
            return 'Invalid username (must contain only letters)', 400
 
        if dob >= today:
            return 'Invalid date of birth (must be before today)', 400
 
        users[username] = dob
        return '', 204  # No Content
    except Exception as e:
        return str(e), 500

@app.route('/status', methods=['GET'])
def status():
    return {"status": 200}

@app.route('/hello/<username>', methods=['GET'])
def get_birthday_message(username):
    try:
        dob = users.get(username)

        if dob:
            dob_arr = str(dob).split("-")
            today_arr = str(datetime.date.today()).split("-")

            month_of_dob = dob_arr[1]
            month_of_today = today_arr[1]
            diff_days = 0

            if month_of_dob >= month_of_today:
                temp_dob = today_arr[0] + "-" + month_of_dob + "-" + dob_arr[2]
                temp_dob = datetime.datetime.strptime(temp_dob, '%Y-%m-%d').date()
                diff_days = (temp_dob - datetime.date.today()).days
            else:
                temp_dob = str(int(today_arr[0]) + 1) + "-" + month_of_dob + "-" + dob_arr[2]
                temp_dob = datetime.datetime.strptime(temp_dob, '%Y-%m-%d').date()
                diff_days = (temp_dob - datetime.date.today()).days
            
            if diff_days == 0:
                message = f'Hello, {username}! Happy birthday!'
            else:
                message = f'Hello, {username}! Your birthday is in {diff_days} day(s)'
            
            return jsonify({'message': message})
        else:
            return 'User not found', 404
        
    except Exception as e:
        return str(e), 500
 
if __name__ == '__main__':
    app.run(debug=True)