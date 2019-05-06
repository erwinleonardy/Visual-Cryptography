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
-- Dumping data for table `client_data`
--

INSERT INTO `client_data` (`client_user_id`, `bank_user_id`, `client_share_path`) VALUES
(2, 1, './vsignit/output/client/janedoe_DBS_client_share.png'),
(3, 1, './vsignit/output/client/johndoe_DBS_client_share.png'),
(4, 1, './vsignit/output/client/timapple_DBS_client_share.png'),
(7, 1, './vsignit/output/client/donaldtrump_DBS_client_share.png'),
(8, 1, './vsignit/output/client/matthewyeo_DBS_client_share.png'),
(9, 1, './vsignit/output/client/mohammedali_DBS_client_share.png');

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

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
