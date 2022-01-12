/* Create table statements for full database
- updated with doc_login table 
- updated with patient_login table
*/

CREATE TABLE patient (
    patient_id VARCHAR(10) NOT NULL,
    name VARCHAR(25) NOT NULL, 
    dob DATE NOT NULL, 
    insurance VARCHAR(30), 
    medical_history TEXT, 
    is_guardian BOOLEAN, 
    diagnoses TEXT
    PRIMARY KEY (patient_id)
); 


CREATE TABLE doctor (
    doc_id VARCHAR(10) NOT NULL,
    license_num VARCHAR(9) NOT NULL,
    job_title VARCHAR(20) NOT NULL, 
    date_hired DATE NOT NULL, 
    degrees VARCHAR(10) NOT NULL, 
    expertise TEXT, 
    doc_name VARCHAR(25), 
    PRIMARY KEY (doc_id, license_num)
); 

CREATE TABLE exam_room (
    room_num INT NOT NULL,
    location VARCHAR(15) NOT NULL, 
    PRIMARY KEY (room_num)
    CHECK (room_num > 0)
); 

CREATE TABLE timeslot (
    date_appt DATE NOT NULL, 
    start_time DATETIME NOT NULL, 
    end_time DATETIME, 
    PRIMARY KEY (date_appt, start_time)
); 

CREATE TABLE medication (
    med_id VARCHAR (15) NOT NULL, 
    license_num VARCHAR(9), 
    pharmacy_addr VARCHAR(100) NOT NULL, 
    refills_num INT, 
    type_ VARCHAR(20), 
    is_prescription BOOLEAN, 
    doc_id VARCHAR(10), 
    p_name VARCHAR(30), 
    PRIMARY KEY (med_id), 
    FOREIGN KEY (doc_id, license_num) REFERENCES doctor(doc_id, license_num)
    CHECK (refills_num >= 0)
); 

CREATE TABLE testing (
    test_id VARCHAR(15) NOT NULL, 
    doc_id VARCHAR(10), 
    license_num VARCHAR(9), 
    lab_reports TEXT,
    shots_given VARCHAR(200), 
    PRIMARY KEY (test_id)
    FOREIGN KEY (doc_id, license_num) REFERENCES doctor(doc_id, license_num)
); 

CREATE TABLE pcp (
    patient_id VARCHAR(10) NOT NULL, 
    doc_id VARCHAR(10) NOT NULL, 
    license_num VARCHAR(9) NOT NULL,
    PRIMARY KEY (patient_id, doc_id, license_num)
); 

CREATE TABLE schedule (
    patient_id VARCHAR(10) NOT NULL, 
    doc_id VARCHAR(10) NOT NULL, 
    license_num VARCHAR(9) NOT NULL, 
    date_appt DATE NOT NULL, 
    start_time DATETIME NOT NULL, 
    room_num INT NOT NULL, 
    PRIMARY KEY (patient_id, doc_id, license_num, date_appt, start_time, room_num)
); 

CREATE TABLE views (
    patient_id VARCHAR(10) NOT NULL, 
    med_id VARCHAR(15) NOT NULL, 
    license_num VARCHAR(9), 
    doc_id VARCHAR(10), 
    test_id VARCHAR(15) NOT NULL, 
    PRIMARY KEY (patient_id, med_id, test_id), 
    FOREIGN KEY (doc_id, license_num) REFERENCES doctor(doc_id, license_num)
); 

CREATE TABLE doc_login (
    login_id INT
); 

DROP TABLE IF EXISTS patient_login;
CREATE TABLE patient_login (
    name VARCHAR(20) NOT NULL, 
    dob DATE NOT NULL, 
); 


