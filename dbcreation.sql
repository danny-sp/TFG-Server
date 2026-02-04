CREATE DATABASE IF NOT EXISTS ev_charging_system
  CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

USE ev_charging_system;

CREATE TABLE ev_users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_name VARCHAR(100) NOT NULL,
  email VARCHAR(120) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  phone VARCHAR(20),
  active_user BOOLEAN DEFAULT TRUE,
  registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE vehicles (
  plate VARCHAR(15) PRIMARY KEY,
  capacity_kwh DECIMAL(6,2) NOT NULL,
  max_kw_speed DECIMAL(5,2) NOT NULL,
  user_id INT,
  registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES ev_users(id)
    ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE charging_stations (
  id INT AUTO_INCREMENT PRIMARY KEY,
  station_name VARCHAR(100),
  latitude DECIMAL(9,6) NOT NULL,
  longitude DECIMAL(9,6) NOT NULL,
  open_time TIME,
  close_time TIME
);

CREATE TABLE services (
  id INT AUTO_INCREMENT PRIMARY KEY,
  charging_station_id INT NOT NULL,
  service_name VARCHAR(150) NOT NULL,
  service_type ENUM(
    'cafe',
    'restaurant',
    'motel',
    'mechanic',
    'supermarket',
    'atm',
    'pharmacy'
  ) NOT NULL,
  open_time TIME,
  close_time TIME,
  FOREIGN KEY (charging_station_id) REFERENCES charging_stations(id)
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE charger_types (
  id INT AUTO_INCREMENT PRIMARY KEY,
  charger_name VARCHAR(50) NOT NULL,
  max_kw_speed DECIMAL(5,2),
  description TEXT
);

CREATE TABLE single_chargers (
  id INT AUTO_INCREMENT PRIMARY KEY,
  charging_station_id INT NOT NULL,
  charger_type_id INT NOT NULL,
  charger_busy BOOLEAN DEFAULT FALSE,
  charger_active BOOLEAN DEFAULT TRUE,
  FOREIGN KEY (charging_station_id) REFERENCES charging_stations(id)
    ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (charger_type_id) REFERENCES charger_types(id)
    ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE price_rates (
  id INT AUTO_INCREMENT PRIMARY KEY,
  charging_station_id INT NOT NULL,
  charger_id INT NOT NULL,
  price_per_kwh DECIMAL(6,2) NOT NULL,
  begin_time TIME,
  end_time TIME,
  FOREIGN KEY (charging_station_id) REFERENCES charging_stations(id)
    ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (charger_id) REFERENCES charger_types(id)
    ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE bookings (
  id INT AUTO_INCREMENT PRIMARY KEY,
  vehicle_plate VARCHAR(15) NOT NULL,
  booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  booking_start DATETIME NOT NULL,
  booking_end DATETIME NOT NULL,
  price_rate_id INT NOT NULL,
  price DECIMAL(8,2) NOT NULL,
  booking_status ENUM('scheduled', 'completed', 'cancelled') DEFAULT 'scheduled',
  FOREIGN KEY (vehicle_plate) REFERENCES vehicles(plate)
    ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (price_rate_id) REFERENCES price_rates(id)
    ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE charging_sessions (
  id INT AUTO_INCREMENT PRIMARY KEY,
  booking_id INT,
  charger_id INT NOT NULL,
  session_start DATETIME NOT NULL,
  session_end DATETIME,
  energy_delivered_kwh DECIMAL(6,2),
  total_cost DECIMAL(8,2),
  FOREIGN KEY (booking_id) REFERENCES bookings(id)
    ON UPDATE CASCADE ON DELETE SET NULL,
  FOREIGN KEY (charger_id) REFERENCES single_chargers(id)
    ON UPDATE CASCADE ON DELETE CASCADE
);

-- EXAMPLE DATA INSERTION
INSERT INTO ev_users (user_name, email, password_hash, phone) VALUES
('John Doe', 'john.doe@example.com', 'hashed_password', '123-456-7890'),
('Jane Smith', 'jane.smith@example.com', 'hashed_password', '098-765-4321');

INSERT INTO vehicles (plate, capacity_kwh, max_kw_speed, user_id) VALUES
('ABC123', 75.00, 150.00, 1),
('XYZ789', 60.00, 120.00, 2);

INSERT INTO charging_stations (station_name, latitude, longitude, open_time, close_time) VALUES
('Luz del tajo toledo', 39.857591, -4.020744, '06:00:00', '22:00:00'),
('Islazul Madrid', 40.364541, -3.736241, '00:00:00', '23:59:59');

INSERT INTO charger_types (charger_name, max_kw_speed, description) VALUES
('Level 2 Charger', 7.2, 'Standard Level 2 AC charger'),
('DC Fast Charger', 50.0, 'High-speed DC fast charger');

INSERT INTO single_chargers (charging_station_id, charger_type_id, charger_busy, charger_active) VALUES
(1, 1, FALSE, TRUE),
(1, 2, FALSE, TRUE),
(2, 1, FALSE, TRUE);

INSERT INTO price_rates (charging_station_id, charger_id, price_per_kwh, begin_time, end_time) VALUES
(1, 1, 0.20, '00:00:00', '23:59:59'),
(1, 2, 0.30, '00:00:00', '23:59:59'),
(2, 1, 0.25, '00:00:00', '23:59:59');

INSERT INTO bookings (vehicle_plate, booking_start, booking_end, price_rate_id, price, booking_status) VALUES
('ABC123', '2024-07-01 10:00:00', '2024-07-01 12:00:00', 1, 14.40, 'scheduled'),
('XYZ789', '2024-07-02 14:00:00', '2024-07-02 16:00:00', 2, 18.00, 'scheduled');

INSERT INTO charging_sessions (booking_id, charger_id, session_start, session_end, energy_delivered_kwh, total_cost) VALUES
(1, 1, '2024-07-01 10:00:00', '2024-07-01 12:00:00', 72.00, 14.40),
(2, 2, '2024-07-02 14:00:00', '2024-07-02 16:00:00', 60.00, 18.00);

-- End of SQL Script for EV Charging System Database Creation