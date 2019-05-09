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
('008cbd5ffbe2fa0e85e1de929c48d1aaace8446c', 4, 1, '2019-05-09 14:17:37', './vsignit/output/cheque/cheque_008cbd5ffbe2fa0e85e1de929c48d1aaace8446c.png'),
('179c7fe6dbdb3f680ced2e746a4ac4e3dab3866c', 4, 1, '2019-05-09 14:09:25', './vsignit/output/cheque/cheque_179c7fe6dbdb3f680ced2e746a4ac4e3dab3866c.png'),
('33460baac8c62298c35df186b4fe42be550872d4', 8, 1, '2019-05-09 14:13:50', './vsignit/output/cheque/cheque_33460baac8c62298c35df186b4fe42be550872d4.png'),
('3c9fef1fc28ca66acff2945e8748b7a7b00eaa44', 7, 1, '2019-05-09 14:09:11', './vsignit/output/cheque/cheque_3c9fef1fc28ca66acff2945e8748b7a7b00eaa44.png'),
('6e7458dae1fa5c891fa326fcdc49ec18abc6f9ab', 9, 1, '2019-05-09 14:12:04', './vsignit/output/cheque/cheque_6e7458dae1fa5c891fa326fcdc49ec18abc6f9ab.png'),
('c1017ef11b91c9d913531d6fc75e264ba494be72', 10, 1, '2019-05-09 14:16:23', './vsignit/output/cheque/cheque_c1017ef11b91c9d913531d6fc75e264ba494be72.png'),
('c90a9eb4366b417527b88a8447ee782fbb86453c', 3, 1, '2019-05-09 14:13:08', './vsignit/output/cheque/cheque_c90a9eb4366b417527b88a8447ee782fbb86453c.png'),
('cff83018f7e1c92af830455d3a7728fe193c8169', 2, 1, '2019-05-09 14:08:38', './vsignit/output/cheque/cheque_cff83018f7e1c92af830455d3a7728fe193c8169.png'),
('e7eaf03165f4d4e0998fd059d4947a54fcad7f16', 3, 1, '2019-05-09 14:08:20', './vsignit/output/cheque/cheque_e7eaf03165f4d4e0998fd059d4947a54fcad7f16.png'),
('ec6f1ef86a6029a0e6f658d670e467078f5b8d11', 2, 1, '2019-05-09 14:08:47', './vsignit/output/cheque/cheque_ec6f1ef86a6029a0e6f658d670e467078f5b8d11.png');
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
