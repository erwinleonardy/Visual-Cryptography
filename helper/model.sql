-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Apr 30, 2019 at 12:59 PM
-- Server version: 8.0.15
-- PHP Version: 7.1.23

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+08:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `vsignit`
--
CREATE DATABASE IF NOT EXISTS `vsignit`

-- --------------------------------------------------------

--
-- Drop existing table
--
DROP TABLE IF EXISTS `vsignit`.`bank_data`;

--
-- Table structure for table `bank_data`
--
CREATE TABLE IF NOT EXISTS `bank_data` (
  `bank_user_id` int(11) NOT NULL,
  `client_user_id` int(11) NOT NULL,
  `bank_share_path` varchar(100) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


--
-- Indexes for dumped tables
--

--
-- Indexes for table `bank_data`
--
ALTER TABLE `bank_data`
  ADD PRIMARY KEY (`bank_user_id`,`client_user_id`) USING BTREE,
  ADD KEY `bank_user_id` (`bank_user_id`,`client_user_id`) USING BTREE;
COMMIT;

-- --------------------------------------------------------

--
-- Drop existing table
--
DROP TABLE IF EXISTS `vsignit`.`client_data`;

--
-- Table structure for table `client_data`
--
CREATE TABLE IF NOT EXISTS `client_data` (
  `client_user_id` int(11) NOT NULL,
  `bank_user_id` int(11) NOT NULL,
  `client_share_path` varchar(100) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 ROW_FORMAT=COMPACT;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `client_data`
--
ALTER TABLE `client_data`
  ADD PRIMARY KEY (`client_user_id`,`bank_user_id`),
  ADD KEY `client_user_id` (`client_user_id`,`bank_user_id`);
COMMIT;

-- --------------------------------------------------------

--
-- Drop existing table
--
DROP TABLE IF EXISTS `vsignit`.`transaction`;

--
-- Table structure for table `transaction`
--
CREATE TABLE IF NOT EXISTS `transaction` (
  `transaction_number` varchar(70) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `client_user_id` int(11) NOT NULL,
  `bank_user_id` int(11) NOT NULL,
  `timestamp` timestamp NOT NULL,
  `filepath` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 ROW_FORMAT=COMPACT;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `transaction`
--
ALTER TABLE `transaction`
  ADD PRIMARY KEY (`transaction_number`);
COMMIT;

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
(1, 'admin', 'gafusoyici@stattech.info', 'DBS', 'pbkdf2:sha256:150000$3DaWGCwB$90db741fbaa5420fad5cee64646562e74d355d553e09488adc881a0ca4babae1'),
(2, 'user', 'gafusoyici@stattech.info', 'janedoe', 'pbkdf2:sha256:150000$kouFGPTV$f7890d5acbb3ec18c83f3af4fbe6cfc1daa21d7976986dc8d04879dd4f91c237'),
(3, 'user', 'gafusoyici@stattech.info', 'johndoe', 'pbkdf2:sha256:150000$8SdvwIgg$76228fa362efeddcc71e20744d44b69002cc29b2263e3c232772c8241d03bc9b');

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
  MODIFY `user_id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
COMMIT;