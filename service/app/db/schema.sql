CREATE DATABASE psd_status;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(128) UNIQUE NOT NULL,
  password VARCHAR(128) NOT NULL
);

CREATE TABLE protocol (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(128) UNIQUE NOT NULL
);

CREATE TABLE monitor (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  protocol_id INTEGER NOT NULL,/*FK*/
  delay INTEGER NOT NULL,
  name VARCHAR(128) UNIQUE NOT NULL,
  target VARCHAR(128) NOT NULL,
  active BOOLEAN NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP,
  CONSTRAINT FK_monitor_protocol FOREIGN KEY (protocol_id) REFERENCES protocol (id)
);

CREATE TABLE ssl_record (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  monitor_id INTEGER NOT NULL,/*FK*/
  success BOOLEAN NOT NULL,
  authority VARCHAR(128),
  expiry_date TIMESTAMP,
  created_at TIMESTAMP,
  CONSTRAINT FK_ssl_record_monitor FOREIGN KEY (monitor_id) REFERENCES monitor (id)
);

CREATE TABLE http_record (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  monitor_id INTEGER NOT NULL,/*FK*/
  response_time FLOAT,
  status_code INTEGER,
  errors VARCHAR(128),
  created_at TIMESTAMP NOT NULL,
  CONSTRAINT FK_http_record_monitor FOREIGN KEY (monitor_id) REFERENCES monitor (id)
);
