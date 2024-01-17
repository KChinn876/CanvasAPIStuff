from canvasapi import Canvas
from decouple import config

API_URL = config('API_URL')
API_KEY = config('API_KEY')
COURSE_ID = config('COURSE_ID')

canvas = Canvas(API_URL, API_KEY)

def create_attendance_sheet(course_id):
    course = canvas.get_course(course_id)
    enrollments = course.get_enrollments()

    with open('Spring2024_Attendance.csv', 'w') as f:
        f.write('Name,SIS ID,SIS Section ID\n')

    for enrollment in enrollments:
        if enrollment.type == 'StudentEnrollment':
            student_name = enrollment.user['sortable_name']
            sis_user_id = enrollment.user['sis_user_id']
            sis_section_id = enrollment.sis_section_id
            sis_section_id = str(sis_section_id)[-5:] # generally want this line uncommented
            
            # print(f'"{student_name}",{sis_user_id},{sis_section_id}\n')

            with open('Spring2024_Attendance.csv', 'a') as f:
                f.write(f'"{student_name}",{sis_user_id},{sis_section_id}\n')
    
    print('✅ Attendance sheet created successfully!')

create_attendance_sheet(COURSE_ID)
print('All Done 😴')
