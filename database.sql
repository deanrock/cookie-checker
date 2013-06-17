CREATE TABLE IF NOT EXISTS `cookies` (
  `id` bigint(255) NOT NULL AUTO_INCREMENT,
  `test_id` int(255) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `domain` varchar(255) DEFAULT NULL,
  `value` varchar(255) DEFAULT NULL,
  `expires` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `tests`
--

CREATE TABLE IF NOT EXISTS `tests` (
  `id` int(255) NOT NULL AUTO_INCREMENT,
  `datetime` datetime NOT NULL,
  `domain` varchar(255) DEFAULT NULL,
  `status` int(255) DEFAULT NULL,
  `info` varchar(255) DEFAULT NULL,
  `finished` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `proxy_cookies` (
  `id` bigint(255) NOT NULL AUTO_INCREMENT,
  `datetime` datetime DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `value` varchar(255) DEFAULT NULL,
  `expiry` varchar(255) DEFAULT NULL,
  `host` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
