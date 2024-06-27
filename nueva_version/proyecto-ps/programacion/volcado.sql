-- MySQL dump 10.13  Distrib 8.0.37, for Linux (x86_64)
--
-- Host: localhost    Database: ps
-- ------------------------------------------------------
-- Server version	8.0.37

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (1,'Maestro');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add usuario',7,'add_usuario'),(26,'Can change usuario',7,'change_usuario'),(27,'Can delete usuario',7,'delete_usuario'),(28,'Can view usuario',7,'view_usuario'),(29,'Can add ejercicio',8,'add_ejercicio'),(30,'Can change ejercicio',8,'change_ejercicio'),(31,'Can delete ejercicio',8,'delete_ejercicio'),(32,'Can view ejercicio',8,'view_ejercicio'),(33,'Can add failed login attempt',9,'add_failedloginattempt'),(34,'Can change failed login attempt',9,'change_failedloginattempt'),(35,'Can delete failed login attempt',9,'delete_failedloginattempt'),(36,'Can view failed login attempt',9,'view_failedloginattempt'),(37,'Can add respuesta ejercicio',10,'add_respuestaejercicio'),(38,'Can change respuesta ejercicio',10,'change_respuestaejercicio'),(39,'Can delete respuesta ejercicio',10,'delete_respuestaejercicio'),(40,'Can view respuesta ejercicio',10,'view_respuestaejercicio');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$150000$Uex4jptUPUPC$dP5cLkVPqSfNF4AD6IKv53JJmsAue11y1PEcZSKWdGU=','2024-06-01 07:34:00.524038',1,'ps','','','ps@gmail.com',1,1,'2024-06-01 07:33:37.066266');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2024-06-01 07:34:38.369122','1','Usuario object (1)',1,'[{\"added\": {}}]',7,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(8,'programacion','ejercicio'),(9,'programacion','failedloginattempt'),(10,'programacion','respuestaejercicio'),(7,'programacion','usuario'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2024-06-01 07:31:59.837542'),(2,'auth','0001_initial','2024-06-01 07:32:00.043629'),(3,'admin','0001_initial','2024-06-01 07:32:00.331465'),(4,'admin','0002_logentry_remove_auto_add','2024-06-01 07:32:00.450894'),(5,'admin','0003_logentry_add_action_flag_choices','2024-06-01 07:32:00.464449'),(6,'contenttypes','0002_remove_content_type_name','2024-06-01 07:32:00.562570'),(7,'auth','0002_alter_permission_name_max_length','2024-06-01 07:32:00.706779'),(8,'auth','0003_alter_user_email_max_length','2024-06-01 07:32:00.761917'),(9,'auth','0004_alter_user_username_opts','2024-06-01 07:32:00.791099'),(10,'auth','0005_alter_user_last_login_null','2024-06-01 07:32:00.850725'),(11,'auth','0006_require_contenttypes_0002','2024-06-01 07:32:00.855798'),(12,'auth','0007_alter_validators_add_error_messages','2024-06-01 07:32:00.871849'),(13,'auth','0008_alter_user_username_max_length','2024-06-01 07:32:00.964255'),(14,'auth','0009_alter_user_last_name_max_length','2024-06-01 07:32:01.045511'),(15,'auth','0010_alter_group_name_max_length','2024-06-01 07:32:01.070139'),(16,'auth','0011_update_proxy_permissions','2024-06-01 07:32:01.085612'),(17,'programacion','0001_initial','2024-06-01 07:32:01.125497'),(18,'programacion','0002_auto_20240529_2343','2024-06-01 07:32:01.187980'),(19,'sessions','0001_initial','2024-06-01 07:32:01.251646'),(20,'programacion','0003_failedloginattempt','2024-06-01 08:33:10.637414'),(21,'programacion','0004_auto_20240601_1848','2024-06-01 18:50:02.014429'),(22,'programacion','0005_ejercicio_descripcion_ejercicio','2024-06-01 18:57:28.363142'),(23,'programacion','0006_auto_20240601_2102','2024-06-01 21:02:49.827032'),(24,'auth','0012_alter_user_first_name_max_length','2024-06-02 03:42:43.947699'),(25,'programacion','0007_usuario_is_maestro_alter_ejercicio_id_and_more','2024-06-02 04:52:41.627079'),(26,'programacion','0008_usuario_last_login','2024-06-02 19:06:32.966253'),(27,'programacion','0009_usuario_groups_usuario_is_staff_usuario_is_superuser_and_more','2024-06-02 19:29:49.568217'),(28,'programacion','0010_usuario_is_active_alter_usuario_groups_and_more','2024-06-02 19:50:43.125141');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('01hovjlzes0fxqs9o80acq2d7qlx923k','.eJxVjM0KwjAQhF9FcrYlu7HV9OjFkwefoGx2tz8qDaQVEfHdbUFQb8N8M9_T1HSbuvo2aqp7MZVBs_7tAvFFhwXImYY25hyHKfUhXyb5h475MYpe95_tn6CjsZvfG_TqAQJZALsjK64Ijtkq4NahI5oTeyyhYRJuGDQEIArSiOy8g1nKUfo21hxTUp7iLD30tjndH-UXtjpoIlkgWtxktszArRCrwlaFN683O-5NVA:1sHtHx:p8PXZJObooFh550EQPK9zB6RTU_oUF672AB9LQ736Bc','2024-06-13 23:06:25.447143'),('42i6c75ep2u5kyqo3cj89mt1nq0snx6n','.eJxVj8tOxDAMRX8FsoWp4qTzaJfs2YCE2FWO7T5mpglKWs1IiH8nQSMBO-ue6yP7U3W4LmO3JondxKpVRj3-zRzSSXwBfEQ_hIqCX-LkqlKpbjRVz4Hl_HTr_hOMmMa8XZtGGgCHGkAfULPdOkukBczeGouYJ2rMDnpCpp5AnANExz3zobGQpUXncZZsW9ZrDj4wpUuI5bg3oAcd59rf55wCT0PoKMQotITy1OuL9-9z_QsH8RKRf6A29UbvNtreadPafbsF9fUN4l1aNA:1sDxaL:YLLI6RDQYsKboodCK-V41VJNp6ZYgSb-VIu5Ha5AyqQ','2024-06-03 03:38:09.351760'),('54s13vewun7mouya2n9kpwag8d71xsj9','.eJyrViotTi3KS8xNVbJSKsmPKTUwSDPMV9JRKkgsLi7PL0oBCocZJmsbFOWa5CkCxZPzUzLT8-OT84uKUpNL8oHSuaFlznmpyZ4IyfTUvNSixBSQpJGBkYmugZmugZGCobmVqZmVkZFSLQDXtyRW:1sDpRO:mmz5-TOCfozmnsSyDSpUhK6TfE5zo-1L8Eg8TjZNkQM','2024-06-02 18:56:22.319314'),('84wboazaw30e82y9tp7hyyis849r30b2','.eJxVjDkOwjAURO_iGln-NktMSZ8zWH8zDiBHipMKcXcSKQV0o3lv5m0SLnNJS9MpDWKuxpvDb0fIT60bkAfW-2h5rPM0kN0Uu9Nm-1H0ddvdv4OCrazro48aAQgdgOvQSThRYHYK_hJ8QFwTR3-GzCicGZQIEEmySBcDmM8X30Q4tg:1sHTZ3:0hSgFfPuf7DN9bYufKX-KRK6taENAXtYDNhHViMC55E','2024-06-12 19:38:21.367274'),('atsjiqh8bcd8toqye8nuwwihn80gpvms','.eJxVjDkOwjAURO_iGln-NktMSZ8zWH8zDiBHipMKcXcSKQV0o3lv5m0SLnNJS9MpDWKuxpvDb0fIT60bkAfW-2h5rPM0kN0Uu9Nm-1H0ddvdv4OCrazro48aAQgdgOvQSThRYHYK_hJ8QFwTR3-GzCicGZQIEEmySBcDmM8X30Q4tg:1sDxjv:vaS5pL27PGwN6R2I7ymV8jIT3z5x7t6NUtGvqFE80Nk','2024-06-03 03:48:03.859364'),('b1egey8luqh3kra9g5p76pgmrlmz7gvy','e30:1sDcCT:uK0RzmgSffaYsETDPgXaif9cbIEG2DHT7DS53P7Txdg','2024-06-02 04:48:05.728020'),('cazqh2nfvdgy9akn5jw78tlr5zigd6un','.eJxVjD0PgkAQRP-KuVrI7R6iUGplYWJhT_Z2lw81XHJAo_G_C4mJ2k3mzbynqWga22oaNFadmNKgWf92nvim_QLkSn0TUg79GDufLpP0Q4f0FETv-8_2T9DS0M7vDAstADxZALsjK27jHbNVwK1DRzQnLjCHmkm4ZlDvgchLLbIrHMxSDtI1oeIQo_IYZqk7Hh7nDi9f2GivkWSBaDFLbJ6AWyGWAOUmN683LzVNCQ:1sHshj:0SnJL_GdR4JadWu041MLmPCchwmHItShRFJ6byM0O8M','2024-06-13 22:28:59.256541'),('cybnsoxstt9u7welngc3p15lklvv38j1','.eJxVjctOAzEMRX8Fsi0dxUlaOrPshhVbJFYjx_Y8Ck1QMkMrIf6dRKqEurPuOdf3R61ZUsCzqE4t61U9qS_M-RITl-ANaKPT2YXHklPkeYw9xZSElljwRa7vL_ob_-EoQRJyhUYbt9X7LcCDtp3bddYVr8d1mfq62c91wdxnHulDQgV8wjDGhmJY0uybqjQ3mpvXyPJ5vLl3DybMU2k700oL4FED6ANqtjtvibSAebbGIpaLWrOHgZBpIBDvAdHzwHxoLajfP12OWoM:1sGsSF:jOtq_JbBgRU4hxQJ59JGduokVyr76SPpWMZZIym7jcE','2024-06-11 04:45:51.773240'),('ic3f4dqvzbyr2437i3uwt6tb88kevqmj','.eJyrViotTi3KS8xNVbJSKimtUNJRKkgsLi7PL0oBCoQZJmsbFOWa5CkCxZPzUzLT8-OT84uKUpNL8oHSzrnOgTnegREIyfTUvNSixBSQpJGBkYmugZmugZGCoaWVgaGVqalSLQD7ISJF:1sDqTb:80YcR-EBjGLxNRPFEJkF7cLrJ5BlhfOVeFkuzGu1iss','2024-06-02 20:02:43.675933'),('kyz83vj8bhl4cnyu66pw2tpwym78c9kq','N2EwYWJiZjY2YjhlZGJiNmVlN2IzY2M0MWMzZGI5ZDZiMzFhNDRmYTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI2ZTJiNTRmM2VhYjUzYTAyNGFmYzVkMjViOGE4NTI4MmVjNjg0YTZmIiwiY29kaWdvX2NvcnJlY3RvIjoiZmFQOVhtejciLCJjb2RpZ29fZ2VuZXJhZG8iOiIyMDI0LTA2LTAxIDA4OjQ1OjM0In0=','2024-06-01 09:45:34.380064'),('mm6xu323gtiqyxgddmepvr58ae4b0ijc','.eJxVjstqwzAQRX-l0TaJGY9kyfayi0Ah2ZbujB7jR9tIRnLoIvTfK0Gg7faeM4e5s0Hftnm4JYrD4ljPBDv83Yy2H-QLcO_aT6GywW9xMVVRqgdN1SU4-nx-uP8Cs05zvkZUo5RWmLHj1HCpFXSdbLgRgiTWjcMOaFSOK4muBTCtlS0qAqihdUbnaMl5faVcW2ldtpC3Vaf0FWL577W2e4hX4Xd5t8EtUxhsiJFsNnv2Bi_n01ltv3AiT1G7AhFQHEEeAZ-w7hF63rDvHxWyWUI:1sDsdg:1hNE16uRDo1M6kz2QYIZ6atjIn83X_e0J8dFcEpfDqY','2024-06-02 22:21:16.008548'),('po3b1xfgrc097solzsqi2z51o3n8r1dj','.eJyrViotTi3KS8xNVbJSKimtUNJRKkgsLi7PL0oBCoQZJmsbFOWa5CkCxZPzUzLT8-OT84uKUpNL8oHSZj6BTqmp6SYIyfTUvNSixBSQpJGBkYmugZmugZGCoYGVoYmVsZFSLQDy6CIR:1sDiES:jedw1r-3InmN0i7QSvlO5TYVWgkGvFW74LWQeFUkNx0','2024-06-02 11:14:32.386271'),('q7t0hh4o7r1sdyg4cx8m8217bnoz86bu','eyJ1c2VybmFtZSI6InR1eCIsInBhc3N3b3JkIjoiVjFjKzBybTRuISJ9:1sEC3W:e1xr2vjcWkr3McwB265CTaQ7IRRXzNK_rGf0YtN5C1I','2024-06-03 19:05:14.926658'),('r9qcwl2w1i5k1p24mg48nghu68nk8tao','.eJxVjctOwzAQRX8FvKWNPHYakiwRO9RNF0isovHM5AHURnaiIiH-HVuqhLob3XPu3B-1JYkez6J6tW7faqe-MKVLiJyDV6AHHc-1v885BV6mMFCIUWgNxT-BvKS35384iZeIXKDRpt7rZq_tHdj-0PbQZG_AbZ2HsjksZcHcZg7pQ3wB_I5-ChUFv8bFVUWprjRVx8Dy-XR1bx7MmObcrk0nHYBDDaBb1GwPzhJpAfNojUXMF3WmgZGQaSQQ5wDR8cjcdhbU7x8n3VpF:1sE8Ct:UMXf3evAVXIPwPBhjClF0tLdqUFdNk5ndS6IF_CevC8','2024-06-03 14:58:39.041717'),('uvcggsbgvjopq2r3wk5lubblbh21vsau','.eJxVjDkOwjAURO_iGln-NktMSZ8zWH8zDiBHipMKcXcSKQV0o3lv5m0SLnNJS9MpDWKuxpvDb0fIT60bkAfW-2h5rPM0kN0Uu9Nm-1H0ddvdv4OCrazro48aAQgdgOvQSThRYHYK_hJ8QFwTR3-GzCicGZQIEEmySBcDmM8X30Q4tg:1sIED7:NN1wroW2jlouuA1rWKgIr6aor8ki-kJV86af2GB_Va8','2024-06-14 21:26:49.514016');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `programacion_ejercicio`
--

DROP TABLE IF EXISTS `programacion_ejercicio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `programacion_ejercicio` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre_ejercicio` varchar(200) NOT NULL,
  `fecha_entrega` datetime(6) NOT NULL,
  `descripcion_ejercicio` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `programacion_ejercicio`
--

LOCK TABLES `programacion_ejercicio` WRITE;
/*!40000 ALTER TABLE `programacion_ejercicio` DISABLE KEYS */;
INSERT INTO `programacion_ejercicio` VALUES (1,'ejersicio 1','2024-06-01 18:50:48.224426','Descripción del ejercicio'),(2,'ejersicio 1','2024-06-01 18:51:23.135545','Descripción del ejercicio'),(3,'ejersicio 1','2024-06-01 18:57:52.909983','este es de prueba'),(4,'ejersicio 1','2024-06-01 19:09:54.747630','este es de tux'),(5,'ejercicio2','2024-06-01 19:43:05.196686','pruebas'),(6,'programa','2024-06-02 21:04:10.000000','este es el numero 1'),(7,'programa2','2024-06-02 04:00:18.000000','esta es otra prueba'),(8,'probando sesion','2024-06-02 20:37:16.000000','este es el primer ejercicio probando sesion'),(9,'otro de prueba','2024-06-02 20:39:04.000000','otro mas'),(10,'otro de prueba 2','2024-06-02 20:40:48.000000','otro mas 2'),(11,'ejercicio 4','2024-06-02 20:42:16.000000','el 4');
/*!40000 ALTER TABLE `programacion_ejercicio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `programacion_failedloginattempt`
--

DROP TABLE IF EXISTS `programacion_failedloginattempt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `programacion_failedloginattempt` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `ip_address` char(39) NOT NULL,
  `attempt_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=85 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `programacion_failedloginattempt`
--

LOCK TABLES `programacion_failedloginattempt` WRITE;
/*!40000 ALTER TABLE `programacion_failedloginattempt` DISABLE KEYS */;
/*!40000 ALTER TABLE `programacion_failedloginattempt` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `programacion_respuestaejercicio`
--

DROP TABLE IF EXISTS `programacion_respuestaejercicio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `programacion_respuestaejercicio` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre_alumno` varchar(100) NOT NULL,
  `respuesta` longtext NOT NULL,
  `puntaje` int DEFAULT NULL,
  `ejercicio_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `programacion_respuestaejercicio_ejercicio_id_f36efc08_fk` (`ejercicio_id`),
  CONSTRAINT `programacion_respuestaejercicio_ejercicio_id_f36efc08_fk` FOREIGN KEY (`ejercicio_id`) REFERENCES `programacion_ejercicio` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `programacion_respuestaejercicio`
--

LOCK TABLES `programacion_respuestaejercicio` WRITE;
/*!40000 ALTER TABLE `programacion_respuestaejercicio` DISABLE KEYS */;
INSERT INTO `programacion_respuestaejercicio` VALUES (1,'victor','esta es mi respuesta',8,6),(2,'vic','esta es mi respueesta',9,7),(3,'esoider','esta es mi respuesta',10,3),(4,'mario bross','mi respuesta',76,11);
/*!40000 ALTER TABLE `programacion_respuestaejercicio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `programacion_usuario`
--

DROP TABLE IF EXISTS `programacion_usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `programacion_usuario` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `password` varchar(128) NOT NULL,
  `is_maestro` tinyint(1) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `programacion_usuario`
--

LOCK TABLES `programacion_usuario` WRITE;
/*!40000 ALTER TABLE `programacion_usuario` DISABLE KEYS */;
INSERT INTO `programacion_usuario` VALUES (1,'juan','juan@gmail.com','123456789',0,NULL,0,0,1),(2,'tux','tux@gmial.com','$6$udyWlJsV0cjn4mj3$mh5o4JD3GuWLWkgiZ7OxukiMZe9iSV2HPCHJTmExYH7yzT9YGqtSGSjGuXTHAO2SG8cMY6DRtOkkOWFCwlmXf/',1,'2024-06-15 22:39:47.439219',0,0,1),(3,'memo','meo@gmail.com','$6$TnMO8zdXqqbgyt1W$Coalj1UPktRZT.nNK3/frTQFGyy9hNTAbCCzRkRGwZHLWZRsIU.mJBO2Vuh8LQBaUJG2bHZbQyZQrS77nnVoM/',0,NULL,0,0,1),(4,'pepito','pepi@gmail.com','$6$A7ScGqKslR6B81r3$gMi/MZl1n8Vy2U1gr1scKs1OR6VpDFEmUA18SyECsmUiZJ7xS9rnLOvUqELCxJInpQHHXL4dJQiBihVpB45FK.',0,'2024-06-03 16:14:11.381436',0,0,1),(5,'toño','j@gmail.com','$6$3aHDiU0soZ4m/CdH$sKCGHCKApM8obRgYLnQQZjvxM2e65JcUUbzQWAh3Dmg9wGOFl/bVLcg71DAX.ACvbNmhSzoqjyc63M7fBCd6D/',0,NULL,0,0,1),(6,'spirder','spider@gmail.com','$6$8wDn8HPWIRu4zT3f$CI0X6eMii6ck5Prhf4oxjmNVoVMKphwYKhtdIoN.Zzcm.qp3JZZMJb8eshLbVJ6jFPnlBtlY4gMFtf49A4OUl1',0,'2024-06-03 02:42:12.263836',0,0,1),(7,'dios','dios@gmail.com','$6$dXfoH+OPTkR0Ho5z$INIUCHHuq2puIOW5KJ4Ez23n82mcOLYV3MUZdXV4uhQzv39o.uNiuFEAaLcjoR8.3dF2c15FFd0scq9vp2w300',0,'2024-06-12 20:05:34.343290',0,0,1);
/*!40000 ALTER TABLE `programacion_usuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `programacion_usuario_groups`
--

DROP TABLE IF EXISTS `programacion_usuario_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `programacion_usuario_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `usuario_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `programacion_usuario_groups_usuario_id_group_id_2e82331b_uniq` (`usuario_id`,`group_id`),
  KEY `programacion_usuario_groups_group_id_9f9fea7b_fk_auth_group_id` (`group_id`),
  CONSTRAINT `programacion_usuario_groups_group_id_9f9fea7b_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `programacion_usuario_usuario_id_355b62f8_fk_programac` FOREIGN KEY (`usuario_id`) REFERENCES `programacion_usuario` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `programacion_usuario_groups`
--

LOCK TABLES `programacion_usuario_groups` WRITE;
/*!40000 ALTER TABLE `programacion_usuario_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `programacion_usuario_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `programacion_usuario_user_permissions`
--

DROP TABLE IF EXISTS `programacion_usuario_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `programacion_usuario_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `usuario_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `programacion_usuario_use_usuario_id_permission_id_17ab9c9a_uniq` (`usuario_id`,`permission_id`),
  KEY `programacion_usuario_permission_id_f4021e00_fk_auth_perm` (`permission_id`),
  CONSTRAINT `programacion_usuario_permission_id_f4021e00_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `programacion_usuario_usuario_id_9d49eaa6_fk_programac` FOREIGN KEY (`usuario_id`) REFERENCES `programacion_usuario` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `programacion_usuario_user_permissions`
--

LOCK TABLES `programacion_usuario_user_permissions` WRITE;
/*!40000 ALTER TABLE `programacion_usuario_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `programacion_usuario_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-06-18 18:57:17
