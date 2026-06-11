DROP DATABASE IF EXISTS ev_charging_system;
CREATE DATABASE ev_charging_system
  CHARACTER SET utf8mb4 
  COLLATE utf8mb4_general_ci;

USE ev_charging_system;

CREATE TABLE ev_users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(100) NOT NULL,
  email VARCHAR(120) UNIQUE NOT NULL,
  phone VARCHAR(20),
  value_of_time DECIMAL(10,2) DEFAULT 15.00,
  active_user BOOLEAN DEFAULT TRUE,
  registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE vehicles (
  plate VARCHAR(15) PRIMARY KEY,
  consumption_wh_km DECIMAL(6,2) NOT NULL,
  capacity_kwh DECIMAL(6,2) NOT NULL,
  max_kw_speed DECIMAL(5,2) NOT NULL,
  user_id INT,
  registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES ev_users(id)
    ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE operators (
  id INT AUTO_INCREMENT PRIMARY KEY,
  operator_name VARCHAR(100) NOT NULL
);

CREATE TABLE charging_stations (
  id INT AUTO_INCREMENT PRIMARY KEY,
  station_name VARCHAR(100),
  operator_id INT,
  location POINT NOT NULL,
  SPATIAL INDEX(location),
  FOREIGN KEY (operator_id) REFERENCES operators(id)
    ON UPDATE CASCADE ON DELETE SET NULL
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

CREATE TABLE chargers (
  id INT AUTO_INCREMENT PRIMARY KEY,
  charging_station_id INT NOT NULL,
  power_kw DECIMAL(5,2) NOT NULL,
  FOREIGN KEY (charging_station_id) REFERENCES charging_stations(id)
    ON UPDATE CASCADE ON DELETE CASCADE
);
