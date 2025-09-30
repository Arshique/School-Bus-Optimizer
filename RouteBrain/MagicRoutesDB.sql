CREATE DATABASE SchlDb;
USE SchlDb;

CREATE Table Admin(
    Adm_Id varchar(7) PRIMARY KEY,
    Adm_username varchar(20) UNIQUE,
    Adm_pass varchar(25) NOT NULL,
    Adm_role ENUM("Admin","Staff","Driver")
);

CREATE TABLE School(
    Schl_id INT PRIMARY KEY Auto_Increment,
    Schl_name varchar(30) NOT NULL,
    Schl_addrs Text NOT NULL
    contact_num INT(10) UNIQUE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL
);

CREATE TABLE Student(
    Std_id INT PRIMARY KEY Auto_Increment,
    Std_name varchar(30) NOT NULL,
    class varchar(3) NOT NULL,
    Roll_no INT NOT NULL,
    Std_addrs Text NOT NULL,
    contact_num INT(10) UNIQUE NOT NULL,
    Schl_id INT,
    FOREIGN KEY (Schl_id) REFERENCES School(Schl_id)
);

CREATE TABLE Driver(
    Drv_id INT PRIMARY KEY Auto_Increment,
    Drv_name varchar(30) NOT NULL,
    Drv_lic_no varchar(15) UNIQUE NOT NULL,
    contact_num INT(10) UNIQUE NOT NULL,
    Adm_id varchar(7),
    FOREIGN KEY (Adm_id) REFERENCES Admin(Adm_Id)
);

CREATE TABLE Bus(
    Bus_id INT PRIMARY KEY Auto_Increment,
    Bus_no varchar(10) UNIQUE NOT NULL,
    capacity INT NOT NULL,
    Drv_id INT,
    Schl_id INT,
    Rte_id INT,
    FOREIGN KEY (Drv_id) REFERENCES Driver(Drv_id),
    FOREIGN KEY (Schl_id) REFERENCES School(Schl_id),
    FOREIGN KEY (Rte_id) REFERENCES Route(Rte_id)
);

CREATE TABLE Route(
    Rte_id INT PRIMARY KEY Auto_Increment,
    Rte_name varchar(20) NOT NULL,
    start_point varchar(30) NOT NULL,
    end_point varchar(30) NOT NULL,
    Total_distance FLOAT NOT NULL,
    Est_time INT NOT NULL
);

CREATE TABLE Stop(
    Stp_id INT PRIMARY KEY Auto_Increment,
    Stp_name varchar(30) NOT NULL,
    latitude DOUBLE NOT NULL,
    longitude DOUBLE NOT NULL,
    Rte_id INT,
    FOREIGN KEY (Rte_id) REFERENCES Route(Rte_id)
);