-- MySQL dump 10.13  Distrib 8.0.27, for Linux (x86_64)
--
-- Host: localhost    Database: proj
-- ------------------------------------------------------
-- Server version	8.0.27-0ubuntu0.20.04.1

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
-- Table structure for table `adminApp_banner`
--

DROP TABLE IF EXISTS `adminApp_banner`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `adminApp_banner` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `bannerimg` varchar(100) DEFAULT NULL,
  `p_id_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `adminApp_banner_p_id_id_9a295753_fk_products_id` (`p_id_id`),
  CONSTRAINT `adminApp_banner_p_id_id_9a295753_fk_products_id` FOREIGN KEY (`p_id_id`) REFERENCES `products` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `adminApp_banner`
--

LOCK TABLES `adminApp_banner` WRITE;
/*!40000 ALTER TABLE `adminApp_banner` DISABLE KEYS */;
INSERT INTO `adminApp_banner` VALUES (1,'images/banner4.jpg',2),(2,'images/banner2.jpg',1);
/*!40000 ALTER TABLE `adminApp_banner` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `adminApp_coupen`
--

DROP TABLE IF EXISTS `adminApp_coupen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `adminApp_coupen` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `coupen_offer` int NOT NULL,
  `coupen_code` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `coupen_code` (`coupen_code`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `adminApp_coupen`
--

LOCK TABLES `adminApp_coupen` WRITE;
/*!40000 ALTER TABLE `adminApp_coupen` DISABLE KEYS */;
/*!40000 ALTER TABLE `adminApp_coupen` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
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
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add user',6,'add_customuser'),(22,'Can change user',6,'change_customuser'),(23,'Can delete user',6,'delete_customuser'),(24,'Can view user',6,'view_customuser'),(25,'Can add cart',7,'add_cart'),(26,'Can change cart',7,'change_cart'),(27,'Can delete cart',7,'delete_cart'),(28,'Can view cart',7,'view_cart'),(29,'Can add address',8,'add_address'),(30,'Can change address',8,'change_address'),(31,'Can delete address',8,'delete_address'),(32,'Can view address',8,'view_address'),(33,'Can add order',9,'add_order'),(34,'Can change order',9,'change_order'),(35,'Can delete order',9,'delete_order'),(36,'Can view order',9,'view_order'),(37,'Can add whishlist',10,'add_whishlist'),(38,'Can change whishlist',10,'change_whishlist'),(39,'Can delete whishlist',10,'delete_whishlist'),(40,'Can view whishlist',10,'view_whishlist'),(41,'Can add category',11,'add_category'),(42,'Can change category',11,'change_category'),(43,'Can delete category',11,'delete_category'),(44,'Can view category',11,'view_category'),(45,'Can add sub category',12,'add_subcategory'),(46,'Can change sub category',12,'change_subcategory'),(47,'Can delete sub category',12,'delete_subcategory'),(48,'Can view sub category',12,'view_subcategory'),(49,'Can add products',13,'add_products'),(50,'Can change products',13,'change_products'),(51,'Can delete products',13,'delete_products'),(52,'Can view products',13,'view_products'),(53,'Can add variant and price',14,'add_variantandprice'),(54,'Can change variant and price',14,'change_variantandprice'),(55,'Can delete variant and price',14,'delete_variantandprice'),(56,'Can view variant and price',14,'view_variantandprice'),(57,'Can add banner',15,'add_banner'),(58,'Can change banner',15,'change_banner'),(59,'Can delete banner',15,'delete_banner'),(60,'Can view banner',15,'view_banner'),(61,'Can add coupen',16,'add_coupen'),(62,'Can change coupen',16,'change_coupen'),(63,'Can delete coupen',16,'delete_coupen'),(64,'Can view coupen',16,'view_coupen');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cart`
--

DROP TABLE IF EXISTS `cart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cart` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `quantity` bigint NOT NULL,
  `user_id_id` bigint DEFAULT NULL,
  `variant_id_id` bigint NOT NULL,
  `subtotal` bigint NOT NULL,
  `guest_user` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `cart_user_id_id_aeb465f1_fk_userApp_customuser_id` (`user_id_id`),
  KEY `cart_variant_id_id_1ec238e9_fk_variantandprice_id` (`variant_id_id`),
  CONSTRAINT `cart_user_id_id_aeb465f1_fk_userApp_customuser_id` FOREIGN KEY (`user_id_id`) REFERENCES `userApp_customuser` (`id`),
  CONSTRAINT `cart_variant_id_id_1ec238e9_fk_variantandprice_id` FOREIGN KEY (`variant_id_id`) REFERENCES `variantandprice` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cart`
--

LOCK TABLES `cart` WRITE;
/*!40000 ALTER TABLE `cart` DISABLE KEYS */;
INSERT INTO `cart` VALUES (14,1,3,1,41399,NULL),(15,1,3,4,9900,NULL),(18,7,2,3,90083,'NULL');
/*!40000 ALTER TABLE `cart` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `category` varchar(100) NOT NULL,
  `offer` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `category_category_71494cb3_uniq` (`category`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES (2,'ANDROID',1),(3,'IOS',0);
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
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
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_userApp_customuser_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_userApp_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `userApp_customuser` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(15,'adminApp','banner'),(11,'adminApp','category'),(16,'adminApp','coupen'),(13,'adminApp','products'),(12,'adminApp','subcategory'),(14,'adminApp','variantandprice'),(3,'auth','group'),(2,'auth','permission'),(4,'contenttypes','contenttype'),(5,'sessions','session'),(8,'userApp','address'),(7,'userApp','cart'),(6,'userApp','customuser'),(9,'userApp','order'),(10,'userApp','whishlist');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=74 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2022-02-16 06:15:57.152826'),(2,'contenttypes','0002_remove_content_type_name','2022-02-16 06:16:06.964271'),(3,'auth','0001_initial','2022-02-16 06:16:40.431966'),(4,'auth','0002_alter_permission_name_max_length','2022-02-16 06:16:46.377167'),(5,'auth','0003_alter_user_email_max_length','2022-02-16 06:16:46.946793'),(6,'auth','0004_alter_user_username_opts','2022-02-16 06:16:47.249622'),(7,'auth','0005_alter_user_last_login_null','2022-02-16 06:16:47.837255'),(8,'auth','0006_require_contenttypes_0002','2022-02-16 06:16:48.196336'),(9,'auth','0007_alter_validators_add_error_messages','2022-02-16 06:16:48.627472'),(10,'auth','0008_alter_user_username_max_length','2022-02-16 06:16:48.908380'),(11,'auth','0009_alter_user_last_name_max_length','2022-02-16 06:16:49.212618'),(12,'auth','0010_alter_group_name_max_length','2022-02-16 06:16:50.062668'),(13,'auth','0011_update_proxy_permissions','2022-02-16 06:16:50.566234'),(14,'auth','0012_alter_user_first_name_max_length','2022-02-16 06:16:50.912748'),(15,'userApp','0001_initial','2022-02-16 06:17:26.705872'),(16,'admin','0001_initial','2022-02-16 06:17:41.644941'),(17,'admin','0002_logentry_remove_auto_add','2022-02-16 06:17:42.056121'),(18,'admin','0003_logentry_add_action_flag_choices','2022-02-16 06:17:42.586445'),(19,'adminApp','0001_initial','2022-02-16 06:17:52.768631'),(20,'adminApp','0002_alter_category_category','2022-02-16 06:17:54.750618'),(21,'adminApp','0003_products','2022-02-16 06:17:57.142941'),(22,'adminApp','0004_alter_products_table','2022-02-16 06:17:59.135174'),(23,'adminApp','0005_products_product_name_alter_products_img1','2022-02-16 06:18:00.834244'),(24,'adminApp','0006_alter_products_img1','2022-02-16 06:18:01.114793'),(25,'adminApp','0007_alter_products_img1','2022-02-16 06:18:01.424632'),(26,'adminApp','0008_products_back_camera_products_battery_and_more','2022-02-16 06:18:36.186127'),(27,'adminApp','0009_alter_variantandprice_product_id','2022-02-16 06:18:50.217391'),(28,'adminApp','0010_alter_products_date','2022-02-16 06:18:56.214170'),(29,'adminApp','0011_alter_products_date','2022-02-16 06:18:57.038746'),(30,'adminApp','0012_auto_20220120_1757','2022-02-16 06:19:05.496602'),(31,'adminApp','0013_banner','2022-02-16 06:19:13.698235'),(32,'adminApp','0014_rename_annerimg_banner_bannerimg','2022-02-16 06:19:14.579158'),(33,'adminApp','0015_rename_product_id_banner_p_id','2022-02-16 06:19:22.750222'),(34,'adminApp','0016_category_offer','2022-02-16 06:19:25.246969'),(35,'adminApp','0017_alter_category_offer','2022-02-16 06:19:25.662251'),(36,'adminApp','0018_auto_20220202_0317','2022-02-16 06:19:35.455633'),(37,'adminApp','0019_coupen','2022-02-16 06:19:38.428299'),(38,'adminApp','0020_alter_coupen_coupen_offer','2022-02-16 06:19:49.895263'),(39,'adminApp','0021_alter_coupen_coupen_offer','2022-02-16 06:19:57.959057'),(40,'adminApp','0022_auto_20220209_0201','2022-02-16 06:19:58.351332'),(41,'adminApp','0023_products_processor','2022-02-16 06:20:01.027458'),(42,'adminApp','0024_alter_products_processor','2022-02-16 06:20:01.382948'),(43,'adminApp','0025_alter_category_offer','2022-02-16 06:20:01.908439'),(44,'sessions','0001_initial','2022-02-16 06:20:06.436423'),(45,'userApp','0002_customuser_block','2022-02-16 06:20:09.244561'),(46,'userApp','0003_alter_customuser_number','2022-02-16 06:20:11.309189'),(47,'userApp','0004_customuser_image','2022-02-16 06:20:13.537088'),(48,'userApp','0005_remove_customuser_image_customuser_profile','2022-02-16 06:20:20.279439'),(49,'userApp','0006_remove_customuser_profile_pic','2022-02-16 06:20:32.910472'),(50,'userApp','0007_customuser_profile_delete_pic','2022-02-16 06:20:36.165613'),(51,'userApp','0008_remove_customuser_profile','2022-02-16 06:20:41.877189'),(52,'userApp','0009_cart','2022-02-16 06:20:55.673652'),(53,'userApp','0010_alter_cart_table','2022-02-16 06:20:57.452573'),(54,'userApp','0011_alter_cart_quantity','2022-02-16 06:20:57.789742'),(55,'userApp','0012_alter_cart_variant_id','2022-02-16 06:21:06.042251'),(56,'userApp','0013_cart_subtotal','2022-02-16 06:21:09.761488'),(57,'userApp','0014_alter_cart_subtotal','2022-02-16 06:21:10.066319'),(58,'userApp','0015_address','2022-02-16 06:21:12.348460'),(59,'userApp','0016_address_user_id','2022-02-16 06:21:18.674985'),(60,'userApp','0017_order','2022-02-16 06:21:26.070908'),(61,'userApp','0018_order_product_id','2022-02-16 06:21:32.450225'),(62,'userApp','0019_auto_20220121_1847','2022-02-16 06:21:47.872733'),(63,'userApp','0020_auto_20220126_1445','2022-02-16 06:22:16.511715'),(64,'userApp','0021_auto_20220126_1447','2022-02-16 06:22:30.696798'),(65,'userApp','0022_order_payment_method','2022-02-16 06:22:33.503344'),(66,'userApp','0023_alter_order_payment_method','2022-02-16 06:22:33.792400'),(67,'userApp','0024_auto_20220131_1400','2022-02-16 06:22:48.699080'),(68,'userApp','0025_alter_order_address','2022-02-16 06:22:49.222666'),(69,'userApp','0026_alter_order_variant_id','2022-02-16 06:22:49.762985'),(70,'userApp','0027_order_coupen_id','2022-02-16 06:22:58.257517'),(71,'userApp','0028_auto_20220209_0454','2022-02-16 06:23:15.128583'),(72,'userApp','0029_auto_20220209_0636','2022-02-16 06:23:40.726261'),(73,'userApp','0030_whishlist','2022-02-16 06:23:55.435304');
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
INSERT INTO `django_session` VALUES ('p8a8lx4qqckjzxlyzb8dyd6erhitmstm','.eJxVjTsOwyAQRO9CbSE-xmCX6XMGtCybQOKPZOwmUe4eLLlI2nkzb97Mw74lvxdafY5sYJI1v1kAfNJ8gPiA-b5wXOZtzYEfFX7Swq9LpPFydv8ECUqqa3AKJXbkoupCb1EZq2XQARwpodrOobXOGHsjamXV9ggALRJEpZ0SpkpXeHmYNjb0QjgtRMOOg-ouCVKeC4x5Yp8vVrNEYw:1nLRDs:bV4TvF2vTvu-tG1RfBoj8I50ATKDvWk9Em6pRiOyBCo','2022-03-05 15:00:32.845857');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `img1` varchar(100) DEFAULT NULL,
  `product_name` varchar(200) NOT NULL,
  `back_camera` int DEFAULT NULL,
  `battery` bigint DEFAULT NULL,
  `brand_id_id` bigint DEFAULT NULL,
  `date` datetime(6) NOT NULL,
  `front_camera` int DEFAULT NULL,
  `img2` varchar(100) DEFAULT NULL,
  `img3` varchar(100) DEFAULT NULL,
  `offer` int NOT NULL,
  `rom` int DEFAULT NULL,
  `processor` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `products_brand_id_id_fd793d1a_fk_subcategory_id` (`brand_id_id`),
  CONSTRAINT `products_brand_id_id_fd793d1a_fk_subcategory_id` FOREIGN KEY (`brand_id_id`) REFERENCES `subcategory` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (1,'images/pixel3_1.jpeg','pixel',30,4500,4,'2022-02-16 07:00:40.837504',42,'images/pixel2_1.jpeg','images/pixel3_1_Qzful4O.jpeg',0,84,'MediaTek'),(2,'images/reame9i3.jpeg','narzo 30 A',8,45000,2,'2022-02-16 07:05:02.013980',13,'images/realme9i2.jpeg','images/samsung1.jpeg',0,64,'MediaTek'),(3,'images/133.jpeg','11 pro max',12,4000,1,'2022-02-16 08:21:48.227915',12,'images/132_1.jpeg','images/131.jpeg',0,54,'bionic');
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subcategory`
--

DROP TABLE IF EXISTS `subcategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `subcategory` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `brand_name` varchar(100) NOT NULL,
  `c_id_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `subcategory_c_id_id_4f021a9e_fk_category_id` (`c_id_id`),
  CONSTRAINT `subcategory_c_id_id_4f021a9e_fk_category_id` FOREIGN KEY (`c_id_id`) REFERENCES `category` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subcategory`
--

LOCK TABLES `subcategory` WRITE;
/*!40000 ALTER TABLE `subcategory` DISABLE KEYS */;
INSERT INTO `subcategory` VALUES (1,'iphone',3),(2,'Realme',2),(3,'MI',2),(4,'Google',2);
/*!40000 ALTER TABLE `subcategory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userApp_address`
--

DROP TABLE IF EXISTS `userApp_address`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `userApp_address` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `full_name` varchar(50) NOT NULL,
  `city` varchar(50) NOT NULL,
  `mobile_number` varchar(10) NOT NULL,
  `zipcode` varchar(6) NOT NULL,
  `address` longtext NOT NULL,
  `user_id_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `userApp_address_user_id_id_94a6c651_fk_userApp_customuser_id` (`user_id_id`),
  CONSTRAINT `userApp_address_user_id_id_94a6c651_fk_userApp_customuser_id` FOREIGN KEY (`user_id_id`) REFERENCES `userApp_customuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userApp_address`
--

LOCK TABLES `userApp_address` WRITE;
/*!40000 ALTER TABLE `userApp_address` DISABLE KEYS */;
INSERT INTO `userApp_address` VALUES (13,'shahin salim','idukki','8921849804','682021','mangalasseil kerala india\r\ngandp gens hostile',1),(16,'shahin salim','idukki','8921849804','682021','mangalasseil kerala india\r\ngandp gens hostile',2),(17,'shahin salim','idukki','8921849804','682021','mangalasseil kerala india\r\ngandp gens hostile',2);
/*!40000 ALTER TABLE `userApp_address` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userApp_customuser`
--

DROP TABLE IF EXISTS `userApp_customuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `userApp_customuser` (
  `id` bigint NOT NULL AUTO_INCREMENT,
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
  `number` varchar(100) NOT NULL,
  `block` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `userApp_customuser_number_9de3d932_uniq` (`number`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userApp_customuser`
--

LOCK TABLES `userApp_customuser` WRITE;
/*!40000 ALTER TABLE `userApp_customuser` DISABLE KEYS */;
INSERT INTO `userApp_customuser` VALUES (1,'pbkdf2_sha256$260000$ChLzHUV0jIE66PEjhwb70u$8CnEVW/vuvymm0urSrvPr9PuGbZYnpzeOjgUP3/nkrI=','2022-02-16 17:16:37.682409',1,'shahin','','','',1,1,'2022-02-16 06:25:01.791360','',0),(2,'pbkdf2_sha256$260000$TnVJWWruFuyd7iEk89vE0e$zY6mfUg1l2XntOkG4TgZO2jodaxRXAFs4uWdRNVbDcI=',NULL,0,'shahinsalim','shahin','shahin','shahinsalim82@gmail.com',0,1,'2022-02-16 06:27:26.279054','8921849804',0),(3,'pbkdf2_sha256$260000$9FV17Zngn6bvpc60B4D77T$+jtQGBV7QRo+kJ8SEdTWn4PmjfI8B2+0Kw4VDZFTexg=',NULL,0,'roshas','roshas','johnson','roshas@gmail.com',0,1,'2022-02-18 11:30:39.074230','7012598205',0);
/*!40000 ALTER TABLE `userApp_customuser` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userApp_customuser_groups`
--

DROP TABLE IF EXISTS `userApp_customuser_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `userApp_customuser_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customuser_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `userApp_customuser_groups_customuser_id_group_id_13af19f1_uniq` (`customuser_id`,`group_id`),
  KEY `userApp_customuser_groups_group_id_9ea84ae9_fk_auth_group_id` (`group_id`),
  CONSTRAINT `userApp_customuser_g_customuser_id_8509e990_fk_userApp_c` FOREIGN KEY (`customuser_id`) REFERENCES `userApp_customuser` (`id`),
  CONSTRAINT `userApp_customuser_groups_group_id_9ea84ae9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userApp_customuser_groups`
--

LOCK TABLES `userApp_customuser_groups` WRITE;
/*!40000 ALTER TABLE `userApp_customuser_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `userApp_customuser_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userApp_customuser_user_permissions`
--

DROP TABLE IF EXISTS `userApp_customuser_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `userApp_customuser_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customuser_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `userApp_customuser_user__customuser_id_permission_adcdd779_uniq` (`customuser_id`,`permission_id`),
  KEY `userApp_customuser_u_permission_id_0d6201db_fk_auth_perm` (`permission_id`),
  CONSTRAINT `userApp_customuser_u_customuser_id_a7a40a81_fk_userApp_c` FOREIGN KEY (`customuser_id`) REFERENCES `userApp_customuser` (`id`),
  CONSTRAINT `userApp_customuser_u_permission_id_0d6201db_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userApp_customuser_user_permissions`
--

LOCK TABLES `userApp_customuser_user_permissions` WRITE;
/*!40000 ALTER TABLE `userApp_customuser_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `userApp_customuser_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userApp_order`
--

DROP TABLE IF EXISTS `userApp_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `userApp_order` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `total_qty` bigint NOT NULL,
  `date` datetime(6) NOT NULL,
  `order_status` varchar(100) NOT NULL,
  `userId_id` bigint NOT NULL,
  `subtotal` bigint NOT NULL,
  `variant_id_id` bigint DEFAULT NULL,
  `order_id` char(32) NOT NULL,
  `payment_method` varchar(100) NOT NULL,
  `address` longtext NOT NULL,
  `coupen_id_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `userApp_order_userId_id_457c822f_fk_userApp_customuser_id` (`userId_id`),
  KEY `userApp_order_variant_id_id_4cfb0eff_fk_variantandprice_id` (`variant_id_id`),
  KEY `userApp_order_coupen_id_id_4219c515_fk_adminApp_coupen_id` (`coupen_id_id`),
  CONSTRAINT `userApp_order_coupen_id_id_4219c515_fk_adminApp_coupen_id` FOREIGN KEY (`coupen_id_id`) REFERENCES `adminApp_coupen` (`id`),
  CONSTRAINT `userApp_order_userId_id_457c822f_fk_userApp_customuser_id` FOREIGN KEY (`userId_id`) REFERENCES `userApp_customuser` (`id`),
  CONSTRAINT `userApp_order_variant_id_id_4cfb0eff_fk_variantandprice_id` FOREIGN KEY (`variant_id_id`) REFERENCES `variantandprice` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userApp_order`
--

LOCK TABLES `userApp_order` WRITE;
/*!40000 ALTER TABLE `userApp_order` DISABLE KEYS */;
INSERT INTO `userApp_order` VALUES (1,1,'2022-02-16 07:13:15.186001','Delivered',2,45999,1,'81e12299ba674ed3a449eac09dac6015','Razorpay','Full name: shahin salim address: mangalasseil kerala india\r\ngandp gens hostile city: idukki pincode: 682021 mobile: 8921849804',NULL),(2,1,'2022-02-16 09:50:38.548812','Admin cancell',2,12869,3,'9903463d94344927a4e7824eab53c8ba','Cash On Delivery','Full name: shahin salim address: mangalasseil kerala india\r\ngandp gens hostile city: idukki pincode: 682021 mobile: 8921849804',NULL),(3,1,'2022-02-16 10:46:32.889059','Returned',2,41399,1,'442c35b2313c4542b1600b2c532461ff','Cash On Delivery','Full name: shahin salim address: mangalasseil kerala india\r\ngandp gens hostile city: idukki pincode: 682021 mobile: 8921849804',NULL),(4,2,'2022-02-16 11:34:49.387102','Delivered',2,25738,3,'5ac1fe2b85f74eef8450da48dfd02ab2','PayPal','Full name: shahin salim address: mangalasseil kerala india\r\ngandp gens hostile city: idukki pincode: 682021 mobile: 8921849804',NULL),(5,1,'2022-02-16 11:34:51.370303','Delivered',2,41399,1,'d82fe5dbcf134a00a58125eed10e5ab0','PayPal','Full name: shahin salim address: mangalasseil kerala india\r\ngandp gens hostile city: idukki pincode: 682021 mobile: 8921849804',NULL),(6,1,'2022-02-16 11:34:53.045940','Delivered',2,79999,5,'01ce8acd930a40dcbf3b086a56650baa','PayPal','Full name: shahin salim address: mangalasseil kerala india\r\ngandp gens hostile city: idukki pincode: 682021 mobile: 8921849804',NULL),(7,3,'2022-02-16 11:35:43.167585','Admin cancell',2,239997,5,'4868f435e33f457fa63fe142b7ac8c9e','Razorpay','Full name: shahin salim address: mangalasseil kerala india\r\ngandp gens hostile city: idukki pincode: 682021 mobile: 8921849804',NULL),(8,3,'2022-02-16 11:35:44.900172','Delivered',2,124197,1,'74baeff17f3241369f1dc088e0220462','Razorpay','Full name: shahin salim address: mangalasseil kerala india\r\ngandp gens hostile city: idukki pincode: 682021 mobile: 8921849804',NULL),(9,1,'2022-02-16 11:37:37.572861','Delivered',2,12869,3,'d5bb80c9715f4b2282c9a13ab54b996c','PayPal','Full name: shahin salim address: mangalasseil kerala india\r\ngandp gens hostile city: idukki pincode: 682021 mobile: 8921849804',NULL),(10,1,'2022-02-16 11:39:38.723428','Delivered',2,11582,3,'82eb89ee37574e0b94f85677abcf0d71','PayPal','Full name: shahin salim address: mangalasseil kerala india\r\ngandp gens hostile city: idukki pincode: 682021 mobile: 8921849804',NULL),(11,1,'2022-02-16 13:45:12.714021','Cancelled',1,12869,3,'7025bc4b78c6434bb0b89f8e7e8dcd70','PayPal','Full name: shahin salim address: mangalasseil kerala india\r\ngandp gens hostile city: idukki pincode: 682021 mobile: 8921849804',NULL),(12,1,'2022-02-16 17:24:37.968013','Admin cancell',2,9900,4,'006d9b2d4dc347f1a74938184e971c0c','PayPal','Full name: shahin salim address: mangalasseil kerala india\r\ngandp gens hostile city: idukki pincode: 682021 mobile: 8921849804',NULL),(13,1,'2022-02-16 17:26:28.871925','Delivered',2,9900,4,'7cb1a8b052a2424dbd069966f72f7fa3','PayPal','Full name: shahin salim address: mangalasseil kerala india\r\ngandp gens hostile city: idukki pincode: 682021 mobile: 8921849804',NULL),(14,1,'2022-02-17 05:07:30.616954','Delivered',2,12869,3,'edd43ee0e13c468da1c066bcddeb1cb0','Cash On Delivery','Full name: shahin salim address: mangalasseil kerala india\r\ngandp gens hostile city: idukki pincode: 682021 mobile: 8921849804',NULL),(15,2,'2022-02-17 05:07:32.703348','Returned',2,19800,4,'f1adf3308e044c899e330fc1b8e3dab7','Cash On Delivery','Full name: shahin salim address: mangalasseil kerala india\r\ngandp gens hostile city: idukki pincode: 682021 mobile: 8921849804',NULL),(16,1,'2022-02-18 16:47:12.554477','Cancelled',2,41399,1,'b93cee1cb792455d8f061112283c7416','Cash On Delivery','Full name: shahin salim address: mangalasseil kerala india\r\ngandp gens hostile city: idukki pincode: 682021 mobile: 8921849804',NULL),(17,1,'2022-02-19 10:40:06.949503','Order Placed',2,22499,2,'dabad495033a478a9e0e72f35081eb10','PayPal','Full name: shahin salim address: mangalasseil kerala india\r\ngandp gens hostile city: idukki pincode: 682021 mobile: 8921849804',NULL),(18,3,'2022-02-19 10:41:47.383453','Order Placed',2,29700,4,'df8cb64b84334b7b83ecf0dad5385926','Razorpay','Full name: shahin salim address: mangalasseil kerala india\r\ngandp gens hostile city: idukki pincode: 682021 mobile: 8921849804',NULL),(19,1,'2022-02-19 10:41:48.477356','Order Placed',2,22499,2,'9116f3912a884ae6a8d88e9a044bee8b','Razorpay','Full name: shahin salim address: mangalasseil kerala india\r\ngandp gens hostile city: idukki pincode: 682021 mobile: 8921849804',NULL);
/*!40000 ALTER TABLE `userApp_order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userApp_whishlist`
--

DROP TABLE IF EXISTS `userApp_whishlist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `userApp_whishlist` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `product_variant_id` bigint NOT NULL,
  `user_id_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `userApp_whishlist_product_variant_id_bb5c93aa_fk_variantan` (`product_variant_id`),
  KEY `userApp_whishlist_user_id_id_383417a0_fk_userApp_customuser_id` (`user_id_id`),
  CONSTRAINT `userApp_whishlist_product_variant_id_bb5c93aa_fk_variantan` FOREIGN KEY (`product_variant_id`) REFERENCES `variantandprice` (`id`),
  CONSTRAINT `userApp_whishlist_user_id_id_383417a0_fk_userApp_customuser_id` FOREIGN KEY (`user_id_id`) REFERENCES `userApp_customuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userApp_whishlist`
--

LOCK TABLES `userApp_whishlist` WRITE;
/*!40000 ALTER TABLE `userApp_whishlist` DISABLE KEYS */;
INSERT INTO `userApp_whishlist` VALUES (3,1,1),(4,5,1),(11,4,3),(12,3,3),(13,1,2);
/*!40000 ALTER TABLE `userApp_whishlist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `variantandprice`
--

DROP TABLE IF EXISTS `variantandprice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `variantandprice` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `variant` int NOT NULL,
  `price` bigint NOT NULL,
  `product_id_id` bigint DEFAULT NULL,
  `quantity` int NOT NULL,
  `final_price` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `variantandprice_product_id_id_e04d3e59_fk_products_id` (`product_id_id`),
  CONSTRAINT `variantandprice_product_id_id_e04d3e59_fk_products_id` FOREIGN KEY (`product_id_id`) REFERENCES `products` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `variantandprice`
--

LOCK TABLES `variantandprice` WRITE;
/*!40000 ALTER TABLE `variantandprice` DISABLE KEYS */;
INSERT INTO `variantandprice` VALUES (1,12,45999,1,5,45539),(2,6,24999,1,8,24749),(3,6,12999,2,10,12869),(4,4,10000,2,0,9900),(5,6,79999,3,2,79999),(6,8,99999,3,8,99999);
/*!40000 ALTER TABLE `variantandprice` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-02-19 20:43:05
