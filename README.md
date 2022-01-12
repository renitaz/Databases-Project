# Databases w4111 Final Project

Patient and Clinic Portal web application built from scratch using PostgreSQL (GoogleCloud), HTML, CSS. 

General Description: The portal is both patient and client facing. New patients can create an account. Returning patients can log in (using Name  and DOB) to query their medical history, see previous and upcoming appointments, find prescribed medication, etc. Due to security concerns, patients cannot edit the inputted information. Clinic staff can log in (using Staff ID) to update appointments, prescribe medication, update medical history for patients, etc.  

**---- Highlights ----**

Main Webpages: 

>**_New Patient Page:_** form to be filled out by a new patient in order to be registered into the system and gain access to the Patient Portal. Input fields: Name, DOB, Insurance ID (optional), Medical History (optional). This information is aadded to the database via PostgreSQL commands on the backend. Patient is then redirected to Patient Portal main page to log in and verify inputted information. On the Clinic side, staff can edit this information and add medical IDs for inputted medical history information. 
>
>See file: patient_new.html


> **_Scheduling an Appointment Page:_** form to be filled out either by a patient or a staff member. The page contains a table (accessed via SQL query and reformatted on the backend) which shows doctor information: ID, Medical Licence Number, Expertise, Degrees, Job Title. An appointment for a specified date and time can be scheduled using the doctor ID selected. 
> 
> See file: scheduling_add.html


> **_Clinic Portal Main Page:_** upon logging in with Doctor ID, system grants access to this reformatted main page for Clinic Staff. Provides access to Patient and Doctor Information (Patient Files, Doctor Files, PCP Files, Patient Medications), Scheduling Information (Clinic Schedule, All Available Timeslots), and Testing and Lab Information (Testing, Patient Labs). 
>
> See file: clinic_portal.html


Interesting Queries: 

>SELECT name, medical_history, summary FROM patient AS p, after_visit_summar AS a WHERE p.patient_id = a.patient_id; 
>
> This query returns a table with patient names, their medical histories, and after visit summaries. This is useful to the Clinic doctors to determine when patients need to follow up (listed in their after visit summaries) and if they have chronic conditions or new, relevant diagnoses in their medical history. 

>SELECT a.patient_id, appointments, summary FROM after_visit_summary AS a, appointment_history AS h WHERE a.patient_id = h.patient_id ORDER BY a.patient_id; 
>
>This query returns a table with patient IDs, an array of all of their appointments, and the after visit summaries of those appointments. This is helpful for both the patients and Clinic staff to see the diagnoses, prescribed medications, and follow up information (all in the after visit summaries) for each appointment. 

>SELECT patient_id, patient_name, doc_name FROM pcp_info ORDER BY doc_id, patient_name;
>
>This query returns a table with patient ID’s, patient names, and their provider’s name. This would be helpful for the clinic and patient to be able to directly see who their provider is and how many patients are being treated by a certain provider. The table is ordered by doctor name and the patients are sorted alphabetically within each doctor.


