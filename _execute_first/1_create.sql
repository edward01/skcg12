/*
** to execute:
cd <sql_scripts folder>
mysql --host=127.0.0.1 -uroot -p
source sql_scripts.sql
*/

CREATE DATABASE `skcg12` /*!40100 DEFAULT CHARACTER SET utf8 */;
use `skcg12`;


-- CREATE TABLES
CREATE TABLE `users` (
  `tbl_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(45) NOT NULL,
  `password` varchar(100) NOT NULL,
  `last_login_timestamp` datetime DEFAULT NULL,
  `acct_active` tinyint(1) DEFAULT '0',
  `password_temp` tinyint(1) DEFAULT '1',
  `member_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`tbl_id`,`username`),
  UNIQUE KEY `username_UNIQUE` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;


CREATE TABLE `members` (
  `tbl_id` int(11) NOT NULL AUTO_INCREMENT,
  `lastname` varchar(100) NOT NULL,
  `firstname` varchar(100) NOT NULL,
  `middlename` varchar(100) DEFAULT NULL,
  `email` varchar(60) DEFAULT NULL,
  `birthdate` datetime DEFAULT NULL,
  `gender` char(1) DEFAULT NULL,
  `barangay_id` int(11) DEFAULT NULL,
  `city_id` int(11) DEFAULT NULL,
  `cellleader_id` int(11) DEFAULT NULL,
  `cellgroup_id` int(11) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`tbl_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
