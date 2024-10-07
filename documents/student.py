from flask_login import login_user, logout_user, current_user, login_required
from flask import request, Blueprint, jsonify

# Local imports
from .models import Student
from . import session


student = Blueprint("students",__name__)

# update user data
@student.route('/update-student-info?/<string:user_id>',methods=['PUT','POST'])
@login_required
def update_student_info(user_id:str):

        try:
            studentData = request.get_json()

            first_name:str = studentData.get('firstName',None)
            last_name:str = studentData.get('lastName',None)
            dob:str = studentData.get('dob',None)
            phone_number:str = studentData.get('phoneNumber',None)
            education_level:str = studentData.get('educationLevel',None)
            countryOfResidence:str = studentData.get('countryResidence',None)
            countryOfInterest:str = studentData.get('countryInterest',None)
            field_of_interest:str = studentData.get('fieldInterest',None)
            user_id:str = user_id

            if request.method == 'PUT':

                #  check if the user existed to update it
                isStudent_exist= session.query(Student).filter_by(user_id=user_id).first()

                if isStudent_exist:
                    isStudent_exist.first_name = first_name
                    isStudent_exist.last_name = last_name
                    isStudent_exist.date_of_birth = dob
                    isStudent_exist.phone_number = phone_number
                    isStudent_exist.education_level = education_level
                    isStudent_exist.country_of_interest = countryOfInterest
                    isStudent_exist.country_of_residence = countryOfResidence
                    isStudent_exist.field_of_study_interest = field_of_interest
                    isStudent_exist.user_id = user_id

                    session.commit()
                    return jsonify({'message': 'Student data successfully updated','ok':True}),201
                else:
                    # Creating a new request to be advised
                    newStudent = Student(
                         first_name = first_name,
                         last_name = last_name,
                         phone_number = phone_number,
                         date_of_birth = dob,
                         education_level = education_level,
                         country_of_residence = countryOfResidence,
                         country_of_interest = countryOfInterest,
                         field_of_study_interest = field_of_interest,
                         user_id = user_id)
                    
                    session.add(newStudent)
                    session.commit()
                    return jsonify({'message': 'Student data successfully created', 'ok':True}),201
        except (KeyError, TypeError) as e:
            print(f'Error processing request data: {e}')
            return jsonify({'error:':'Invalid request data'}), 400

# delete student data
@student.route('/student-info-account-delete?/<string:delete_id>',methods=['DELETE'])
@login_required
def delete_student_record(delete_id:str):
     if request.method == 'DELETE':
          
         try:
               existed_student = session.query(Student).filter_by(id = delete_id).first()

               if existed_student:
                    session.delete(existed_student)
                    session.commit()
                    return jsonify({'message': 'student data successfully deleted'})
               else:
                    # Handle case where student doesn't exist
                    return jsonify({'error': 'Student not found'}), 404
               
         except Exception as e:
                # Handle general exceptions gracefully
                print(f"Error deleting student: {e}")
                return jsonify({'error': 'Failed to delete student'}), 500

          


