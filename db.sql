DROP database if exists beltline;
CREATE DATABASE  IF NOT EXISTS `beltline` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */;
USE `beltline`;
-- MySQL dump 10.13  Distrib 8.0.13, for Win64 (x86_64)
--
-- Host: localhost    Database: beltline
-- ------------------------------------------------------
-- Server version	8.0.13

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `administrator`
--

DROP TABLE IF EXISTS `administrator`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `administrator` (
  `Username` varchar(20) NOT NULL,
  PRIMARY KEY (`Username`),
  CONSTRAINT `administrator_ibfk_1` FOREIGN KEY (`Username`) REFERENCES `employee` (`username`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `administrator`
--

LOCK TABLES `administrator` WRITE;
/*!40000 ALTER TABLE `administrator` DISABLE KEYS */;
INSERT INTO `administrator` VALUES ('james.smith');
/*!40000 ALTER TABLE `administrator` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `assign_to`
--

DROP TABLE IF EXISTS `assign_to`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `assign_to` (
  `Username` varchar(20) NOT NULL,
  `Name` varchar(50) NOT NULL,
  `StartDate` date NOT NULL,
  `SiteName` varchar(50) NOT NULL,
  PRIMARY KEY (`Username`,`Name`,`StartDate`,`SiteName`),
  KEY `Name` (`Name`,`StartDate`,`SiteName`),
  CONSTRAINT `assign_to_ibfk_1` FOREIGN KEY (`Name`, `StartDate`, `SiteName`) REFERENCES `event` (`name`, `startdate`, `sitename`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `assign_to_ibfk_2` FOREIGN KEY (`Username`) REFERENCES `staff` (`username`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assign_to`
--

LOCK TABLES `assign_to` WRITE;
/*!40000 ALTER TABLE `assign_to` DISABLE KEYS */;
INSERT INTO `assign_to` VALUES ('staff3','Arboretum Walking Tour','2019-02-08','Inman Park'),('michael.smith','Bus Tour','2019-02-01','Inman Park'),('staff2','Bus Tour','2019-02-01','Inman Park'),('michael.smith','Bus Tour','2019-02-08','Inman Park'),('robert.smith','Bus Tour','2019-02-08','Inman Park'),('robert.smith','Eastside Trail','2019-02-04','Inman Park'),('staff2','Eastside Trail','2019-02-04','Inman Park'),('michael.smith','Eastside Trail','2019-02-04','Piedmont Park'),('staff1','Eastside Trail','2019-02-04','Piedmont Park'),('michael.smith','Eastside Trail','2019-02-13','Historic Fourth Ward Park'),('staff1','Eastside Trail','2019-03-01','Inman Park'),('staff1','Official Atlanta BeltLine Bike Tour','2019-02-09','Atlanta BeltLine Center'),('robert.smith','Private Bus Tour','2019-02-01','Inman Park'),('staff1','Westside Trail','2019-02-18','Westview Cemetery'),('staff3','Westside Trail','2019-02-18','Westview Cemetery');
/*!40000 ALTER TABLE `assign_to` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `connect`
--

DROP TABLE IF EXISTS `connect`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `connect` (
  `TransitType` varchar(10) NOT NULL,
  `TransitRoute` varchar(18) NOT NULL,
  `SiteName` varchar(50) NOT NULL,
  PRIMARY KEY (`TransitType`,`TransitRoute`,`SiteName`),
  KEY `SiteName` (`SiteName`),
  CONSTRAINT `connect_ibfk_1` FOREIGN KEY (`TransitType`, `TransitRoute`) REFERENCES `transit` (`transittype`, `transitroute`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `connect_ibfk_2` FOREIGN KEY (`SiteName`) REFERENCES `site` (`name`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `connect`
--

LOCK TABLES `connect` WRITE;
/*!40000 ALTER TABLE `connect` DISABLE KEYS */;
INSERT INTO `connect` VALUES ('Bike','Relay','Historic Fourth Ward Park'),('Bus','152','Historic Fourth Ward Park'),('MARTA','Blue','Historic Fourth Ward Park'),('Bus','152','Inman Park'),('MARTA','Blue','Inman Park'),('Bike','Relay','Piedmont Park'),('Bus','152','Piedmont Park'),('MARTA','Blue','Piedmont Park'),('MARTA','Blue','Westview Cemetery');
/*!40000 ALTER TABLE `connect` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `email`
--

DROP TABLE IF EXISTS `email`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `email` (
  `Username` varchar(20) NOT NULL,
  `EMAIL` varchar(320) NOT NULL,
  PRIMARY KEY (`EMAIL`),
  UNIQUE KEY `EMAIL` (`EMAIL`),
  KEY `Username` (`Username`),
  CONSTRAINT `email_ibfk_1` FOREIGN KEY (`Username`) REFERENCES `user` (`username`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `email`
--

LOCK TABLES `email` WRITE;
/*!40000 ALTER TABLE `email` DISABLE KEYS */;
INSERT INTO `email` VALUES ('david.smith','dsmith@outlook.com'),('james.smith','jsmith@gatech.edu'),('james.smith','jsmith@gmail.com'),('james.smith','jsmith@hotmail.com'),('james.smith','jsmith@outlook.com'),('manager1','m1@beltline.com'),('manager2','m2@beltline.com'),('manager3','m3@beltline.com'),('manager4','m4@beltline.com'),('manager5','m5@beltline.com'),('maria.garcia','mgarcia@gatech.edu'),('maria.garcia','mgarcia@yahoo.com'),('maria.hernandez','mh@gatech.edu'),('maria.hernandez','mh123@gmail.com'),('maria.rodriguez','mrodriguez@gmail.com'),('mary.smith','mary@outlook.com'),('michael.smith','msmith@gmail.com'),('robert.smith','rsmith@hotmail.com'),('staff1','s1@beltline.com'),('staff2','s2@beltline.com'),('staff3','s3@beltline.com'),('user1','u1@beltline.com'),('visitor1','v1@beltline.com');
/*!40000 ALTER TABLE `email` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee`
--

DROP TABLE IF EXISTS `employee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `employee` (
  `Username` varchar(20) NOT NULL,
  `EMPLOYEEID` char(9) NOT NULL,
  `Phone` char(12) NOT NULL,
  `Address` varchar(50) NOT NULL,
  `City` varchar(20) NOT NULL,
  `State` char(2) NOT NULL,
  `Zipcode` char(5) NOT NULL,
  PRIMARY KEY (`Username`),
  UNIQUE KEY `EMPLOYEEID` (`EMPLOYEEID`),
  UNIQUE KEY `Phone` (`Phone`),
  CONSTRAINT `employee_ibfk_1` FOREIGN KEY (`Username`) REFERENCES `user` (`username`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee`
--

LOCK TABLES `employee` WRITE;
/*!40000 ALTER TABLE `employee` DISABLE KEYS */;
INSERT INTO `employee` VALUES ('david.smith','5','5124776435','350 Ferst Drive','Atlanta','GA','30332'),('james.smith','1','4043721234','123 East Main Street','Rochester','NY','14604'),('manager1','6','8045126767','123 East Main Street','Rochester','NY','14604'),('manager2','7','9876543210','123 East Main Street','Rochester','NY','14604'),('manager3','8','5432167890','350 Ferst Drive','Atlanta','GA','30332'),('manager4','9','8053467565','123 East Main Street','Columbus','OH','43215'),('manager5','10','8031446782','801 Atlantic Drive','Atlanta','GA','30332'),('maria.garcia','4','7890123456','123 East Main Street','Richland','PA','17987'),('michael.smith','2','4043726789','350 Ferst Drive','Atlanta','GA','30332'),('robert.smith','3','1234567890','123 East Main Street','Columbus','OH','43215'),('staff1','11','8024456765','266 Ferst Drive Northwest','Atlanta','GA','30332'),('staff2','12','8888888888','266 Ferst Drive Northwest','Atlanta','GA','30332'),('staff3','13','3333333333','801 Atlantic Drive','Atlanta','GA','30332');
/*!40000 ALTER TABLE `employee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event`
--

DROP TABLE IF EXISTS `event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `event` (
  `Name` varchar(50) NOT NULL,
  `StartDate` date NOT NULL,
  `SiteName` varchar(50) NOT NULL,
  `Capacity` int(4) unsigned NOT NULL,
  `Price` decimal(6,2) unsigned NOT NULL,
  `EndDate` date NOT NULL,
  `Description` text,
  `MinStaffReq` int(4) unsigned NOT NULL,
  PRIMARY KEY (`Name`,`StartDate`,`SiteName`),
  KEY `SiteName` (`SiteName`),
  CONSTRAINT `event_ibfk_1` FOREIGN KEY (`SiteName`) REFERENCES `site` (`name`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event`
--

LOCK TABLES `event` WRITE;
/*!40000 ALTER TABLE `event` DISABLE KEYS */;
INSERT INTO `event` VALUES ('Arboretum Walking Tour','2019-02-08','Inman Park',5,5.00,'2019-02-11','Official Atlanta BeltLine Arboretum Walking Tours provide an up-close view of the Westside Trail and the Atlanta BeltLine Arboretum led by Trees Atlanta Docents. The one and a half hour tours step off at at 10am (Oct thru May), and 9am (June thru September). Departure for all tours is from Rose Circle Park near Brown Middle School. More details at: https://beltline.org/visit/atlanta-beltline-tours/#arboretum-walking',1),('Bus Tour','2019-02-01','Inman Park',6,25.00,'2019-02-02','The Atlanta BeltLine Partnership’s tour program operates with a natural gas-powered, ADA accessible tour bus funded through contributions from 10th & Monroe, LLC, SunTrust Bank Trusteed Foundations – Florence C. and Harry L. English Memorial Fund and Thomas Guy Woolford Charitable Trust, and AGL Resources',2),('Bus Tour','2019-02-08','Inman Park',6,25.00,'2019-02-10','The Atlanta BeltLine Partnership’s tour program operates with a natural gas-powered, ADA accessible tour bus funded through contributions from 10th & Monroe, LLC, SunTrust Bank Trusteed Foundations – Florence C. and Harry L. English Memorial Fund and Thomas Guy Woolford Charitable Trust, and AGL Resources',2),('Eastside Trail','2019-02-04','Inman Park',99999,0.00,'2019-02-05','A combination of multi-use trail and linear greenspace, the Eastside Trail was the first finished section of the Atlanta BeltLine trail in the old rail corridor. The Eastside Trail, which was funded by a combination of public and private philanthropic sources, runs from the tip of Piedmont Park to Reynoldstown. More details at https://beltline.org/explore-atlanta-beltline-trails/eastside-trail/',1),('Eastside Trail','2019-02-04','Piedmont Park',99999,0.00,'2019-02-05','A combination of multi-use trail and linear greenspace, the Eastside Trail was the first finished section of the Atlanta BeltLine trail in the old rail corridor. The Eastside Trail, which was funded by a combination of public and private philanthropic sources, runs from the tip of Piedmont Park to Reynoldstown. More details at https://beltline.org/explore-atlanta-beltline-trails/eastside-trail/',1),('Eastside Trail','2019-02-13','Historic Fourth Ward Park',99999,0.00,'2019-02-14','A combination of multi-use trail and linear greenspace, the Eastside Trail was the first finished section of the Atlanta BeltLine trail in the old rail corridor. The Eastside Trail, which was funded by a combination of public and private philanthropic sources, runs from the tip of Piedmont Park to Reynoldstown. More details at https://beltline.org/explore-atlanta-beltline-trails/eastside-trail/',1),('Eastside Trail','2019-03-01','Inman Park',99999,0.00,'2019-03-02','A combination of multi-use trail and linear greenspace, the Eastside Trail was the first finished section of the Atlanta BeltLine trail in the old rail corridor. The Eastside Trail, which was funded by a combination of public and private philanthropic sources, runs from the tip of Piedmont Park to Reynoldstown. More details at https://beltline.org/explore-atlanta-beltline-trails/eastside-trail/',1),('Official Atlanta BeltLine Bike Tour','2019-02-09','Atlanta BeltLine Center',5,5.00,'2019-02-14','These tours will include rest stops highlighting assets and points of interest along the Atlanta BeltLine. Staff will lead the rides, and each group will have a ride sweep to help with any unexpected mechanical difficulties.',1),('Private Bus Tour','2019-02-01','Inman Park',4,40.00,'2019-02-02','Private tours are available most days, pending bus and tour guide availability. Private tours can accommodate up to 4 guests per tour, and are subject to a tour fee (nonprofit rates are available). As a nonprofit organization with limited resources, we are unable to offer free private tours. We thank you for your support and your understanding as we try to provide as many private group tours as possible. The Atlanta BeltLine Partnership’s tour program operates with a natural gas-powered, ADA accessible tour bus funded through contributions from 10th & Monroe, LLC, SunTrust Bank Trusteed Foundations – Florence C. and Harry L. English Memorial Fund and Thomas Guy Woolford Charitable Trust, and AGL Resources',1),('Westside Trail','2019-02-18','Westview Cemetery',99999,0.00,'2019-02-21','The Westside Trail is a free amenity that offers a bicycle and pedestrian-safe corridor with a 14-foot-wide multi-use trail surrounded by mature trees and grasses thanks to Trees Atlanta’s Arboretum. With 16 points of entry, 14 of which will be ADA-accessible with ramp and stair systems, the trail provides numerous access points for people of all abilities. More details at: https://beltline.org/explore-atlanta-beltline-trails/westside-trail/',1);
/*!40000 ALTER TABLE `event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `manager`
--

DROP TABLE IF EXISTS `manager`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `manager` (
  `Username` varchar(20) NOT NULL,
  PRIMARY KEY (`Username`),
  CONSTRAINT `manager_ibfk_1` FOREIGN KEY (`Username`) REFERENCES `employee` (`username`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `manager`
--

LOCK TABLES `manager` WRITE;
/*!40000 ALTER TABLE `manager` DISABLE KEYS */;
INSERT INTO `manager` VALUES ('david.smith'),('manager1'),('manager2'),('manager3'),('manager4'),('manager5'),('maria.garcia');
/*!40000 ALTER TABLE `manager` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `myview`
--

DROP TABLE IF EXISTS `myview`;
/*!50001 DROP VIEW IF EXISTS `myview`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8mb4;
/*!50001 CREATE VIEW `myview` AS SELECT 
 1 AS `Username`,
 1 AS `EmailCount`,
 1 AS `Status`,
 1 AS `UserType`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `site`
--

DROP TABLE IF EXISTS `site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `site` (
  `Name` varchar(50) NOT NULL,
  `Address` varchar(50) DEFAULT NULL,
  `Zipcode` char(5) NOT NULL,
  `OpenEveryDay` enum('Yes','No') NOT NULL,
  `Manager` varchar(20) NOT NULL,
  PRIMARY KEY (`Name`),
  UNIQUE KEY `Manager` (`Manager`),
  CONSTRAINT `site_ibfk_1` FOREIGN KEY (`Manager`) REFERENCES `manager` (`username`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `site`
--

LOCK TABLES `site` WRITE;
/*!40000 ALTER TABLE `site` DISABLE KEYS */;
INSERT INTO `site` VALUES ('Atlanta Beltline Center','112 Krog Street Northeast','30307','No','manager3'),('Historic Fourth Ward Park','680 Dallas Street Northeast','30308','Yes','manager4'),('Inman Park','','30307','Yes','david.smith'),('Piedmont Park','400 Park Drive Northeast','30306','Yes','manager2'),('Westview Cemetery','1680 Westview Drive Southwest','30310','No','manager5');
/*!40000 ALTER TABLE `site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `staff`
--

DROP TABLE IF EXISTS `staff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `staff` (
  `Username` varchar(20) NOT NULL,
  PRIMARY KEY (`Username`),
  CONSTRAINT `staff_ibfk_1` FOREIGN KEY (`Username`) REFERENCES `employee` (`username`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staff`
--

LOCK TABLES `staff` WRITE;
/*!40000 ALTER TABLE `staff` DISABLE KEYS */;
INSERT INTO `staff` VALUES ('michael.smith'),('robert.smith'),('staff1'),('staff2'),('staff3');
/*!40000 ALTER TABLE `staff` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `staff_busy`
--

DROP TABLE IF EXISTS `staff_busy`;
/*!50001 DROP VIEW IF EXISTS `staff_busy`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8mb4;
/*!50001 CREATE VIEW `staff_busy` AS SELECT 
 1 AS `Username`,
 1 AS `Name`,
 1 AS `StartDate`,
 1 AS `SiteName`,
 1 AS `EndDate`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `take`
--

DROP TABLE IF EXISTS `take`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `take` (
  `Username` varchar(20) NOT NULL,
  `TransitType` varchar(10) NOT NULL,
  `TransitRoute` varchar(18) NOT NULL,
  `TransitDate` date NOT NULL,
  PRIMARY KEY (`Username`,`TransitDate`,`TransitType`,`TransitRoute`),
  KEY `TransitType` (`TransitType`,`TransitRoute`),
  CONSTRAINT `take_ibfk_1` FOREIGN KEY (`Username`) REFERENCES `user` (`username`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `take_ibfk_2` FOREIGN KEY (`TransitType`, `TransitRoute`) REFERENCES `transit` (`transittype`, `transitroute`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `take`
--

LOCK TABLES `take` WRITE;
/*!40000 ALTER TABLE `take` DISABLE KEYS */;
INSERT INTO `take` VALUES ('manager3','Bike','Relay','2019-03-20'),('maria.hernandez','Bike','Relay','2019-03-20'),('mary.smith','Bike','Relay','2019-03-23'),('manager2','Bus','152','2019-03-20'),('maria.hernandez','Bus','152','2019-03-20'),('maria.hernandez','Bus','152','2019-03-22'),('manager2','MARTA','Blue','2019-03-20'),('manager2','MARTA','Blue','2019-03-21'),('manager2','MARTA','Blue','2019-03-22'),('visitor1','MARTA','Blue','2019-03-21');
/*!40000 ALTER TABLE `take` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `test1`
--

DROP TABLE IF EXISTS `test1`;
/*!50001 DROP VIEW IF EXISTS `test1`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8mb4;
/*!50001 CREATE VIEW `test1` AS SELECT 
 1 AS `Name`,
 1 AS `SiteName`,
 1 AS `StartDate`,
 1 AS `Price`,
 1 AS `TotalVisits`,
 1 AS `description`,
 1 AS `EndDate`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `test2`
--

DROP TABLE IF EXISTS `test2`;
/*!50001 DROP VIEW IF EXISTS `test2`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8mb4;
/*!50001 CREATE VIEW `test2` AS SELECT 
 1 AS `Name`,
 1 AS `SiteName`,
 1 AS `Price`,
 1 AS `username`,
 1 AS `capacity`,
 1 AS `startdate`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `transit`
--

DROP TABLE IF EXISTS `transit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `transit` (
  `TransitType` varchar(10) NOT NULL,
  `TransitRoute` varchar(18) NOT NULL,
  `Price` decimal(6,2) unsigned NOT NULL,
  PRIMARY KEY (`TransitType`,`TransitRoute`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transit`
--

LOCK TABLES `transit` WRITE;
/*!40000 ALTER TABLE `transit` DISABLE KEYS */;
INSERT INTO `transit` VALUES ('Bike','Relay',1.00),('Bus','152',2.00),('MARTA','Blue',2.00);
/*!40000 ALTER TABLE `transit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `user` (
  `Username` varchar(20) NOT NULL,
  `Password` varchar(200) NOT NULL,
  `User_Status` enum('Pending','Approved','Declined') NOT NULL,
  `FirstName` varchar(20) NOT NULL,
  `LastName` varchar(20) NOT NULL,
  PRIMARY KEY (`Username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES ('david.smith','dsmith456','Approved','David','Smith'),('james.smith','jsmith123','Approved','James','Smith'),('manager1','manager1','Pending','Manager','One'),('manager2','manager2','Approved','Manager','Two'),('manager3','manager3','Approved','Manager','Three'),('manager4','manager4','Approved','Manager','Four'),('manager5','manager5','Approved','Manager','Five'),('maria.garcia','mgarcia123','Approved','Maria','Garcia'),('maria.hernandez','mhernandez','Approved','Maria','Hernandez'),('maria.rodriguez','mrodriguez','Declined','Maria','Rodriguez'),('mary.smith','msmith789','Approved','Mary','Smith'),('michael.smith','msmith456','Approved','Michael','Smith'),('robert.smith','rsmith789','Approved','Robert ','Smith'),('staff1','staff1234','Approved','Staff','One'),('staff2','staff4567','Approved','Staff','Two'),('staff3','staff7890','Approved','Staff','Three'),('user1','user123456','Pending','User','One'),('visitor1','visitor123','Approved','Visitor','One');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `visit_event`
--

DROP TABLE IF EXISTS `visit_event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `visit_event` (
  `Username` varchar(20) NOT NULL,
  `VisitEventName` varchar(50) NOT NULL,
  `StartDate` date NOT NULL,
  `SiteName` varchar(50) NOT NULL,
  `VisitEventDate` date NOT NULL,
  PRIMARY KEY (`Username`,`VisitEventName`,`StartDate`,`SiteName`,`VisitEventDate`),
  KEY `VisitEventName` (`VisitEventName`,`StartDate`,`SiteName`),
  CONSTRAINT `visit_event_ibfk_1` FOREIGN KEY (`VisitEventName`, `StartDate`, `SiteName`) REFERENCES `event` (`name`, `startdate`, `sitename`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `visit_event_ibfk_2` FOREIGN KEY (`Username`) REFERENCES `visitor` (`username`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `visit_event`
--

LOCK TABLES `visit_event` WRITE;
/*!40000 ALTER TABLE `visit_event` DISABLE KEYS */;
INSERT INTO `visit_event` VALUES ('mary.smith','Arboretum Walking Tour','2019-02-08','Inman Park','2019-02-10'),('manager2','Bus Tour','2019-02-01','Inman Park','2019-02-02'),('manager4','Bus Tour','2019-02-01','Inman Park','2019-02-01'),('manager5','Bus Tour','2019-02-01','Inman Park','2019-02-02'),('maria.garcia','Bus Tour','2019-02-01','Inman Park','2019-02-02'),('mary.smith','Bus Tour','2019-02-01','Inman Park','2019-02-01'),('staff2','Bus Tour','2019-02-01','Inman Park','2019-02-02'),('mary.smith','Eastside Trail','2019-02-04','Piedmont Park','2019-02-04'),('mary.smith','Eastside Trail','2019-02-13','Historic Fourth Ward Park','2019-02-13'),('mary.smith','Eastside Trail','2019-02-13','Historic Fourth Ward Park','2019-02-14'),('visitor1','Eastside Trail','2019-02-13','Historic Fourth Ward Park','2019-02-14'),('mary.smith','Official Atlanta BeltLine Bike Tour','2019-02-09','Atlanta BeltLine Center','2019-02-10'),('visitor1','Official Atlanta BeltLine Bike Tour','2019-02-09','Atlanta BeltLine Center','2019-02-10'),('mary.smith','Private Bus Tour','2019-02-01','Inman Park','2019-02-01'),('mary.smith','Private Bus Tour','2019-02-01','Inman Park','2019-02-02'),('mary.smith','Westside Trail','2019-02-18','Westview Cemetery','2019-02-19'),('visitor1','Westside Trail','2019-02-18','Westview Cemetery','2019-02-19');
/*!40000 ALTER TABLE `visit_event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `visit_site`
--

DROP TABLE IF EXISTS `visit_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `visit_site` (
  `Username` varchar(20) NOT NULL,
  `SiteName` varchar(50) NOT NULL,
  `Date` date NOT NULL,
  PRIMARY KEY (`Username`,`SiteName`,`Date`),
  KEY `SiteName` (`SiteName`),
  CONSTRAINT `visit_site_ibfk_1` FOREIGN KEY (`SiteName`) REFERENCES `site` (`name`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `visit_site_ibfk_2` FOREIGN KEY (`Username`) REFERENCES `visitor` (`username`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `visit_site`
--

LOCK TABLES `visit_site` WRITE;
/*!40000 ALTER TABLE `visit_site` DISABLE KEYS */;
INSERT INTO `visit_site` VALUES ('mary.smith','Atlanta Beltline Center','2019-02-01'),('mary.smith','Atlanta Beltline Center','2019-02-10'),('visitor1','Atlanta Beltline Center','2019-02-09'),('visitor1','Atlanta Beltline Center','2019-02-13'),('mary.smith','Historic Fourth Ward Park','2019-02-02'),('visitor1','Historic Fourth Ward Park','2019-02-11'),('mary.smith','Inman Park','2019-02-01'),('mary.smith','Inman Park','2019-02-02'),('mary.smith','Inman Park','2019-02-03'),('visitor1','Inman Park','2019-02-01'),('mary.smith','Piedmont Park','2019-02-02'),('visitor1','Piedmont Park','2019-02-01'),('visitor1','Piedmont Park','2019-02-11'),('visitor1','Westview Cemetery','2019-02-06');
/*!40000 ALTER TABLE `visit_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `visitor`
--

DROP TABLE IF EXISTS `visitor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `visitor` (
  `Username` varchar(20) NOT NULL,
  PRIMARY KEY (`Username`),
  CONSTRAINT `visitor_ibfk_1` FOREIGN KEY (`Username`) REFERENCES `user` (`username`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `visitor`
--

LOCK TABLES `visitor` WRITE;
/*!40000 ALTER TABLE `visitor` DISABLE KEYS */;
INSERT INTO `visitor` VALUES ('manager2'),('manager4'),('manager5'),('maria.garcia'),('maria.rodriguez'),('mary.smith'),('michael.smith'),('staff2'),('staff3'),('visitor1');
/*!40000 ALTER TABLE `visitor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'beltline'
--

--
-- Dumping routines for database 'beltline'
--

--
-- Final view structure for view `myview`
--

/*!50001 DROP VIEW IF EXISTS `myview`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `myview` AS select `user`.`Username` AS `Username`,count(`user`.`Username`) AS `EmailCount`,`user`.`User_Status` AS `Status`,(case when `user`.`Username` in (select `visitor`.`Username` from `visitor`) then 'visitor' when `user`.`Username` in (select `manager`.`Username` from `manager`) then 'manager' when `user`.`Username` in (select `staff`.`Username` from `staff`) then 'staff' when `user`.`Username` in (select `administrator`.`Username` from `administrator`) then 'administrator' else 'user' end) AS `UserType` from (`user` join `email` on((`user`.`Username` = `email`.`Username`))) group by `user`.`Username` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `staff_busy`
--

/*!50001 DROP VIEW IF EXISTS `staff_busy`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `staff_busy` AS select `assign_to`.`Username` AS `Username`,`assign_to`.`Name` AS `Name`,`assign_to`.`StartDate` AS `StartDate`,`assign_to`.`SiteName` AS `SiteName`,`event`.`EndDate` AS `EndDate` from (`assign_to` join `event` on(((`assign_to`.`Name` = `event`.`Name`) and (`assign_to`.`StartDate` = `event`.`StartDate`) and (`assign_to`.`SiteName` = `event`.`SiteName`)))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `test1`
--

/*!50001 DROP VIEW IF EXISTS `test1`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `test1` AS select `event`.`Name` AS `Name`,`event`.`SiteName` AS `SiteName`,`event`.`StartDate` AS `StartDate`,`event`.`Price` AS `Price`,count(`visit_event`.`Username`) AS `TotalVisits`,`event`.`Description` AS `description`,`event`.`EndDate` AS `EndDate` from (`event` join `visit_event` on(((`visit_event`.`SiteName` = `event`.`SiteName`) and (`visit_event`.`StartDate` = `event`.`StartDate`) and (`visit_event`.`VisitEventName` = `event`.`Name`)))) group by `event`.`Name`,`event`.`StartDate`,`event`.`SiteName` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `test2`
--

/*!50001 DROP VIEW IF EXISTS `test2`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `test2` AS select `event`.`Name` AS `Name`,`event`.`SiteName` AS `SiteName`,`event`.`Price` AS `Price`,`visit_event`.`Username` AS `username`,`event`.`Capacity` AS `capacity`,`event`.`StartDate` AS `startdate` from (`event` join `visit_event` on(((`visit_event`.`SiteName` = `event`.`SiteName`) and (`visit_event`.`StartDate` = `event`.`StartDate`) and (`visit_event`.`VisitEventName` = `event`.`Name`)))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-04-21 23:59:50
