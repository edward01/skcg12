/*
** to execute:
cd <sql_scripts folder>
mysql --host=127.0.0.1 -uroot -p
source sql_scripts.sql
*/

-- CREATE DEFAULT DATA
INSERT INTO `users` (`tbl_id`, `username`, `password`, `acct_active`, `password_temp`) VALUES ('1', 'admin', 'admin', 1, 0);
