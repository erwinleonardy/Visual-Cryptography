-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Apr 20, 2019 at 03:33 PM
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
-- Dumping data for table `transaction`
--

INSERT INTO `transaction` (`transaction_number`, `client_user_id`, `bank_user_id`, `timestamp`, `filepath`) VALUES
('1d5ba78f7f878dae56b1766b40b1280217f9d369', 2, 1, '2019-04-20 15:30:20', './vsignit/output/cheque/cheque_1d5ba78f7f878dae56b1766b40b1280217f9d369.png'),
('687ec9012daedbecc55d5c970f0edbd8a80f01ad', 2, 5, '2019-04-20 15:22:09', './vsignit/output/cheque/cheque_687ec9012daedbecc55d5c970f0edbd8a80f01ad.png'),
('ee4ee87599378df7543f835b9ecfb67048c87ad4', 2, 1, '2019-04-20 15:30:12', './vsignit/output/cheque/cheque_ee4ee87599378df7543f835b9ecfb67048c87ad4.png');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `transaction`
--
ALTER TABLE `transaction`
  ADD PRIMARY KEY (`transaction_number`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
