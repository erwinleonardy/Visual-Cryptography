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
('0047961963c07b968991533486d86b343b5faea9', 2, 1, '2019-04-30 12:47:44', './vsignit/output/cheque/cheque_0047961963c07b968991533486d86b343b5faea9.png'),
('0a13843c5d0a150db110be8693805848df5b5622', 7, 1, '2019-04-30 12:55:13', './vsignit/output/cheque/cheque_0a13843c5d0a150db110be8693805848df5b5622.png'),
('2bd9663e58bf16ab278007d91c236e8dee25c6eb', 9, 1, '2019-04-30 12:57:41', './vsignit/output/cheque/cheque_2bd9663e58bf16ab278007d91c236e8dee25c6eb.png'),
('357f44c3613a6bce9157dd55f81961a2545c156c', 3, 1, '2019-04-30 12:55:36', './vsignit/output/cheque/cheque_357f44c3613a6bce9157dd55f81961a2545c156c.png'),
('3d47c907455649b455bf092e72bebe3c20f1370d', 3, 1, '2019-04-30 12:56:57', './vsignit/output/cheque/cheque_3d47c907455649b455bf092e72bebe3c20f1370d.png'),
('457e51a867cd90e14f6d3c8378446c8e2439d3f2', 4, 1, '2019-04-30 12:55:24', './vsignit/output/cheque/cheque_457e51a867cd90e14f6d3c8378446c8e2439d3f2.png'),
('688beaad2f4de77d45cbdc8c0fe8e6a25824d5c4', 8, 1, '2019-04-30 12:56:09', './vsignit/output/cheque/cheque_688beaad2f4de77d45cbdc8c0fe8e6a25824d5c4.png'),
('69b22639b0cb83fc8bccadbac22259e422dcb138', 9, 1, '2019-04-30 12:57:42', './vsignit/output/cheque/cheque_69b22639b0cb83fc8bccadbac22259e422dcb138.png'),
('8a3bf86b54bc49cae99a8774c2a76bec0941bb74', 3, 1, '2019-04-30 12:47:32', './vsignit/output/cheque/cheque_8a3bf86b54bc49cae99a8774c2a76bec0941bb74.png'),
('9bd080d0c94e598d3b824d5b03104c3068bb18db', 2, 1, '2019-04-30 12:57:08', './vsignit/output/cheque/cheque_9bd080d0c94e598d3b824d5b03104c3068bb18db.png'),
('9f232bda2604b382d4e1f15addeac682246363b9', 3, 1, '2019-04-30 12:49:26', './vsignit/output/cheque/cheque_9f232bda2604b382d4e1f15addeac682246363b9.png'),
('b5db831efec0692f3e670f413e46117eb10823e7', 3, 1, '2019-04-30 12:56:58', './vsignit/output/cheque/cheque_b5db831efec0692f3e670f413e46117eb10823e7.png'),
('d54fc0d14c09355c6d3478b627171f4e3c0a3d69', 3, 1, '2019-04-30 12:49:25', './vsignit/output/cheque/cheque_d54fc0d14c09355c6d3478b627171f4e3c0a3d69.png'),
('d83e25225d9228cf81a19b300e53dbf2284e9899', 2, 1, '2019-04-30 12:47:42', './vsignit/output/cheque/cheque_d83e25225d9228cf81a19b300e53dbf2284e9899.png'),
('e3a1fee61195d75491796640e09c8cc81ea0ad11', 8, 1, '2019-04-30 12:56:10', './vsignit/output/cheque/cheque_e3a1fee61195d75491796640e09c8cc81ea0ad11.png'),
('f027ff6d29718ead2801dbaef56cb6aa705c71b3', 7, 1, '2019-04-30 12:55:11', './vsignit/output/cheque/cheque_f027ff6d29718ead2801dbaef56cb6aa705c71b3.png');

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
