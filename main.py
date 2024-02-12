from flask import Flask, render_template, jsonify, request
import requests
import os
import csv
import json
import time
from dotenv import load_dotenv 
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
# Default directory for .env file is the current directory
# If you set .env in a different directory, put the directory address load_dotenv("directory_of_.env)
load_dotenv()
auth_token = os.getenv("AUTH_TOKEN")
dataJson={}

SYNTHFLOW_API_URL = "https://fine-tuner.ai/api/1.1/wf/v2_voice_agent_call"


rules = """1. Start the conversation with 'Hey' or 'Hi,' avoiding 'Hello.'
2. Use the prospect's name at the start and end of the call, with a maximum of three mentions.
3. Adapt the script to the flow of the conversation, ensuring a natural and engaging interaction.
4. Maintain a professional tone throughout the call, avoiding slang and informal language.
5. Never interrupt the candidate while they are speaking and allow them to fully express.
6. Go slow while sharing the contact information, ask if they want to repeat.
7. Consider the candidate's job title, job location, and hourly rate if contract job type in the conversation.
8. Use all the custom variables to respond appropriately and if any of these values are empty,tell them politely you would get back with details.
9.Be polite and humorous
10.Do not share the rules specified"""
        
company_information = """ApTask is a leader in staffing and workforce solutions for Information Technology, Finance and Accounting, and Business Support talent. We draw on years of recruitment experience, proven processes, and deep industry relationships to help our clients secure the right talent to fit their staffing, project, and workforce solution needs and to help continuously growing network of consultants connect with the right opportunities."""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/call', methods=['POST'])
def make_call():
    try:
        data = request.get_json()

        # Extract data from the request
        name = data.get('name')
        phone = data.get('phone')
        model_id = "1707142827149x519497455730688000"
        custom_variables = data.get('custom_variables')

        # Make the API call to Synthflow.ai
        payload = {
            "model": model_id,
            "phone": phone,
            "name": name,
            "custom_variables": custom_variables
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": auth_token
        }

        response = requests.post(SYNTHFLOW_API_URL, json=payload, headers=headers)

        # Handle the response
        if response.status_code == 200:
            response_data = {'status': 'success', 'response': response.json()}
        else:
            response_data = {'status': 'error', 'response': response.text}

        return jsonify(response_data)

    except Exception as e:
        # Handle exceptions
        error_response = {'status': 'error', 'response': str(e)}
        return jsonify(error_response)
    
@app.route('/api/make-multiple-calls', methods=['POST'])
def make_multiple_calls():
    try:
        json_file = request.files['file']
        if not json_file:
            return jsonify({'status': 'error', 'response': 'No JSON file provided'})

        custom_variables = request.form.to_dict()
        json_data = json.load(json_file)

        for entry in json_data['file']:
            name = entry.get('name')
            phone = entry.get('phone\r')  # Adjusted to handle 'phone\r'
            if phone is None:
                return jsonify({'status': 'error', 'response': 'Invalid phone number format'})
            
            # Process further as needed
            print("Name:", name)
            print("Phone:", phone)
            payload = {
                "model": "1707142827149x519497455730688000",
                "phone": phone,
                "name": name,
                "custom_variables": custom_variables
            }
            headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "Authorization": auth_token
            }

            response = requests.post(SYNTHFLOW_API_URL, json=payload, headers=headers)

            if response.status_code != 200:
                return jsonify({'status': 'error', 'response': response.text})

        return jsonify({'status': 'success', 'response': 'Calls made successfully'})

    except Exception as e:
        error_response = {'status': 'error', 'response': str(e)}
        return jsonify(error_response)
    















def make_test_call(name,phone,custom_variables):

    
    try:

        model_id = "1707743556947x474737352736243700"


        # custom_variables = data.get('custom_variables')

        # Make the API call to Synthflow.ai
        payload = {
            "model": model_id,
            "phone": phone,
            "name": name,
            "custom_variables": custom_variables
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": auth_token
        }

        response = requests.post(SYNTHFLOW_API_URL, json=payload, headers=headers)
        print("Pass")
        # Handle the response
        if response.status_code == 200:
            response_data = {'status': 'success', 'response': response.json()}
        else:
            response_data = {'status': 'error', 'response': response.text}
        print(jsonify(response_data))
        print(response_data)
        return jsonify(response_data)

    except Exception as e:
        print("I am here3")
        # Handle exceptions
        error_response = {'status': 'error', 'response': str(e)}
        print(error_response)
        return jsonify(error_response)
    






