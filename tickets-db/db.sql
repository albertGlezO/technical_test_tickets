CREATE DATABASE `tickets`;

USE `tickets`;

CREATE TABLE `events` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  `from_datetime` datetime NOT NULL,
  `to_datetime` datetime NOT NULL,
  `total_tickets` int(11) NOT NULL,
  `total_ticket_sales` int(11) DEFAULT '0',
  `total_ticket_redeem` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `tickets` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `event_id` int(11) NOT NULL,
  `ticket_hash` varchar(37) NOT NULL,
  `redeem` tinyint(4) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `tickets_FK` (`event_id`),
  CONSTRAINT `tickets_FK` FOREIGN KEY (`event_id`) REFERENCES `events` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
