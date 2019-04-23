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
('12c1bdf65e36e02ca31bbfcecdae5deb18ba4475', 3, 1, '2019-04-21 12:55:07', './vsignit/output/cheque/cheque_12c1bdf65e36e02ca31bbfcecdae5deb18ba4475.png'),
('1e58aaaf5bc5a746d7bedd7343cdd7b1dd3f3dc1', 3, 1, '2019-04-22 02:51:16', './vsignit/output/cheque/cheque_1e58aaaf5bc5a746d7bedd7343cdd7b1dd3f3dc1.png'),
('4985fab3030ad209a501aced52546c92fd1c2eaf', 3, 1, '2019-04-21 12:56:49', './vsignit/output/cheque/cheque_4985fab3030ad209a501aced52546c92fd1c2eaf.png'),
('5d222357215969648bf47dd3cba63b987bb9105d', 3, 1, '2019-04-23 05:45:59', './vsignit/output/cheque/cheque_5d222357215969648bf47dd3cba63b987bb9105d.png'),
('66b215bc90fcc71a658910a5c54d0bfb13417c71', 7, 1, '2019-04-21 12:56:34', './vsignit/output/cheque/cheque_66b215bc90fcc71a658910a5c54d0bfb13417c71.png'),
('b80d015406fddd3d324a369aa64b95471190bd2d', 3, 1, '2019-04-21 12:56:51', './vsignit/output/cheque/cheque_b80d015406fddd3d324a369aa64b95471190bd2d.png'),
('b812217d6aa5b7410fdfc48a55a7a5f4cfe4647a', 3, 1, '2019-04-23 12:33:11', './vsignit/output/cheque/cheque_b812217d6aa5b7410fdfc48a55a7a5f4cfe4647a.png'),
('c1866956d296089a140a0653b5574d69bfd79ed0', 3, 1, '2019-04-21 12:56:47', './vsignit/output/cheque/cheque_c1866956d296089a140a0653b5574d69bfd79ed0.png'),
('d20974e6bd15825f0304a13f0b19fd3142b4fde1', 3, 1, '2019-04-22 01:21:07', './vsignit/output/cheque/cheque_d20974e6bd15825f0304a13f0b19fd3142b4fde1.png'),
('d5b28c68acc358cd39c30ef07185a4e419041555', 2, 1, '2019-04-21 12:56:11', './vsignit/output/cheque/cheque_d5b28c68acc358cd39c30ef07185a4e419041555.png'),
('d6d1abcbce7eea6a332e985e1d9cb25d331fed54', 3, 1, '2019-04-23 16:28:05', './vsignit/output/cheque/cheque_d6d1abcbce7eea6a332e985e1d9cb25d331fed54.png'),
('dc5e4fd6b0055ba768f51a3e1b13698b715332c9', 3, 1, '2019-04-22 01:21:25', './vsignit/output/cheque/cheque_dc5e4fd6b0055ba768f51a3e1b13698b715332c9.png'),
('e0dff950c24fb6cc5be80cb0088d427cb8a449c1', 3, 1, '2019-04-22 02:57:53', './vsignit/output/cheque/cheque_e0dff950c24fb6cc5be80cb0088d427cb8a449c1.png'),
('fc716078c1df9cac5a9653ec48dd856e72ae7ddd', 3, 1, '2019-04-23 12:34:35', './vsignit/output/cheque/cheque_fc716078c1df9cac5a9653ec48dd856e72ae7ddd.png');

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
