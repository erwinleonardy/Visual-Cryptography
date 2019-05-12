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
(9, 1, './vsignit/output/client/mohammedali_DBS_client_share.png'),
(10, 1, './vsignit/output/client/kimjongun_DBS_client_share.png');

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
-- Dumping data for table `transaction`
--

INSERT INTO `transaction` (`transaction_number`, `client_user_id`, `bank_user_id`, `timestamp`, `filepath`) VALUES
('138b82ce5a4eb63ea14456a908cf0d779c601fe2', 8, 1, '2019-05-09 15:58:00', './vsignit/output/cheque/cheque_138b82ce5a4eb63ea14456a908cf0d779c601fe2.png'),
('33a3c36314f7c5ff8d11fd188a0ec0418eb3ab4d', 2, 1, '2019-05-09 15:57:29', './vsignit/output/cheque/cheque_33a3c36314f7c5ff8d11fd188a0ec0418eb3ab4d.png'),
('3f41b1f7ea3f1c4e3488019aef5f40fcd2a844b2', 9, 1, '2019-05-09 15:58:21', './vsignit/output/cheque/cheque_3f41b1f7ea3f1c4e3488019aef5f40fcd2a844b2.png'),
('9ec1dfa2a24f6e34d05ef3dec1016f8bb07bb12b', 3, 1, '2019-05-09 15:57:42', './vsignit/output/cheque/cheque_9ec1dfa2a24f6e34d05ef3dec1016f8bb07bb12b.png'),
('da3cf4bc07b8056ffbe34e50c29fc67c78fc7b6a', 3, 1, '2019-05-09 15:57:17', './vsignit/output/cheque/cheque_da3cf4bc07b8056ffbe34e50c29fc67c78fc7b6a.png');
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
(3, 'user', 'gafusoyici@stattech.info', 'johndoe', 'pbkdf2:sha256:150000$8SdvwIgg$76228fa362efeddcc71e20744d44b69002cc29b2263e3c232772c8241d03bc9b'),
(4, 'user', 'gafusoyici@stattech.info', 'timapple', 'pbkdf2:sha256:150000$7mOYt08J$fc0307caf5bdb16f1933c1e4244b9d27fc7cb5c3cca54d46639283f9ef08cc37'),
(5, 'admin', 'gafusoyici@stattech.info', 'HSBC', 'pbkdf2:sha256:150000$Dj5kYxxr$fb25ef376b2d2ff36269e9dcd8eaed15f80dedf884345f146abea7421c306480'),
(7, 'user', 'gafusoyici@stattech.info', 'donaldtrump', 'pbkdf2:sha256:150000$uloLEq3t$5fc7cc6cfbc624f8e1602e1e3e18488c254d42328c1b615eedc265cdbd510010'),
(8, 'user', 'gafusoyici@stattech.info', 'matthewyeo', 'pbkdf2:sha256:150000$V9YwLwB4$158c7d584b6b13cb807ae1bf0a92eae9de5f2d88ee5b2548027a696a9b5b88b1'),
(9, 'user', 'gafusoyici@stattech.info', 'mohammedali', 'pbkdf2:sha256:150000$31Af1YXM$dd8d06b2b29988b7f5fc8bb004c1610f4f9346c641da0ebda5ad443a64eeb2fe'),
(10, 'user', 'gafusoyici@stattech.info', 'kimjongun', 'pbkdf2:sha256:150000$G2P54b7J$92b3850bc46014d1d84ecf38599b07b3ac2d1f4136e6f145d7a6ca213dae4182');

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
  MODIFY `user_id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;
COMMIT;