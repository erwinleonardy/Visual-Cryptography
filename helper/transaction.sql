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
('0ae3cd1497139ebfbe8995bc160314bb96030fd6', 7, 1, '2019-05-06 15:20:20', './vsignit/output/cheque/cheque_0ae3cd1497139ebfbe8995bc160314bb96030fd6.png'),
('5453566bd6b53e28095c78efd024083d590fa275', 2, 1, '2019-05-06 15:19:47', './vsignit/output/cheque/cheque_5453566bd6b53e28095c78efd024083d590fa275.png'),
('5853ed09e024358df3b482447a85d9806a4a006d', 4, 1, '2019-05-06 15:20:01', './vsignit/output/cheque/cheque_5853ed09e024358df3b482447a85d9806a4a006d.png'),
('9b9495ad265848cdb3d018e3071fa0cad35c6f1f', 3, 1, '2019-05-06 15:16:54', './vsignit/output/cheque/cheque_9b9495ad265848cdb3d018e3071fa0cad35c6f1f.png'),
('c276ddebc8194557b82c9a3b5eb547cfff5ed3cd', 8, 1, '2019-05-06 15:20:37', './vsignit/output/cheque/cheque_c276ddebc8194557b82c9a3b5eb547cfff5ed3cd.png'),
('d5b566ba7ebdbd1410e4510f85e2ffdfec90d901', 9, 1, '2019-05-06 15:20:52', './vsignit/output/cheque/cheque_d5b566ba7ebdbd1410e4510f85e2ffdfec90d901.png');

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