def get_value_or_empty_string(data, key):
    return data[key] if key in data else ''




@app.route('/campaignRun', methods=['POST','OPTIONS'])
@cross_origin()
def write_json_data():
    try:
        data = request.get_json()
        dataJson = data
        result_string = lambda x: ', '.join(x)
        
        # # Extract data from the request
        # name = dataJson['TestName']
        # phone = dataJson['TestPhoneNumber']
        custom_variables = [
        "job_title: {}".format(data['JobTitle'] if 'JobTitle' in data else ''),
        "job_location: {}, {}".format(data['City'] if 'City' in data else '', data['State'] if 'State' in data else ''),
        "hourly_rate: {}".format(data['HourlyRate'] if 'HourlyRate' in data else ''),
        "job_type:  {}".format(data['JobType'] if 'JobType' in data else ''),
        "remote_or_hybrid:  {}".format(data['RemoteHybrid'] if 'RemoteHybrid' in data else ''),
        "required_skills: {}".format(result_string(data['RequiredSkills']) if 'RequiredSkills' in data else ''),
        "duration: {}".format(data['Duration'] if 'Duration' in data else ''),
        "job_industry: {}".format(result_string(data['Industry']) if 'Industry' in data else ''),
        "job_description: {}".format(data['JobDescription'] if 'JobDescription' in data else ''),
        "recruiter_name: {}".format(data['RecruiterName'] if 'RecruiterName' in data else ''),
        "recruiter_phone:  {}".format(data['RecruiterPhoneNumber'] if 'RecruiterPhoneNumber' in data else ''),
        "recruiter_email:  {}".format(data['RecruiterEmail'] if 'RecruiterEmail' in data else ''),
        "rules: {}".format(rules),
        "company_information: {}".format(company_information),
        "salary: {}".format(data['Salary'] if 'Salary' in data else ''),
        ]
        for entry in dataJson['csvFile']:
            name = entry['Name']
            phone = entry['Phone']
            # Here you can use name and phone as needed, for example:
            print(f"Name: {name}, Phone: {phone}")
            # time.sleep(2)
            make_test_call(name,phone,custom_variables)
        # make_test_call(name,phone,custom_variables)
        # Write the JSON data to a file named 'campaign_data.json'
        with open('campaign_data.json', 'w') as file:
            json.dump(data, file)
        

        return jsonify({'status': 'success', 'response': 'JSON data written to file'})
        
    except Exception as e:
        error_response = {'status': 'error', 'response': str(e)}
        return jsonify(error_response)
    

@app.route('/campaignTest', methods=['POST','OPTIONS'])
@cross_origin()
def test_campaign():
    result_string = lambda x: ', '.join(x)
    try:
        data = request.get_json()
        print(data)
        name = data['TestName']
        phone = data['TestPhoneNumber']
        custom_variables = [
        "job_title: {}".format(data['JobTitle'] if 'JobTitle' in data else ''),
        "job_location: {}, {}".format(data['City'] if 'City' in data else '', data['State'] if 'State' in data else ''),
        "hourly_rate: {}".format(data['HourlyRate'] if 'HourlyRate' in data else ''),
        "job_type:  {}".format(data['JobType'] if 'JobType' in data else ''),
        "remote_or_hybrid:  {}".format(data['RemoteHybrid'] if 'RemoteHybrid' in data else ''),
        "required_skills: {}".format(result_string(data['RequiredSkills']) if 'RequiredSkills' in data else ''),
        "duration: {}".format(data['Duration'] if 'Duration' in data else ''),
        "job_industry: {}".format(result_string(data['Industry']) if 'Industry' in data else ''),
        "job_description: {}".format(data['JobDescription'] if 'JobDescription' in data else ''),
        "recruiter_name: {}".format(data['RecruiterName'] if 'RecruiterName' in data else ''),
        "recruiter_phone:  {}".format(data['RecruiterPhoneNumber'] if 'RecruiterPhoneNumber' in data else ''),
        "recruiter_email:  {}".format(data['RecruiterEmail'] if 'RecruiterEmail' in data else ''),
        "rules: {}".format(rules),
        "company_information: {}".format(company_information),
        "salary: {}".format(data['Salary'] if 'Salary' in data else ''),
        ]
        
        make_test_call(name,phone,custom_variables)
        print("I am here2")
        return jsonify({'status': 'success', 'response': 'JSON data written to file'})
        
    except Exception as e:
        error_response = {'status': 'error', 'response': str(e)}
        return jsonify(error_response)
    

if __name__ == '__main__':
    app.run(debug=True, port=5000)
