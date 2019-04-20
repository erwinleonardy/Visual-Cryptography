-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Apr 20, 2019 at 08:42 AM
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
DROP TABLE IF EXISTS `vsignit`.`user_table`;

--
-- Table structure for table `user_table`
--

CREATE TABLE IF NOT EXISTS `user_table` (
  `user_id` int(11) UNSIGNED NOT NULL,
  `user_type` enum('admin','user') CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `email` varchar(100) NOT NULL,
  `username` varchar(70) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `password` varchar(70) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 ROW_FORMAT=COMPACT;

--
-- Dumping data for table `user_table`
--

INSERT INTO `user_table` (`user_id`, `user_type`, `email`, `username`, `password`) VALUES
(1, 'admin', 'veleseb@max-mail.info', 'DBS', '7026cf9936b5c5b974dc5db6422f542aed7b1f01'),
(2, 'user', 'rusocevupo@direct-mail.info', 'janedoe', '8a8deed44623d4c44268c26652d80945851c4f7f'),
(3, 'user', 'rusocevupo@direct-mail.info', 'johndoe', 'a51dda7c7ff50b61eaea0444371f4a6a9301e501'),
(4, 'user', 'rusocevupo@direct-mail.info', 'timapple', '5ee0edb9e2229c0838f1959779f1949031de0123'),
(5, 'admin', 'veleseb@max-mail.info', 'HSBC', '616da28709f422331b28f7106673c5ad02b6d477'),
(7, 'user', 'rusocevupo@direct-mail.info', 'donaldtrump', '53e11eb7b24cc39e33733a0ff06640f1b39425ea');

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
  MODIFY `user_id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
