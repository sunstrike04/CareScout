-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS illinois_hospital_data;

-- Select it as the active database
USE illinois_hospital_data;

DROP TABLE IF EXISTS illinois_hospital_insurances;
DROP TABLE IF EXISTS illinois_hospitals;
DROP TABLE IF EXISTS insurances;

CREATE TABLE illinois_hospitals (
    hospital_id INT AUTO_INCREMENT, 
    hospital_name VARCHAR(100),
    address VARCHAR(200),
    city VARCHAR(60),
    zip_code INT,
    PRIMARY KEY (hospital_id)
);

CREATE TABLE insurances (
    insurance_id INT AUTO_INCREMENT,
    insurance_name VARCHAR(100),
    PRIMARY KEY (insurance_id)
);

CREATE TABLE illinois_hospital_insurances (
    hospital_id INT,
    insurance_id INT,
    PRIMARY KEY (hospital_id, insurance_id),
    FOREIGN KEY (hospital_id) REFERENCES illinois_hospitals(hospital_id),
    FOREIGN KEY (insurance_id) REFERENCES insurances(insurance_id)
);

-- Populate illinois_hospitals table
INSERT INTO illinois_hospitals (hospital_name, address, city, zip_code) 
VALUES 
    ('Northwestern Memorial Hospital', '251 E Huron St', 'Chicago', 60611),
    ('Rush University Medical Center', '1620 W Harrison St', 'Chicago', 60612),
    ('Advocate Illinois Masonic Medical Center', '836 W Wellington Ave', 'Chicago', 60657),
    ('Carle Foundation Hospital', '611 W Park St', 'Urbana', 61801),
    ('OSF Saint Francis Medical Center', '530 NE Glen Oak Ave', 'Peoria', 61637),
    ('Memorial Medical Center', '701 N First St', 'Springfield', 62781),
    ('Advocate Good Samaritan Hospital', '3815 Highland Ave', 'Downers Grove', 60515),
    ('NorthShore University HealthSystem', '2650 Ridge Ave', 'Evanston', 60201),
    ('Edward Hospital', '801 S Washington St', 'Naperville', 60540),
    ('Loyola University Medical Center', '2160 S First Ave', 'Maywood', 60153),
    ('Silver Cross Hospital', '1900 Silver Cross Blvd', 'New Lenox', 60451),
    ('Advocate Christ Medical Center', '4440 W 95th St', 'Oak Lawn', 60453),
    ('Riverside Medical Center', '350 N Wall St', 'Kankakee', 60901),
    ('Swedish Hospital', '5145 N California Ave', 'Chicago', 60625),
    ('Decatur Memorial Hospital', '2300 N Edward St', 'Decatur', 62526);

-- Populate insurances table
INSERT INTO insurances (insurance_name)
VALUES
    ('Blue Cross Blue Shield'),
    ('UnitedHealthcare'),
    ('Aetna'),
    ('Cigna'),
    ('Humana'),
    ('Medicare'),
    ('Medicaid'),
    ('Blue Cross Blue Shield of Illinois'),
    ('Ambetter'),
    ('Health Alliance'),
    ('Molina Healthcare'),
    ('Oscar Health'),
    ('Anthem'),
    ('Kaiser Permanente');

INSERT INTO illinois_hospital_insurances (hospital_id, insurance_id) 
    VALUES
    (1, 1),  -- Northwestern Memorial Hospital accepts Blue Cross Blue Shield
    (1, 2),  -- Northwestern Memorial Hospital accepts UnitedHealthcare
    (2, 3),  -- Rush University Medical Center accepts Aetna
    (3, 6),  -- Advocate Illinois Masonic Medical Center accepts Medicare
    (4, 10),
    (5, 10),
	(5, 14),
    (6,11),
    (6,14),
    (6,9),
    (7,2),
    (7,5),
    (7,12),
    (8,1),
    (8,2),
    (9,7),
    (9,4),
    (10,12),
    (11,14),
    (13,1), 
    (13, 11), 
    (14, 12),
    (12, 1), 
    (15, 3);
    
    
    

DROP TABLE IF EXISTS illinois_hospital_full_pivot;


CREATE TABLE illinois_hospital_full_pivot AS
SELECT 
    h.hospital_id,
    h.hospital_name,
    h.address,
    h.city,
    h.zip_code,
    GROUP_CONCAT(CONCAT(i.insurance_id, ':', i.insurance_name) ORDER BY i.insurance_id SEPARATOR ', ') AS insurances
FROM illinois_hospitals h
LEFT JOIN illinois_hospital_insurances hi
    ON h.hospital_id = hi.hospital_id
LEFT JOIN insurances i
    ON hi.insurance_id = i.insurance_id
GROUP BY h.hospital_id, h.hospital_name, h.address, h.city, h.zip_code
ORDER BY h.hospital_id;


SELECT * FROM illinois_hospitals;
SELECT * FROM insurances;
SELECT * FROM illinois_hospital_insurances;
SELECT * FROM illinois_hospital_full_pivot;
