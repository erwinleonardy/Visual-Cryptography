-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Apr 30, 2019 at 08:22 AM
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
('071901a75c789e8cc99063b5e2e121325e111ebe', 2, 1, '2019-04-30 08:17:49', './vsignit/output/cheque/cheque_071901a75c789e8cc99063b5e2e121325e111ebe.png'),
('1c8f0ba827b04a4784f78a0dc06fdcae07a11bf0', 4, 1, '2019-04-30 08:18:04', './vsignit/output/cheque/cheque_1c8f0ba827b04a4784f78a0dc06fdcae07a11bf0.png'),
('429f8fe8eec9fb0eb4633a733bc2612a841dd762', 4, 1, '2019-04-30 08:18:02', './vsignit/output/cheque/cheque_429f8fe8eec9fb0eb4633a733bc2612a841dd762.png'),
('46da2aea669476571c4bd0321e5e192fb37810d0', 3, 1, '2019-04-30 08:16:28', './vsignit/output/cheque/cheque_46da2aea669476571c4bd0321e5e192fb37810d0.png'),
('4c8bf7a490ec3e53f144b54e558d9314d33f7aa9', 2, 1, '2019-04-30 08:17:47', './vsignit/output/cheque/cheque_4c8bf7a490ec3e53f144b54e558d9314d33f7aa9.png'),
('643b048ecbb988fd96bc707126aa072fceb23d0d', 3, 1, '2019-04-30 08:16:27', './vsignit/output/cheque/cheque_643b048ecbb988fd96bc707126aa072fceb23d0d.png'),
('76c5b2e1c84a80ecd9801761eb4d22d53995b6c5', 2, 1, '2019-04-30 08:17:46', './vsignit/output/cheque/cheque_76c5b2e1c84a80ecd9801761eb4d22d53995b6c5.png'),
('84c4e0514d377d26acc5718a16166984da6a866e', 7, 1, '2019-04-30 08:18:16', './vsignit/output/cheque/cheque_84c4e0514d377d26acc5718a16166984da6a866e.png'),
('8d67912fc0d3866a0a50a29c4637647ec9a30672', 4, 1, '2019-04-30 08:18:03', './vsignit/output/cheque/cheque_8d67912fc0d3866a0a50a29c4637647ec9a30672.png'),
('92bc297d32ecd229594f94405e1050d4e30937c1', 2, 1, '2019-04-30 08:17:48', './vsignit/output/cheque/cheque_92bc297d32ecd229594f94405e1050d4e30937c1.png'),
('a42eeb40b92937cb8b7395e4a7f5c7aa1b711eef', 4, 1, '2019-04-30 08:18:46', './vsignit/output/cheque/cheque_a42eeb40b92937cb8b7395e4a7f5c7aa1b711eef.png'),
('a71dfd682218aad260bc81af1af674a92cd500f2', 7, 1, '2019-04-30 08:18:18', './vsignit/output/cheque/cheque_a71dfd682218aad260bc81af1af674a92cd500f2.png'),
('c7c4c7764a26f2bf949fd4a74259365e2ad599c9', 3, 1, '2019-04-30 08:17:37', './vsignit/output/cheque/cheque_c7c4c7764a26f2bf949fd4a74259365e2ad599c9.png'),
('c7ecca24b745180d1ead1e4b06e616a1b66d04d9', 3, 1, '2019-04-30 08:18:29', './vsignit/output/cheque/cheque_c7ecca24b745180d1ead1e4b06e616a1b66d04d9.png'),
('d63faf3e3cf213551a67b0af1f56320d0043c88e', 4, 1, '2019-04-30 08:18:01', './vsignit/output/cheque/cheque_d63faf3e3cf213551a67b0af1f56320d0043c88e.png'),
('d6c3b9c1ec36ab36228c1de1bef963a18a28d437', 3, 1, '2019-04-30 08:16:24', './vsignit/output/cheque/cheque_d6c3b9c1ec36ab36228c1de1bef963a18a28d437.png'),
('dea7e3900900b698a1b18575f329cb70c90b85d9', 7, 1, '2019-04-30 08:18:17', './vsignit/output/cheque/cheque_dea7e3900900b698a1b18575f329cb70c90b85d9.png'),
('ea0ca8c98d13c76c6430b5c7bb84107a4f121751', 8, 1, '2019-04-28 02:19:35', './vsignit/output/cheque/cheque_ea0ca8c98d13c76c6430b5c7bb84107a4f121751.png'),
('ff911663da76f57ee466337bff10209006ecaf86', 2, 1, '2019-04-30 08:18:37', './vsignit/output/cheque/cheque_ff911663da76f57ee466337bff10209006ecaf86.png');

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
