CREATE TABLE `users` (
  `userid` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `password` varchar(40) NOT NULL,
  `member_id` int NULL,
  PRIMARY KEY (`userid`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;


CREATE TABLE `members` (
  `_id` int(11) NOT NULL AUTO_INCREMENT,
  `lastname` varchar(45) NOT NULL,
  `firstname` varchar(45) NOT NULL,
  `middlename` varchar(45) DEFAULT NULL,
  `birthdate` datetime DEFAULT NULL,
  `email` VARCHAR(45) NULL,
  `picture_filename` VARCHAR(45) NULL,
  `gender` CHAR(1) NULL,
  `address` VARCHAR(100) NULL,
  `city` VARCHAR(50) NULL,
  `nickname` VARCHAR(20) NULL,
  `cell_leader_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
