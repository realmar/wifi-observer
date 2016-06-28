DROP TABLE IF EXISTS data;
DROP TABLE IF EXISTS ssids;
DROP TABLE IF EXISTS bssids;

CREATE TABLE ssids (
  id    INTEGER PRIMARY KEY AUTOINCREMENT,
  ssid  VARCHAR(11)
);

CREATE TABLE bssids (
  id      INTEGER PRIMARY KEY AUTOINCREMENT,
  bssid   VARCHAR(18)
);

CREATE TABLE  data (
  id                  INTEGER PRIMARY KEY AUTOINCREMENT,
  time_needed_conn    FLOAT(7) NULL,
  time_needed_dhcp    FLOAT(7) NULL,
  ping_average        FLOAT(7) NULL,
  time_start          TIMESTAMP NOT NULL,
  dbm                 INTEGER NULL,
  ssid_fk             INTEGER UNSIGNED NOT NULL,
  bssid_fk            INTEGER UNSIGNED NULL,
  location_fk         INTEGER UNSIGNED NULL,
  FOREIGN KEY(ssid_fk)  REFERENCES ssids(id),
  FOREIGN KEY(bssid_fk) REFERENCES bssids(id),
  FOREIGN KEY(location_fk) REFERENCES locations(id)
);

CREATE TABLE errors (
  id    INTEGER PRIMARY KEY AUTOINCREMENT,
  code  VARCHAR(1024)
);

CREATE TABLE errors_data (
  id        INTEGER PRIMARY KEY AUTOINCREMENT,
  data_fk   INTEGER UNSIGNED NOT NULL,
  error_fk  INTEGER UNSIGNED NOT NULL
);

CREATE TABLE locations (
  id        INTEGER PRIMARY KEY AUTOINCREMENT,
  location  VARCHAR(200)
);
