-- MySQL dump 10.13  Distrib 5.7.17, for macos10.12 (x86_64)
--
-- Host: localhost    Database: ncaa_bb
-- ------------------------------------------------------
-- Server version	5.7.20

use ncaa_bb;
/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `baseratings`
--

DROP TABLE IF EXISTS `baseratings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `baseratings` (
  `teamname` varchar(50) NOT NULL,
  `basedate` date NOT NULL,
  `predictive-by-other` float(7,4) DEFAULT NULL,
  `home-by-other` float(7,4) DEFAULT NULL,
  `away-by-other` float(7,4) DEFAULT NULL,
  `neutral-by-other` float(7,4) DEFAULT NULL,
  `home-adv-by-other` float(7,4) DEFAULT NULL,
  `schedule-strength-by-other` float(7,4) DEFAULT NULL,
  `future-sos-by-other` float(7,4) DEFAULT NULL,
  `season-sos-by-other` float(7,4) DEFAULT NULL,
  `sos-basic-by-other` float(7,4) DEFAULT NULL,
  `in-conference-sos-by-other` float(7,4) DEFAULT NULL,
  `non-conference-sos-by-other` float(7,4) DEFAULT NULL,
  `last-5-games-by-other` float(7,4) DEFAULT NULL,
  `last-10-games-by-other` float(7,4) DEFAULT NULL,
  `in-conference-by-other` float(7,4) DEFAULT NULL,
  `non-conference-by-other` float(7,4) DEFAULT NULL,
  `luck-by-other` float(7,4) DEFAULT NULL,
  `consistency-by-other` float(7,4) DEFAULT NULL,
  `vs-1-10-by-other` float(7,4) DEFAULT NULL,
  `vs-11-25-by-other` float(7,4) DEFAULT NULL,
  `vs-26-40-by-other` float(7,4) DEFAULT NULL,
  `vs-41-75-by-other` float(7,4) DEFAULT NULL,
  `vs-76-120-by-other` float(7,4) DEFAULT NULL,
  `first-half-by-other` float(7,4) DEFAULT NULL,
  `second-half-by-other` float(7,4) DEFAULT NULL,
  PRIMARY KEY (`teamname`,`basedate`),
  CONSTRAINT `fk_base_teamname` FOREIGN KEY (`teamname`) REFERENCES `teamnames` (`teamname`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `masseyratings`
--

DROP TABLE IF EXISTS `masseyratings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `masseyratings` (
  `teamname` varchar(50) NOT NULL,
  `masseydate` date NOT NULL,
  `PIR` int(11) DEFAULT NULL,
  `OSC` int(11) DEFAULT NULL,
  `UCC` int(11) DEFAULT NULL,
  `KPK` int(11) DEFAULT NULL,
  `COF` int(11) DEFAULT NULL,
  `LAZ` int(11) DEFAULT NULL,
  `RWP` int(11) DEFAULT NULL,
  `ACU` int(11) DEFAULT NULL,
  `PAY` int(11) DEFAULT NULL,
  `JTR` int(11) DEFAULT NULL,
  `MTN` int(11) DEFAULT NULL,
  `RT` int(11) DEFAULT NULL,
  `DII` int(11) DEFAULT NULL,
  `ASH` int(11) DEFAULT NULL,
  `FMG` int(11) DEFAULT NULL,
  `RUD` int(11) DEFAULT NULL,
  `MGS` int(11) DEFAULT NULL,
  `ARG` int(11) DEFAULT NULL,
  `SOR` int(11) DEFAULT NULL,
  `WLK` int(11) DEFAULT NULL,
  `SEL` int(11) DEFAULT NULL,
  `HEN` int(11) DEFAULT NULL,
  `HAT` int(11) DEFAULT NULL,
  `MAS` int(11) DEFAULT NULL,
  `HKB` int(11) DEFAULT NULL,
  `DOL` int(11) DEFAULT NULL,
  `MvG` int(11) DEFAULT NULL,
  `KEE` int(11) DEFAULT NULL,
  `FAS` int(11) DEFAULT NULL,
  `SAG` int(11) DEFAULT NULL,
  `BIH` int(11) DEFAULT NULL,
  `HOW` int(11) DEFAULT NULL,
  `GRS` int(11) DEFAULT NULL,
  `ENG` int(11) DEFAULT NULL,
  `JRT` int(11) DEFAULT NULL,
  `STH` int(11) DEFAULT NULL,
  `PGH` int(11) DEFAULT NULL,
  `RTH` int(11) DEFAULT NULL,
  `HNL` int(11) DEFAULT NULL,
  `KH` int(11) DEFAULT NULL,
  `EZ` int(11) DEFAULT NULL,
  `WOB` int(11) DEFAULT NULL,
  `ABC` int(11) DEFAULT NULL,
  `ISR` int(11) DEFAULT NULL,
  `JNK` int(11) DEFAULT NULL,
  `AND` int(11) DEFAULT NULL,
  `COL` int(11) DEFAULT NULL,
  `BOW` int(11) DEFAULT NULL,
  `YCM` int(11) DEFAULT NULL,
  `PCP` int(11) DEFAULT NULL,
  `SOL` int(11) DEFAULT NULL,
  `WOL` int(11) DEFAULT NULL,
  `EFI` int(11) DEFAULT NULL,
  `BSS` int(11) DEFAULT NULL,
  `KRA` int(11) DEFAULT NULL,
  `WIL` int(11) DEFAULT NULL,
  `LOG` int(11) DEFAULT NULL,
  `BWE` int(11) DEFAULT NULL,
  `BBT` int(11) DEFAULT NULL,
  `RTP` int(11) DEFAULT NULL,
  `RFL` int(11) DEFAULT NULL,
  `WWP` int(11) DEFAULT NULL,
  `KLK` int(11) DEFAULT NULL,
  `REW` int(11) DEFAULT NULL,
  `DUN` int(11) DEFAULT NULL,
  `KEL` int(11) DEFAULT NULL,
  `DP` int(11) DEFAULT NULL,
  `BIL` int(11) DEFAULT NULL,
  `ONV` int(11) DEFAULT NULL,
  `KNT` int(11) DEFAULT NULL,
  `MCK` int(11) DEFAULT NULL,
  `BMC` int(11) DEFAULT NULL,
  `SP` int(11) DEFAULT NULL,
  `LSW` int(11) DEFAULT NULL,
  `GLD` int(11) DEFAULT NULL,
  `WEL` int(11) DEFAULT NULL,
  `BCM` int(11) DEFAULT NULL,
  `MCL` int(11) DEFAULT NULL,
  `LSD` int(11) DEFAULT NULL,
  `MAR` int(11) DEFAULT NULL,
  `DOI` int(11) DEFAULT NULL,
  `DOK` int(11) DEFAULT NULL,
  `TRP` int(11) DEFAULT NULL,
  `VRN` int(11) DEFAULT NULL,
  `INP` int(11) DEFAULT NULL,
  `MJS` int(11) DEFAULT NULL,
  `CSL` int(11) DEFAULT NULL,
  `DEZ` int(11) DEFAULT NULL,
  `RME` int(11) DEFAULT NULL,
  `DWI` int(11) DEFAULT NULL,
  `DES` int(11) DEFAULT NULL,
  `KEN` int(11) DEFAULT NULL,
  `MOR` int(11) DEFAULT NULL,
  `DCI` int(11) DEFAULT NULL,
  `CTW` int(11) DEFAULT NULL,
  `FPI` int(11) DEFAULT NULL,
  `PPP` int(11) DEFAULT NULL,
  `MRK` int(11) DEFAULT NULL,
  `TFG` int(11) DEFAULT NULL,
  `MDS` int(11) DEFAULT NULL,
  `BAS` int(11) DEFAULT NULL,
  `GRR` int(11) DEFAULT NULL,
  `BRN` int(11) DEFAULT NULL,
  `GBE` int(11) DEFAULT NULL,
  `RSL` int(11) DEFAULT NULL,
  `PIG` int(11) DEFAULT NULL,
  `SFX` int(11) DEFAULT NULL,
  `FEI` int(11) DEFAULT NULL,
  `CGV` int(11) DEFAULT NULL,
  `KAM` int(11) DEFAULT NULL,
  `CFP` int(11) DEFAULT NULL,
  `S&P` int(11) DEFAULT NULL,
  `RBA` int(11) DEFAULT NULL,
  `NOL` int(11) DEFAULT NULL,
  `PFZ` int(11) DEFAULT NULL,
  `MGN` int(11) DEFAULT NULL,
  `TPR` int(11) DEFAULT NULL,
  `BDF` int(11) DEFAULT NULL,
  `D1A` int(11) DEFAULT NULL,
  `ATC` int(11) DEFAULT NULL,
  `CMV` int(11) DEFAULT NULL,
  `MVP` int(11) DEFAULT NULL,
  `NUT` int(11) DEFAULT NULL,
  `RTB` int(11) DEFAULT NULL,
  PRIMARY KEY (`teamname`,`masseydate`),
  CONSTRAINT `fk_massey_teamname` FOREIGN KEY (`teamname`) REFERENCES `teamnames` (`teamname`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `oddsdata`
--

DROP TABLE IF EXISTS `oddsdata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `oddsdata` (
  `oddsdate` date NOT NULL,
  `favorite` varchar(50) NOT NULL,
  `underdog` varchar(50) NOT NULL,
  `line` float(7,4) DEFAULT NULL,
  `juice` float(7,4) DEFAULT NULL,
  `overunder` float(7,4) DEFAULT NULL,
  `oujuice` float(7,4) DEFAULT NULL,
  `favmoneyline` float(7,2) DEFAULT NULL,
  `dogmoneyline` float(7,2) DEFAULT NULL,
  `favscore` int(11) DEFAULT NULL,
  `dogscore` int(11) DEFAULT NULL,
  `homeaway` int(11) DEFAULT NULL,
  PRIMARY KEY (`oddsdate`,`favorite`,`underdog`),
  KEY `fk_odds_favorite` (`favorite`),
  KEY `fk_odds_underdog` (`underdog`),
  CONSTRAINT `fk_odds_favorite` FOREIGN KEY (`favorite`) REFERENCES `teamnames` (`teamname`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_odds_underdog` FOREIGN KEY (`underdog`) REFERENCES `teamnames` (`teamname`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `teamnames`
--

DROP TABLE IF EXISTS `teamnames`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `teamnames` (
  `teamname` varchar(50) NOT NULL,
  PRIMARY KEY (`teamname`),
  UNIQUE KEY `teamname_UNIQUE` (`teamname`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;


/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-11-25 22:13:36
