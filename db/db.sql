-- MySQL dump 10.13  Distrib 8.0.23, for Win64 (x86_64)
--
-- Host: localhost    Database: crime_detection
-- ------------------------------------------------------
-- Server version	8.0.23

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `advocate_info`
--

DROP TABLE IF EXISTS `advocate_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `advocate_info` (
  `aid` int NOT NULL AUTO_INCREMENT,
  `lid` int DEFAULT NULL,
  `enrolment_year` varchar(45) NOT NULL,
  `practice_place` varchar(45) NOT NULL,
  `created_on` datetime NOT NULL,
  PRIMARY KEY (`aid`),
  KEY `lid_idx` (`lid`),
  CONSTRAINT `advocate_info_ibfk_1` FOREIGN KEY (`lid`) REFERENCES `login` (`lid`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `advocate_info`
--

LOCK TABLES `advocate_info` WRITE;
/*!40000 ALTER TABLE `advocate_info` DISABLE KEYS */;
INSERT INTO `advocate_info` VALUES (2,26,'2022-01-21','place','2022-01-21 15:05:46'),(5,34,'2022-01-25','ernakalum','2022-01-25 19:05:09'),(6,35,'2022-02-02','kozhikode','2022-02-02 12:35:35'),(7,36,'2022-02-02','kozhikode','2022-02-02 12:36:31'),(8,48,'2024-02-25','kerala','2024-02-25 21:44:57');
/*!40000 ALTER TABLE `advocate_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `advocate_rating`
--

