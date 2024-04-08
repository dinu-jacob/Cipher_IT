-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 05, 2019 at 09:54 AM
-- Server version: 10.1.36-MariaDB
-- PHP Version: 7.2.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cipherwu`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `a_id` int(50) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`a_id`, `username`, `password`) VALUES
(1, 'admin', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `feedback`
--

CREATE TABLE `feedback` (
  `id` int(11) NOT NULL,
  `sendfrom` varchar(250) NOT NULL,
  `sendto` varchar(250) NOT NULL,
  `date` date NOT NULL,
  `subject` varchar(20) NOT NULL,
  `feedback` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `feedback`
--

INSERT INTO `feedback` (`id`, `sendfrom`, `sendto`, `date`, `subject`, `feedback`) VALUES
(14, 'inumaria21@gmail.com', 'admin', '2018-10-29', 'security', 'High security'),
(15, 'drisyapr@gmail.com', 'admin', '2018-10-29', 'design', 'good user interface'),
(16, 'keerthanacmurali@gmail.com', 'admin', '2018-10-29', 'feedback', 'Easily accessible'),
(17, 'jithinjolya.jj77@gmail.com', 'admin', '2018-10-29', 'user', 'good user support\r\n'),
(18, 'rosycandida96@gmail.com', 'admin', '2018-10-29', 'feedback', 'nice'),
(19, 'inumaria21@gmail.com', 'admin', '2018-10-29', 'perfomance', 'very good'),
(21, 'jithinjolya.jj77@gmail.com', 'admin', '2018-10-29', 'Error', 'file upload not possible'),
(22, 'inumaria21@gmail.com', 'admin', '2018-10-31', 'Error', 'bad'),
(23, 'keerthanacmurali@gmail.com', 'admin', '2018-11-02', 'feedback', 'well done'),
(24, 'snehavk2012@gmail.com', 'admin', '2018-11-09', 'UI', 'Good interface'),
(25, 'drisyapr@gmail.com', 'admin', '2018-11-10', 'cipher', 'super'),
(26, 'neethupp754@gmail.com', 'admin', '2019-10-18', 'Subject', 'helllo'),
(27, 'neethupp754@gmail.com', 'admin', '2019-11-02', 'sn', 'hhhhh'),
(28, 'manu@gmail.com', 'admin', '2019-11-05', 'file trasnsfr', 'add different type of file ');

-- --------------------------------------------------------

--
-- Table structure for table `message`
--

CREATE TABLE `message` (
  `mid` int(11) NOT NULL,
  `date` date NOT NULL,
  `msgfrom` varchar(100) NOT NULL,
  `sendto` varchar(100) NOT NULL,
  `subject` varchar(100) NOT NULL,
  `content` varchar(225) NOT NULL,
  `status` varchar(10) NOT NULL,
  `image` varchar(250) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `message`
--

INSERT INTO `message` (`mid`, `date`, `msgfrom`, `sendto`, `subject`, `content`, `status`, `image`) VALUES
(154, '2019-11-05', 'manu@gmail.com', 'shyam@gmail.com', 'top', 'tfdsfu!nfttbhf', 'sent', 'static/media/assassins.png'),
(164, '2019-11-05', 'manu@gmail.com', 'shyam@gmail.com', '1452', 'tihtikjd', 'sent', 'static/media/edit%20forms%20data_cvpNFIm.jpg'),
(166, '2019-11-05', 'manu@gmail.com', 'shyam@gmail.com', 'draftme', ' hcwhg', 'sent', 'static/media/Annotation%202019-09-02%20105917.jpg'),
(167, '2019-11-05', 'shyam@gmail.com', 'manu@gmail.com', 'shfhdg', 'khiwik', 'sent', 'static/media/hide123456.png');

-- --------------------------------------------------------

--
-- Table structure for table `registration`
--

CREATE TABLE `registration` (
  `uid` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `address` varchar(100) NOT NULL,
  `dob` varchar(20) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `mobile` varchar(20) NOT NULL,
  `email` varchar(100) NOT NULL,
  `image` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `answer` varchar(20) NOT NULL,
  `status` varchar(25) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `registration`
--

INSERT INTO `registration` (`uid`, `name`, `address`, `dob`, `gender`, `mobile`, `email`, `image`, `password`, `answer`, `status`) VALUES
(17, 'shyam', 'omangalathu', '1994-03-14', 'male', '9633710717', 'shyam@gmail.com', 'static/media/shyam%20pass.jpg', '1', 'red', 'approved'),
(18, 'manu', 'manuvilas', '1998-01-11', 'male', '9856321472', 'manu@gmail.com', 'static/media/myAvatar.png', 'manu', 'green', 'approved');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`a_id`);

--
-- Indexes for table `feedback`
--
ALTER TABLE `feedback`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `message`
--
ALTER TABLE `message`
  ADD PRIMARY KEY (`mid`);

--
-- Indexes for table `registration`
--
ALTER TABLE `registration`
  ADD PRIMARY KEY (`uid`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `a_id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `feedback`
--
ALTER TABLE `feedback`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT for table `message`
--
ALTER TABLE `message`
  MODIFY `mid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=168;

--
-- AUTO_INCREMENT for table `registration`
--
ALTER TABLE `registration`
  MODIFY `uid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
