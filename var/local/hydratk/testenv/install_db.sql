CREATE TABLE customer (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR NOT NULL,
  status INTEGER NOT NULL,
  segment INTEGER NOT NULL,
  birth_no VARCHAR,
  reg_no VARCHAR,
  tax_no VARCHAR,
  create_date DATETIME,
  modify_date DATETIME,
  FOREIGN KEY (status) REFERENCES lov_status(id),
  FOREIGN KEY (segment) REFERENCES lov_segment(id)
);

CREATE TABLE payer (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR NOT NULL,
  status INTEGER NOT NULL,
  billcycle INTEGER NOT NULL,
  bank_account VARCHAR,
  customer INTEGER NOT NULL,
  create_date DATETIME,
  modify_date DATETIME,
  FOREIGN KEY (status) REFERENCES lov_status(id),
  FOREIGN KEY (billcycle) REFERENCES lov_billcycle(id),
  FOREIGN KEY (customer) REFERENCES customer(id)
);

CREATE TABLE subscriber (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR NOT NULL,
  msisdn VARCHAR NOT NULL,
  status INTEGER NOT NULL,
  market INTEGER NOT NULL,
  tariff INTEGER NOT NULL,
  customer INTEGER NOT NULL,
  payer INTEGER NOT NULL,
  create_date DATETIME,
  modify_date DATETIME,
  FOREIGN KEY (status) REFERENCES lov_status(id),
  FOREIGN KEY (market) REFERENCES lov_market(id),
  FOREIGN KEY (tariff) REFERENCES lov_tariff(id),
  FOREIGN KEY (customer) REFERENCES customer(id),
  FOREIGN KEY (payer) REFERENCES payer(id)
);

CREATE TABLE contact (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR NOT NULL,
  phone VARCHAR,
  email VARCHAR,
  create_date DATETIME,
  modify_date DATETIME
);

CREATE TABLE contact_role (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  contact_role INTEGER NOT NULL,
  contact INTEGER NOT NULL,
  customer INTEGER,
  payer INTEGER,
  subscriber INTEGER,
  create_date DATETIME,
  FOREIGN KEY (contact_role) REFERENCES lov_contact_role(id),
  FOREIGN KEY (contact) REFERENCES contact(id),
  FOREIGN KEY (customer) REFERENCES customer(id),
  FOREIGN KEY (payer) REFERENCES payer(id),
  FOREIGN KEY (subscriber) REFERENCES subscriber(id)
);

CREATE TABLE address (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  street VARCHAR NOT NULL,
  street_no VARCHAR NOT NULL,
  city VARCHAR NOT NULL,
  zip VARCHAR NOT NULL,
  create_date DATETIME,
  modify_date DATETIME
);

CREATE TABLE address_role (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  address_role INTEGER NOT NULL,
  address INTEGER NOT NULL,
  contact INTEGER,
  customer INTEGER,
  payer INTEGER,
  subscriber INTEGER,
  create_date DATETIME,
  FOREIGN KEY (address_role) REFERENCES lov_address_role(id),
  FOREIGN KEY (address) REFERENCES address(id),
  FOREIGN KEY (contact) REFERENCES contact(id),
  FOREIGN KEY (customer) REFERENCES customer(id),
  FOREIGN KEY (payer) REFERENCES payer(id),
  FOREIGN KEY (subscriber) REFERENCES subscriber(id)
);

CREATE TABLE service (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  service INTEGER NOT NULL,
  status INTEGER NOT NULL,
  customer INTEGER,
  payer INTEGER,
  subscriber INTEGER,
  create_date DATETIME,
  modify_date DATETIME,
  FOREIGN KEY (service) REFERENCES lov_service(id),
  FOREIGN KEY (status) REFERENCES lov_status(id),
  FOREIGN KEY (customer) REFERENCES customer(id),
  FOREIGN KEY (payer) REFERENCES payer(id),
  FOREIGN KEY (subscriber) REFERENCES subscriber(id)
);

CREATE TABLE service_params (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  param INTEGER NOT NULL,
  value VARCHAR,
  service INTEGER NOT NULL,
  create_date DATETIME,
  modify_date DATETIME,
  FOREIGN KEY (param) REFERENCES lov_service_param(id),
  FOREIGN KEY (service) REFERENCES service(id)
);

CREATE TABLE history (
  id INTEGER PRIMARY KEY AUTOINCREMENT, 
  event_date DATETIME NOT NULL,
  table_name VARCHAR NOT NULL,
  table_id INTEGER NOT NULL,
  event VARCHAR NOT NULL,
  log CLOB
);

