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
-- Dumping data for table `bank_data`
--

INSERT INTO `bank_data` (`bank_user_id`, `client_user_id`, `bank_share_path`) VALUES
(1, 2, './vsignit/output/bank/janedoe_DBS_bank_share.png'),
(1, 3, './vsignit/output/bank/johndoe_DBS_bank_share.png'),
(1, 4, './vsignit/output/bank/timapple_DBS_bank_share.png'),
(1, 7, './vsignit/output/bank/donaldtrump_DBS_bank_share.png'),
(1, 8, './vsignit/output/bank/matthewyeo_DBS_bank_share.png'),
(1, 9, './vsignit/output/bank/mohammedali_DBS_bank_share.png'),
(1, 10, './vsignit/output/bank/kimjongun_DBS_bank_share.png');

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

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