DROP TABLE IF EXISTS `advocate_rating`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `advocate_rating` (
  `Advocate_rating_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `adv_id` int NOT NULL,
  `rating` int NOT NULL,
  `created_on` datetime NOT NULL,
  PRIMARY KEY (`Advocate_rating_id`),
  KEY `user_id_idx` (`user_id`),
  KEY `adv_id_idx` (`adv_id`),
  CONSTRAINT `advocate_rating_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `login` (`lid`),
  CONSTRAINT `advocate_rating_ibfk_2` FOREIGN KEY (`adv_id`) REFERENCES `login` (`lid`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `advocate_rating`
--

LOCK TABLES `advocate_rating` WRITE;
/*!40000 ALTER TABLE `advocate_rating` DISABLE KEYS */;
INSERT INTO `advocate_rating` VALUES (1,32,34,5,'2022-01-26 11:35:12'),(2,37,34,5,'2022-02-05 14:41:25'),(6,32,36,1,'2022-02-05 16:57:45'),(7,32,35,3,'2022-02-05 19:15:34'),(8,32,36,5,'2022-02-05 19:15:47'),(10,32,35,1,'2022-02-07 17:59:40'),(11,32,36,1,'2022-02-07 18:01:00'),(12,32,35,1,'2022-02-07 18:04:01'),(13,32,34,5,'2022-02-07 18:05:40');
/*!40000 ALTER TABLE `advocate_rating` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `advocate_request`
--

DROP TABLE IF EXISTS `advocate_request`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `advocate_request` (
  `ar_id` int NOT NULL AUTO_INCREMENT,
  `req_id` int NOT NULL,
  `adv_id` int NOT NULL,
  `request_type` varchar(45) NOT NULL,
  `case_id` int NOT NULL,
  `created_on` datetime NOT NULL,
  `status` varchar(45) NOT NULL,
  PRIMARY KEY (`ar_id`),
  KEY `req_id_idx` (`req_id`),
  KEY `adv_id_idx` (`adv_id`),
  KEY `case_id_idx` (`case_id`),
  CONSTRAINT `adv_id` FOREIGN KEY (`adv_id`) REFERENCES `login` (`lid`),
  CONSTRAINT `case_id` FOREIGN KEY (`case_id`) REFERENCES `cases` (`case_id`) ON DELETE CASCADE,
  CONSTRAINT `req_id` FOREIGN KEY (`req_id`) REFERENCES `login` (`lid`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `advocate_request`
--

LOCK TABLES `advocate_request` WRITE;
/*!40000 ALTER TABLE `advocate_request` DISABLE KEYS */;
INSERT INTO `advocate_request` VALUES (2,53,36,'medium',6,'2024-03-10 13:29:15','pending'),(3,37,35,'jjj',6,'2024-03-10 14:43:45','pending'),(4,53,35,'individual',7,'2024-03-17 21:35:30','pending'),(5,53,34,'petty',6,'2024-03-17 21:35:59','pending'),(6,53,34,'quick',6,'2024-03-18 10:07:34','pending'),(7,32,35,'oppose',6,'2024-03-18 20:33:25','pending');
/*!40000 ALTER TABLE `advocate_request` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `case_against_individuals`
--

DROP TABLE IF EXISTS `case_against_individuals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `case_against_individuals` (
  `c_id` int NOT NULL AUTO_INCREMENT,
  `case_type` varchar(45) NOT NULL,
  `name` varchar(45) NOT NULL,
  `phone` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  `parent_name` varchar(45) NOT NULL,
  `details` varchar(45) NOT NULL,
  `created_on` text NOT NULL,
  PRIMARY KEY (`c_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `case_against_individuals`
--

LOCK TABLES `case_against_individuals` WRITE;
/*!40000 ALTER TABLE `case_against_individuals` DISABLE KEYS */;
INSERT INTO `case_against_individuals` VALUES (1,'individual case','raju','8978767876','raju@gmail.com','sree ram','test','2022-02-04 14:29:41.899901');
/*!40000 ALTER TABLE `case_against_individuals` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `case_involve`
--

DROP TABLE IF EXISTS `case_involve`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `case_involve` (
  `cid` int NOT NULL AUTO_INCREMENT,
  `c_id` int NOT NULL,
  `name` varchar(45) NOT NULL,
  `phone` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  `address` varchar(45) NOT NULL,
  `parent_name` varchar(45) NOT NULL,
  `details` text NOT NULL,
  `created_on` datetime NOT NULL,
  PRIMARY KEY (`cid`),
  KEY `c_id_idx` (`c_id`),
  CONSTRAINT `case_involve_ibfk_1` FOREIGN KEY (`c_id`) REFERENCES `case_against_individuals` (`c_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `case_involve`
--

LOCK TABLES `case_involve` WRITE;
/*!40000 ALTER TABLE `case_involve` DISABLE KEYS */;
INSERT INTO `case_involve` VALUES (3,1,'case invovles','8978767876','sample@gmail.com','test','sree ram','test','2022-02-05 19:41:18'),(4,1,'Kumar','8989898989','kumar@gmail.com','Kateel junction','kannan','IPC-346','2024-03-10 13:03:07'),(8,1,'ankush','9899898989','ankush@gmail.com','bajpe ','ankith','narcotics dealer','2024-03-18 19:55:02'),(9,1,'nikhil','9898080800','nik@gmail.com','bajpe','anand','gold roberry','2024-03-18 20:10:40'),(10,1,'anand','7979797797','anand@gmail.com','kenjar,bajpe','ambadi','dealer of drugs ','2024-03-18 21:04:05');
/*!40000 ALTER TABLE `case_involve` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `case_involves`
--

DROP TABLE IF EXISTS `case_involves`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `case_involves` (
  `ci_id` int NOT NULL AUTO_INCREMENT,
  `c_id` int NOT NULL,
  `name` varchar(45) NOT NULL,
  `phone` varchar(30) NOT NULL,
  `email` varchar(45) NOT NULL,
  `address` varchar(45) NOT NULL,
  `parent_name` varchar(45) NOT NULL,
  `details` text NOT NULL,
  `created_on` datetime NOT NULL,
  PRIMARY KEY (`ci_id`),
  KEY `c_id_idx` (`c_id`),
  CONSTRAINT `c_id` FOREIGN KEY (`c_id`) REFERENCES `cases` (`case_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `case_involves`
--

LOCK TABLES `case_involves` WRITE;
/*!40000 ALTER TABLE `case_involves` DISABLE KEYS */;
/*!40000 ALTER TABLE `case_involves` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cases`
--

DROP TABLE IF EXISTS `cases`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cases` (
  `case_id` int NOT NULL AUTO_INCREMENT,
  `case_type` varchar(45) NOT NULL,
  `case_involver` varchar(45) NOT NULL,
  `number` varchar(12) NOT NULL,
  `subject` varchar(45) NOT NULL,
  `content` text NOT NULL,
  `location` varchar(45) NOT NULL,
  `s_id` int NOT NULL,
  `created_on` datetime NOT NULL,
  PRIMARY KEY (`case_id`),
  KEY `s_id_idx` (`s_id`),
  KEY `c_in_idx` (`case_involver`),
  CONSTRAINT `s_id` FOREIGN KEY (`s_id`) REFERENCES `station` (`s_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cases`
--

LOCK TABLES `cases` WRITE;
/*!40000 ALTER TABLE `cases` DISABLE KEYS */;
INSERT INTO `cases` VALUES (6,'individual case','sagar','8989898987','Accident','Run away after accident','Kateel',15,'2024-03-10 13:03:07'),(7,'petty','suman','7878767890','smoke at public place','smoke at public place is an offence','kateel',15,'2024-03-10 14:30:28'),(8,'individual case','akil','890987867','narcotics ','narcotics dealer','bajpe,ekenjar',8,'2024-03-18 19:55:02'),(9,'individual case','nikhil','8987898767','robbing ','home roberry','bajpe,kenjar',8,'2024-03-18 20:10:40'),(10,'individual case','anand','898767890','drug dealings','dealer of drugs ','kenjar, near sdit',8,'2024-03-18 21:04:05');
/*!40000 ALTER TABLE `cases` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `complaint_against_advocate`
--

DROP TABLE IF EXISTS `complaint_against_advocate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `complaint_against_advocate` (
  `complaint_against_id` int NOT NULL AUTO_INCREMENT,
  `complainant_id` int NOT NULL,
  `adv_id` int NOT NULL,
  `complaint` text NOT NULL,
  `created_on` datetime NOT NULL,
  PRIMARY KEY (`complaint_against_id`),
  KEY `complainant_id_idx` (`complainant_id`),
  KEY `adv_id_idx` (`adv_id`),
  CONSTRAINT `complaint_against_advocate_ibfk_1` FOREIGN KEY (`complainant_id`) REFERENCES `login` (`lid`),
  CONSTRAINT `complaint_against_advocate_ibfk_2` FOREIGN KEY (`adv_id`) REFERENCES `login` (`lid`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `complaint_against_advocate`
--

LOCK TABLES `complaint_against_advocate` WRITE;
/*!40000 ALTER TABLE `complaint_against_advocate` DISABLE KEYS */;
INSERT INTO `complaint_against_advocate` VALUES (3,32,34,'against advocate','2022-01-26 13:16:01'),(4,37,34,'saji advocate is not responding for case related issues','2024-01-20 21:12:50'),(5,53,36,'advocate not responding','2024-03-09 17:31:07');
/*!40000 ALTER TABLE `complaint_against_advocate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `complaints_feedback`
--

DROP TABLE IF EXISTS `complaints_feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `complaints_feedback` (
  `complaints_feedback_id` int NOT NULL AUTO_INCREMENT,
  `complainant_id` int NOT NULL,
  `complaint` text NOT NULL,
  `reply` text,
  `created_on` datetime NOT NULL,
  `replied_on` date DEFAULT NULL,
  PRIMARY KEY (`complaints_feedback_id`),
  KEY `complainant_id_idx` (`complainant_id`),
  CONSTRAINT `complainant_id` FOREIGN KEY (`complainant_id`) REFERENCES `login` (`lid`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `complaints_feedback`
--

LOCK TABLES `complaints_feedback` WRITE;
/*!40000 ALTER TABLE `complaints_feedback` DISABLE KEYS */;
INSERT INTO `complaints_feedback` VALUES (3,32,'test','hello','2022-02-03 14:50:13','2022-02-03'),(4,32,'testtt','complaint replay','2022-02-03 14:50:19','2022-02-03'),(5,32,'another complaint','will inform later','2022-02-03 15:52:00','2022-02-07'),(6,37,'need to improve the complaint section in system\r\n','ok','2024-01-20 21:08:39','2024-02-28');
/*!40000 ALTER TABLE `complaints_feedback` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `login`
--

DROP TABLE IF EXISTS `login`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `login` (
  `lid` int NOT NULL AUTO_INCREMENT,
  `username` varchar(45) NOT NULL,
  `password` varchar(45) NOT NULL,
  `provisionized` tinyint NOT NULL,
  `type` varchar(45) NOT NULL,
  `created_on` datetime NOT NULL,
  PRIMARY KEY (`lid`)
) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login`
--

LOCK TABLES `login` WRITE;
/*!40000 ALTER TABLE `login` DISABLE KEYS */;
INSERT INTO `login` VALUES (12,'admin','admin',1,'admin','2022-01-20 11:06:45'),(15,'Sreeshma','BRD98tOVkz',1,'police','2022-01-20 16:15:57'),(23,'Arya','QP2U94yszc',1,'police','2022-01-21 12:08:12'),(24,'Arjun','0UHWHfDCgv',0,'police','2022-01-21 13:14:56'),(26,'advocate','sZwfMC0CtF',1,'advocate_admin','2022-01-21 15:05:46'),(28,'test','BhjFjOJ60o',0,'police','2022-01-25 12:33:03'),(30,'employeetwo','vCvZilEDRl',1,'station_admin','2022-01-25 14:05:10'),(32,'user','eP08YeVYCl',1,'user','2022-01-25 16:30:51'),(34,'saji','i5z0b1m4Eh',1,'advocate','2022-01-25 19:05:09'),(35,'sreeraju','dhZCxI1wUc',1,'advocate','2022-02-02 12:35:35'),(36,'anu','h0cRkw41AD',1,'advocate','2022-02-02 12:36:31'),(37,'surya','JOevAtuIDj',1,'user','2022-02-03 16:00:10'),(40,'sample','5EoflDV4PD',0,'police','2022-02-08 13:19:33'),(44,'sample','zz1incUQcs',0,'police','2022-02-08 17:35:05'),(47,'admin','admin',1,'admin','2022-02-08 17:35:05'),(48,'maneesh','auzAV8zusr',0,'advocate','2024-02-25 21:44:57'),(49,'nikshith','hndg6HGgQQ',0,'user','2024-02-25 21:46:50'),(50,'Athul','PRhdT9msRp',1,'station_admin','2024-03-09 14:32:01'),(51,'Nikhil','O7TO2pfNIz',0,'police','2024-03-09 14:36:19'),(53,'Bhumi','D4gp1QQVqn',1,'user','2024-03-09 14:42:20'),(54,'Akil Dev','FrzeaIsHYr',0,'user','2024-03-17 20:24:09'),(55,'Manjunatha','6TGihu3YFQ',0,'police','2024-03-25 13:25:26');
/*!40000 ALTER TABLE `login` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `normal_complaints`
--

DROP TABLE IF EXISTS `normal_complaints`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `normal_complaints` (
  `Normal_complaints_id` int NOT NULL AUTO_INCREMENT,
  `complainant_id` int NOT NULL,
  `case_subject` varchar(45) NOT NULL,
  `complaint` text NOT NULL,
  `status` varchar(45) NOT NULL,
  `created_on` datetime NOT NULL,
  PRIMARY KEY (`Normal_complaints_id`),
  KEY `complainant_id_idx` (`complainant_id`),
  CONSTRAINT `normal_complaints_ibfk_1` FOREIGN KEY (`complainant_id`) REFERENCES `login` (`lid`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `normal_complaints`
--

LOCK TABLES `normal_complaints` WRITE;
/*!40000 ALTER TABLE `normal_complaints` DISABLE KEYS */;
INSERT INTO `normal_complaints` VALUES (3,37,'Accident case','An accident was done athe road side today morning at bajpe ','accepted','2024-01-20 20:42:07'),(4,37,'fight at kavoor ','bus vs bus fight at kavoor','accepted','2024-01-20 21:08:07');
/*!40000 ALTER TABLE `normal_complaints` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `personalised_complaints`
--

DROP TABLE IF EXISTS `personalised_complaints`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `personalised_complaints` (
  `Personalised_complaints_id` int NOT NULL AUTO_INCREMENT,
  `complainant_id` int NOT NULL,
  `complaint` text NOT NULL,
  `name` varchar(45) NOT NULL,
  `phone` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  `parenetname` varchar(45) NOT NULL,
  `status` varchar(45) NOT NULL,
  `created_on` datetime NOT NULL,
  PRIMARY KEY (`Personalised_complaints_id`),
  KEY `complainant_id_idx` (`complainant_id`),
  CONSTRAINT `personalised_complaints_ibfk_1` FOREIGN KEY (`complainant_id`) REFERENCES `login` (`lid`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `personalised_complaints`
--

LOCK TABLES `personalised_complaints` WRITE;
/*!40000 ALTER TABLE `personalised_complaints` DISABLE KEYS */;
INSERT INTO `personalised_complaints` VALUES (3,32,'hey','','','','','accept','2022-02-01 17:34:21'),(4,37,'i have one test case','','','','','accepted','2024-01-20 21:09:49'),(5,53,'test personalized  complaint','','','','','accepted','2024-03-09 14:49:43'),(6,53,'narcotics dealer','nikhil','8989898989','nikhil@gmail.com','anand','pending','2024-03-18 20:19:38');
/*!40000 ALTER TABLE `personalised_complaints` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quick_complaint`
--

DROP TABLE IF EXISTS `quick_complaint`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `quick_complaint` (
  `qc_id` int NOT NULL AUTO_INCREMENT,
  `lid` int NOT NULL,
  `complaint` text NOT NULL,
  `image` text NOT NULL,
  `created_on` datetime NOT NULL,
  PRIMARY KEY (`qc_id`),
  KEY `lid_idx` (`lid`),
  CONSTRAINT `quick_complaint_ibfk_1` FOREIGN KEY (`lid`) REFERENCES `login` (`lid`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quick_complaint`
--

LOCK TABLES `quick_complaint` WRITE;
/*!40000 ALTER TABLE `quick_complaint` DISABLE KEYS */;
INSERT INTO `quick_complaint` VALUES (2,37,'Accident happend at Kenjar','accident1.jpg','2024-01-20 20:44:48'),(4,53,'Forest fire at kenjar','ForestFires.jpg','2024-03-09 14:48:08');
/*!40000 ALTER TABLE `quick_complaint` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `registration`
--

DROP TABLE IF EXISTS `registration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registration` (
  `id` int NOT NULL AUTO_INCREMENT,
  `lid` int NOT NULL,
  `name` varchar(45) NOT NULL,
  `gender` varchar(45) NOT NULL,
  `dob` date NOT NULL,
  `email` varchar(45) NOT NULL,
  `phone` varchar(11) NOT NULL,
  `address` varchar(45) NOT NULL,
  `adharnumber` varchar(45) NOT NULL,
  `occupation` varchar(45) NOT NULL,
  `image` text NOT NULL,
  `created_on` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `lid_idx` (`lid`),
  CONSTRAINT `lid` FOREIGN KEY (`lid`) REFERENCES `login` (`lid`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registration`
--

LOCK TABLES `registration` WRITE;
/*!40000 ALTER TABLE `registration` DISABLE KEYS */;
INSERT INTO `registration` VALUES (1,15,'Sreeshma','female','2022-01-20','sreeshmac200@gmail.com','6545678909','test','56789098765','DGP','port-arthur-1584098_1920.jpg','2022-01-20 16:15:57'),(9,23,'Arya','female','2022-01-21','arya@gmail.com','5678987678','address','5555555555','SI','port-arthur-1584098_1920.jpg','2022-01-21 12:08:12'),(10,24,'Arjunc','male','1891-01-21','arjun@gmail.com','7867567898','test','44444','SI','dlpng_com_Tech_background_elements_png_download_-_1425_704_-_Free_____6343401.png','2022-01-21 13:14:56'),(12,26,'advocate','male','2022-01-21','advocate@gmail.com','8978987890','test','2022-01-21','place','noun-product-3407444.png','2022-01-21 15:05:46'),(14,28,'test','female','2022-01-25','test@gmail.com','6789098909','test','76678987898','SI','cae1.jpg','2022-01-25 12:33:03'),(16,30,'employeetwo','male','2022-01-25','test@gmail.com','6789876789','test','78978908765','SI','patrick-sun-QGKwUaaTWyc-unsplash.jpg','2022-01-25 14:05:10'),(18,32,'user','female','2022-01-25','usertest@gmail.com','8967568789','test','888888888','driver','eng_design7.jpg','2022-01-25 16:30:51'),(20,34,'saji','male','2022-01-25','advocate4@gmail.com','8978767876','test','66666666666','advocate','img-4.png','2022-01-25 19:05:09'),(21,35,'sreeraju','male','2022-02-02','sample@gmail.com','8978767876','address','67896555455','advocate','img.png','2022-02-02 12:35:35'),(22,36,'anu','female','2022-02-02','anu@gmail.com','8978767876','address','567868999997','advocate','20220108_154012.jpg','2022-02-02 12:36:31'),(23,37,'surya thejas','male','2022-02-03','testtejas@gmail.com','8978767879','thejas kavoor','88888888888','driver','cutting-metal.jpg','2022-02-03 16:00:10'),(28,44,'sample','female','2022-02-08','test@gmail.com','8978767876','test','66666666666','SI','eng_design7.jpg','2022-02-08 17:35:05'),(31,48,'maneesh','male','2006-09-19','mani2@gmail.com','8989898989','kasaragod','9090909090','advocate','Maneesh.jpg','2024-02-25 21:44:57'),(32,49,'nikshith','male','2024-02-25','nikshi@gmail.com','98999979797','kkkajja','8898998999','nothing','Maneesh_M_-_Intro_to_Programming.png','2024-02-25 21:46:50'),(33,50,'Athul','male','2024-03-09','athul@gmail.com','9898989898','athul kozhikode','898989898989','Constable','login-bg.jpg','2024-03-09 14:32:01'),(34,51,'Nikhil','male','2024-03-14','nikhil@gmail.com','7878787878','Nikhil thomas roi','787878787879','Police Constable','login-bg.jpg','2024-03-09 14:36:19'),(36,53,'Bhumi','female','2024-03-15','bhumi@gmail.com','8989898989','bhumi kateel','878787878787','SE','login-bg.jpg','2024-03-09 14:42:20'),(37,54,'Akil Dev','male','2004-03-11','akil@gmail.com','9090909090','akil Dev Kavoor','898989989909','Painter','Maneesh.jpg','2024-03-17 20:24:09'),(38,55,'Manjunatha','male','2004-03-15','manju@gmail.com','8989878987','chowki kasaragod','787878787878','CI','A7303476cropped.JPG','2024-03-25 13:25:26');
/*!40000 ALTER TABLE `registration` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `station`
--

DROP TABLE IF EXISTS `station`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `station` (
  `s_id` int NOT NULL AUTO_INCREMENT,
  `sh_id` int NOT NULL,
  `name` varchar(45) NOT NULL,
  `address` varchar(45) NOT NULL,
  `member` int NOT NULL,
  `created_on` datetime NOT NULL,
  PRIMARY KEY (`s_id`),
  KEY `sh_id_idx` (`sh_id`),
  CONSTRAINT `sh_id` FOREIGN KEY (`sh_id`) REFERENCES `login` (`lid`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `station`
--

LOCK TABLES `station` WRITE;
/*!40000 ALTER TABLE `station` DISABLE KEYS */;
INSERT INTO `station` VALUES (8,12,'kenjar','Kenjar Station',46,'2022-01-21 11:06:07'),(9,12,'Kadri Station','Near Pumpvail',100,'2022-01-21 11:06:18'),(15,12,'kateel','near kateel temple',100,'2024-03-08 23:00:33');
/*!40000 ALTER TABLE `station` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `station_user_map`
--

DROP TABLE IF EXISTS `station_user_map`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `station_user_map` (
  `su_id` int NOT NULL AUTO_INCREMENT,
  `lid` int NOT NULL,
  `s_id` int NOT NULL,
  `created_on` datetime NOT NULL,
  PRIMARY KEY (`su_id`),
  KEY `lid_idx` (`lid`),
  KEY `s_id_idx` (`s_id`),
  CONSTRAINT `station_user_map_ibfk_1` FOREIGN KEY (`lid`) REFERENCES `login` (`lid`),
  CONSTRAINT `station_user_map_ibfk_2` FOREIGN KEY (`s_id`) REFERENCES `station` (`s_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `station_user_map`
--

LOCK TABLES `station_user_map` WRITE;
/*!40000 ALTER TABLE `station_user_map` DISABLE KEYS */;
INSERT INTO `station_user_map` VALUES (5,23,8,'2022-01-21 12:08:12'),(9,30,8,'2022-01-25 14:05:10'),(21,50,15,'2024-03-09 14:32:01'),(22,51,15,'2024-03-09 14:36:19'),(24,53,15,'2024-03-09 14:42:20'),(26,55,15,'2024-03-25 13:25:26');
/*!40000 ALTER TABLE `station_user_map` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-06-13 21:29:08