CREATE TABLE lov_status (
  id INTEGER PRIMARY KEY,
  title VARCHAR NOT NULL
);

CREATE TABLE lov_segment (
  id INTEGER PRIMARY KEY,
  title VARCHAR NOT NULL
);

CREATE TABLE lov_billcycle (
  id INTEGER PRIMARY KEY,
  title VARCHAR NOT NULL
);

CREATE TABLE lov_market (
  id INTEGER PRIMARY KEY,
  title VARCHAR NOT NULL
);

CREATE TABLE lov_tariff (
  id INTEGER PRIMARY KEY,
  title VARCHAR NOT NULL,
  segment INTEGER,
  market INTEGER,
  monthly_fee INTEGER
);

CREATE TABLE lov_contact_role (
  id INTEGER PRIMARY KEY,
  title VARCHAR NOT NULL
);

CREATE TABLE lov_address_role (
  id INTEGER PRIMARY KEY,
  title VARCHAR NOT NULL
);

CREATE TABLE lov_service (
  id INTEGER PRIMARY KEY,
  title VARCHAR NOT NULL,
  monthly_fee INTEGER,
  customer INTEGER,
  payer INTEGER,
  subscriber INTEGER
);

CREATE TABLE lov_service_param (
  id INTEGER PRIMARY KEY,
  title VARCHAR NOT NULL,
  service INTEGER NOT NULL,
  default_value VARCHAR,
  mandatory INTEGER,
  FOREIGN KEY (service) REFERENCES lov_service(id)
);

INSERT INTO lov_status (id, title) VALUES (1, 'active');
INSERT INTO lov_status (id, title) VALUES (2, 'deactive');
INSERT INTO lov_status (id, title) VALUES (3, 'suspend');

INSERT INTO lov_segment (id, title) VALUES (2, 'RES');
INSERT INTO lov_segment (id, title) VALUES (3, 'VSE');
INSERT INTO lov_segment (id, title) VALUES (4, 'SME');
INSERT INTO lov_segment (id, title)VALUES (5, 'LE');

INSERT INTO lov_billcycle (id, title) VALUES (1, '51');
INSERT INTO lov_billcycle (id, title) VALUES (2, '52');
INSERT INTO lov_billcycle (id, title) VALUES (3, '53');
INSERT INTO lov_billcycle (id, title) VALUES (4, '54');

INSERT INTO lov_market (id, title) VALUES (1, 'GSM');
INSERT INTO lov_market (id, title) VALUES (2, 'DSL');
INSERT INTO lov_market (id, title) VALUES (3, 'FIX');

INSERT INTO lov_tariff (id, title, segment, market, monthly_fee) VALUES (433, 'S nami sit nesit', 2, 1, 449);
INSERT INTO lov_tariff (id, title, segment, market, monthly_fee) VALUES (459, 'S nami sit nesit bez zavazku', 2, 1, 599);
INSERT INTO lov_tariff (id, title, segment, market, monthly_fee) VALUES (434, 'S nami sit nesit v podnikani', 3, 1, 449);
INSERT INTO lov_tariff (id, title, segment, market, monthly_fee) VALUES (460, 'S nami sit nesit v podnikani bez zavazku', 3, 1, 599);

INSERT INTO lov_contact_role (id, title) VALUES (1, 'contact');
INSERT INTO lov_contact_role (id, title) VALUES (2, 'contract');
INSERT INTO lov_contact_role (id, title) VALUES (3, 'invoicing');

INSERT INTO lov_address_role (id, title) VALUES (1, 'contact');
INSERT INTO lov_address_role (id, title) VALUES (2, 'contract');
INSERT INTO lov_address_role (id, title) VALUES (3, 'invoicing');
INSERT INTO lov_address_role (id, title) VALUES (4, 'delivery');

INSERT INTO lov_service (id, title, monthly_fee, customer, payer, subscriber) VALUES (615, 'Telefonni cislo', null, 0, 0, 1);
INSERT INTO lov_service (id, title, monthly_fee, customer, payer, subscriber) VALUES (619, 'SIM karta', null, 0, 0, 1);

INSERT INTO lov_service_param (id, title, service, default_value, mandatory) VALUES (121, 'MSISDN', 615, null, 1);
INSERT INTO lov_service_param (id, title, service, default_value, mandatory) VALUES (122, 'ICCID', 619, null, 1);
INSERT INTO lov_service_param (id, title, service, default_value, mandatory) VALUES (123, 'IMSI', 619, null, 1);