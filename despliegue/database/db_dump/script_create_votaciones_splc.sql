SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

--
-- Base de datos: `votaciones_splc`
--

CREATE DATABASE IF NOT EXISTS `votaciones_splc`;

USE `votaciones_splc`;

drop table if exists cookie;
drop table if exists user;
drop table if exists user_account_per_census;
drop table if exists user_account;
drop table if exists role;
drop table if exists option_per_vote;
drop table if exists question_option;
drop table if exists question;
drop table if exists vote;
drop table if exists vote_type;
drop table if exists poll;
drop table if exists census;
drop table if exists ca;

#Role
create table if not exists role(
id int not null auto_increment,
name varchar(10) not null,
primary key(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;

INSERT INTO `role` (`id`, `name`)
VALUES
	(1,'ADMIN'),
	(2,'VOTER');

#UserAccount
create table if not exists user_account(
id int not null auto_increment,
username varchar(50) not null,
password varchar(50) not null,
email varchar(100) not null,
role_id int not null,
CONSTRAINT username_unique UNIQUE (username),
foreign key(role_id) references role(id) on update no action on delete cascade,
primary key(id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;

#Cookie
create table if not exists cookie(
number_id int not null,
user_account_id int not null,
primary key(number_id),
foreign key(user_account_id) references user_account(id) on update no action on delete cascade
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;


# ************************************************************
# Comunidades Autónomas.
# ------------------------------------------------------------

CREATE TABLE `ca` (
  `id` int NOT NULL auto_increment,
  `name` varchar(100) NOT NULL,
   primary key(id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;

INSERT INTO `ca` (`id`, `name`)
VALUES
	(1,'Andalucía'),
	(2,'Aragón'),
	(3,'Asturias, Principado de'),
	(4,'Balears, Illes'),
	(5,'Canarias'),
	(6,'Cantabria'),
	(7,'Castilla y León'),
	(8,'Castilla - La Mancha'),
	(9,'Catalunya'),
	(10,'Comunitat Valenciana'),
	(11,'Extremadura'),
	(12,'Galicia'),
	(13,'Madrid, Comunidad de'),
	(14,'Murcia, Región de'),
	(15,'Navarra, Comunidad Foral de'),
	(16,'País Vasco'),
	(17,'Rioja, La'),
	(18,'Ceuta'),
	(19,'Melilla');

#User
create table if not exists user (
id int not null auto_increment,
name varchar(100) not null,
surname varchar(200) not null,
#M:MUJER,H:HOMBRE
genre enum("M","H","I") not null,
edad date not null,
dni varchar(9) not null,
ca_id int not null,
user_account_id int not null,
primary key(id),
foreign key(ca_id) references ca(id) on update no action on delete cascade,
foreign key(user_account_id) references user_account(id) on update no action on delete cascade
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;

#Censo
create table if not exists census(
id int not null auto_increment,
title varchar(100) not null,
postalCode int,
ca_id int not null,
foreign key(ca_id) references ca(id) on update no action on delete cascade,
primary key (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;

#UserPerCensus
create table if not exists user_account_per_census(
id int not null auto_increment,
census_id int not null,
user_account_id int not null,
foreign key(census_id) references census(id) on update no action on delete cascade,
foreign key(user_account_id) references user_account(id) on update no action on delete cascade,
primary key(id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;


#Poll
create table if not exists poll(
id int not null auto_increment,
title varchar(50) not null,
description varchar(150),
startDate date not null,
endDate date not null,
census_id int not null,
foreign key(census_id) references census(id) on update no action on delete cascade,
primary key(id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;

#Question
create table if not exists question(
id int not null auto_increment,
title varchar(50) not null,
description varchar(150),
optional boolean not null,
multiple boolean not null,
poll_id int not null,
foreign key(poll_id) references poll(id) on update no action on delete cascade,
primary key(id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;

#Question Option
create table if not exists question_option(
id int not null auto_increment,
description varchar(150),
question_id int not null,
foreign key(question_id) references question(id) on update no action on delete cascade,
primary key(id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;

#VoteType
create table if not exists vote_type(
id int not null auto_increment,
name varchar(10) not null,
primary key(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;

INSERT INTO `vote_type` (`id`, `name`)
VALUES
	(1,'WEB'),
	(2,'SLACK'),
	(3,'TELEGRAM');


#Vote
create table if not exists vote(
id int not null auto_increment,
token varchar(150) not null,
vote_type_id int not null,
vote_date date not null,
foreign key(vote_type_id) references vote_type(id) on update no action on delete cascade,
primary key(id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;


#OptionPerVote
create table if not exists option_per_vote(
id int not null auto_increment,
vote_id int not null,
question_option_id int not null,
foreign key(vote_id) references vote(id) on update no action on delete cascade,
foreign key(question_option_id) references question_option(id) on update no action on delete cascade,
primary key(id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;
