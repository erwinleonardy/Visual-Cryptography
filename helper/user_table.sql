-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Apr 20, 2019 at 08:42 AM
-- Server version: 8.0.15
-- PHP Version: 7.1.23

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `vsignit`
--

-- --------------------------------------------------------

--
-- Drop existing table
--
DROP TABLE IF EXISTS `vsignit`.`user_table`;

--
-- Table structure for table `user_table`
--

CREATE TABLE IF NOT EXISTS `user_table` (
  `user_id` int(11) UNSIGNED NOT NULL,
  `user_type` enum('admin','user') CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `email` varchar(100) NOT NULL,
  `username` varchar(70) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `password` varchar(128) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 ROW_FORMAT=COMPACT;

--
-- Dumping data for table `user_table`
--

INSERT INTO `user_table` (`user_id`, `user_type`, `email`, `username`, `password`) VALUES
(1, 'admin', 'veleseb@max-mail.info', 'DBS', 'pbkdf2:sha256:150000$3DaWGCwB$90db741fbaa5420fad5cee64646562e74d355d553e09488adc881a0ca4babae1'),
(2, 'user', 'rusocevupo@direct-mail.info', 'janedoe', 'pbkdf2:sha256:150000$kouFGPTV$f7890d5acbb3ec18c83f3af4fbe6cfc1daa21d7976986dc8d04879dd4f91c237'),
(3, 'user', 'rusocevupo@direct-mail.info', 'johndoe', 'pbkdf2:sha256:150000$8SdvwIgg$76228fa362efeddcc71e20744d44b69002cc29b2263e3c232772c8241d03bc9b'),
(4, 'user', 'rusocevupo@direct-mail.info', 'timapple', 'pbkdf2:sha256:150000$7mOYt08J$fc0307caf5bdb16f1933c1e4244b9d27fc7cb5c3cca54d46639283f9ef08cc37'),
(5, 'admin', 'veleseb@max-mail.info', 'HSBC', 'pbkdf2:sha256:150000$Dj5kYxxr$fb25ef376b2d2ff36269e9dcd8eaed15f80dedf884345f146abea7421c306480'),
(7, 'user', 'rusocevupo@direct-mail.info', 'donaldtrump', 'pbkdf2:sha256:150000$uloLEq3t$5fc7cc6cfbc624f8e1602e1e3e18488c254d42328c1b615eedc265cdbd510010');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `user_table`
--
ALTER TABLE `user_table`
  ADD PRIMARY KEY (`user_id`),
  ADD KEY `Index` (`user_id`,`username`) USING BTREE;

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `user_table`
--
ALTER TABLE `user_table`
  MODIFY `user_id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
