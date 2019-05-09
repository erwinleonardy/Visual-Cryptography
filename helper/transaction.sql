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

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
