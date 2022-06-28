# Hostel Management API

## User

- username
- full_name
- phone
- role(Admin,Student)
- is_active
- is_admin
- is_staff
- timestamp

## Profile

- user(User)
- bio
- profile_picture
- id_no(national Id)
- nationality
- town
- estate
- gender
- date_of_birth
- timestamp

## Administrator

- job_id_no
- available

## Student

- admission_no
- course(Course)
- year enrolled

## Course

- course_name
- code
- duration
- academic_year
- start_year
- completion_year

## Hostel

- name
- gender
- care_taker

## Rooms

- room_name
- room_type
- no_of_spaces
- hostel(Hostel)

## Spaces

- room
- space name
- vacant
- price

## Book Hostel

- space
- student
- admin
- checkin_date
- checkout_date
- paid
- accepted

## Todo's

- Students and Administrators can register (Done)
- Account Activation can take place (Done)
- Students and Administrators can login (Done)
- Students and Administrator can view and update their profiles (Done)
- Password Reset can take place (Done)
- Administrator can view all students and Administrators and can update their details
- Administrators can create hostel
- Administrator can create room
- Administrator can create space
- Administrator can book for students
- Students can book hostel and view the hostel that they have booked
