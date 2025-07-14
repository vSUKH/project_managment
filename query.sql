create database project_managment;
CREATE TABLE projects (
  project_id INT(10) NOT NULL,
  project VARCHAR(100) NOT NULL,
  location VARCHAR(100) NOT NULL,
  overall_cost VARCHAR(10) NOT NULL,
  start_date DATE NOT NULL,
  deadline DATE NOT NULL,  
  tid INT(10) NOT NULL,
  proposed_project INT(5) NOT NULL,
  date_added DATE NOT NULL
);


select * from projects;



INSERT INTO projects (
  project_id, project, location, overall_cost,
  start_date, deadline, tid, proposed_project, date_added
) VALUES
(1, 'Solar Power Plant', 'Rajasthan', '2500000', '2024-01-10', '2025-01-10', 101, 1, '2024-01-05'),

(2, 'Smart Irrigation System', 'Punjab', '1200000', '2024-02-15', '2024-10-15', 102, 1, '2024-02-01'),

(3, 'Highway Expansion', 'Uttar Pradesh', '8000000', '2024-03-01', '2025-06-30', 103, 0, '2024-02-25'),

(4, 'AI Traffic Management', 'Delhi', '3500000', '2024-04-10', '2025-01-31', 104, 1, '2024-03-15'),

(5, 'Rainwater Harvesting', 'Karnataka', '950000', '2024-05-05', '2024-11-05', 105, 0, '2024-04-20');


CREATE TABLE employee (
  eid INT(10) NOT NULL,
  lastname VARCHAR(50) NOT NULL,
  firstname VARCHAR(50) NOT NULL,
  bday DATE NOT NULL,
  contact_no VARCHAR(15) NOT NULL,
  address VARCHAR(100) NOT NULL,
  pid INT(10) NOT NULL,
  statuss VARCHAR(30) NOT NULL,
  gender VARCHAR(10) NOT NULL,  
  date_added DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

select * from employee;

INSERT INTO employee (
  eid, lastname, firstname, bday, contact_no,
  address, pid, statuss, gender, date_added
) VALUES
(1, 'Sharma', 'Ravi', '1990-05-12', '9876543210', 'Delhi', 1, 'Active', 'Male', CURDATE()),

(2, 'Kaur', 'Simran', '1995-08-22', '9123456789', 'Amritsar', 2, 'On Leave', 'Female', CURDATE()),

(3, 'Patel', 'Amit', '1988-03-03', '9988776655', 'Ahmedabad', 3, 'Active', 'Male', CURDATE()),

(4, 'Reddy', 'Sneha', '1993-11-30', '9012345678', 'Hyderabad', 4, 'Inactive', 'Female', CURDATE()),

(5, 'Mehta', 'Karan', '1992-01-17', '7894561230', 'Mumbai', 5, 'Active', 'Male', CURDATE());


CREATE TABLE tasks (
    project_id INT(15) NOT NULL,
    task_id VARCHAR(20) NOT NULL,
    descriptions VARCHAR(250) NOT NULL,
    statuss INT(1) NOT NULL,
    estimate_days INT(2) NOT NULL
);

