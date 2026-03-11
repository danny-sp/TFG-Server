CREATE DATABASE IF NOT EXISTS ev_charging_system
  CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

USE ev_charging_system;

CREATE TABLE ev_users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(100) NOT NULL,
  email VARCHAR(120) UNIQUE NOT NULL,
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
  operator VARCHAR(100),
  location POINT NOT NULL,
  SPATIAL INDEX(location)
);

CREATE TABLE services (
  id INT AUTO_INCREMENT PRIMARY KEY,
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
  location POINT NOT NULL,
  SPATIAL INDEX(location)
);

CREATE TABLE charger_types (
  id INT AUTO_INCREMENT PRIMARY KEY,
  charger_name VARCHAR(50) NOT NULL,
  max_kw_speed DECIMAL(5,2),
  description TEXT
);

CREATE TABLE chargers (
  id INT AUTO_INCREMENT PRIMARY KEY,
  charging_station_id INT NOT NULL,
  charger_type_id INT NOT NULL,
  power_kw DECIMAL(5,2) NOT NULL,
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
  charger_type_id INT NOT NULL,
  price_per_kwh DECIMAL(6,2) NOT NULL,
  begin_date DATETIME,
  end_date DATETIME,
  FOREIGN KEY (charging_station_id) REFERENCES charging_stations(id)
    ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (charger_type_id) REFERENCES charger_types(id)
    ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE bookings (
  id INT AUTO_INCREMENT PRIMARY KEY,
  vehicle_plate VARCHAR(15) NOT NULL,
  booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  start_date DATETIME NOT NULL,
  end_date DATETIME NOT NULL,
  price_rate_id INT NOT NULL,
  price DECIMAL(8,2) NOT NULL,
  status ENUM('scheduled', 'completed', 'cancelled') DEFAULT 'scheduled',
  FOREIGN KEY (vehicle_plate) REFERENCES vehicles(plate)
    ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (price_rate_id) REFERENCES price_rates(id)
    ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE charging_sessions (
  id INT AUTO_INCREMENT PRIMARY KEY,
  booking_id INT,
  charger_id INT NOT NULL,
  start_date DATETIME NOT NULL,
  end_date DATETIME,
  energy_delivered_kwh DECIMAL(6,2),
  total_cost DECIMAL(8,2),
  FOREIGN KEY (booking_id) REFERENCES bookings(id)
    ON UPDATE CASCADE ON DELETE SET NULL,
  FOREIGN KEY (charger_id) REFERENCES chargers(id)
    ON UPDATE CASCADE ON DELETE CASCADE
);

-- EXAMPLE DATA INSERTION
INSERT INTO ev_users (username, email, phone) VALUES
('John Doe', 'john.doe@example.com', '123-456-7890'),
('Jane Smith', 'jane.smith@example.com', '098-765-4321');

INSERT INTO vehicles (plate, capacity_kwh, max_kw_speed, user_id) VALUES
('ABC123', 75.00, 150.00, 1),
('XYZ789', 60.00, 120.00, 2);

-- End of SQL Script for EV Charging System Database Creation