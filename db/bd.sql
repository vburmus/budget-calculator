-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`user` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `login` VARCHAR(45) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `balance` FLOAT 0,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `login_UNIQUE` (`login` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`account`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`account` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `description` VARCHAR(45) NULL,
  `user_id` BIGINT NOT NULL,
  `balance` FLOAT 0,
   PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `fk_Account_User1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_Account_User1`
    FOREIGN KEY (`user_id`)
    REFERENCES `mydb`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`type`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`type` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`kategory`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`kategory` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`transaction`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`transaction` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `amount` VARCHAR(45) NOT NULL,
  `description` VARCHAR(45) NULL,
  `date` VARCHAR(45) NOT NULL,
  `account_id` BIGINT NOT NULL,
  `type_id` BIGINT NOT NULL,
  `kategory_id` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `fk_Spend_Account1_idx` (`account_id` ASC) VISIBLE,
  INDEX `fk_Spend_Type1_idx` (`type_id` ASC) VISIBLE,
  INDEX `fk_Spend_Kategory1_idx` (`kategory_id` ASC) VISIBLE,
  CONSTRAINT `fk_Spend_Account1`
    FOREIGN KEY (`account_id`)
    REFERENCES `mydb`.`account` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Spend_Type1`
    FOREIGN KEY (`type_id`)
    REFERENCES `mydb`.`type` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Spend_Kategory1`
    FOREIGN KEY (`kategory_id`)
    REFERENCES `mydb`.`kategory` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

-- -----------------------------------------------------
-- Data for table `mydb`.`type`
-- -----------------------------------------------------
START TRANSACTION;
USE `mydb`;
INSERT INTO `mydb`.`type` (`id`, `name`) VALUES (1, 'income');
INSERT INTO `mydb`.`type` (`id`, `name`) VALUES (2, 'expense');

COMMIT;


-- -----------------------------------------------------
-- Data for table `mydb`.`kategory`
-- -----------------------------------------------------
START TRANSACTION;
USE `mydb`;
INSERT INTO `mydb`.`kategory` (`id`, `name`) VALUES (1, 'Food');
INSERT INTO `mydb`.`kategory` (`id`, `name`) VALUES (2, 'Housing');
INSERT INTO `mydb`.`kategory` (`id`, `name`) VALUES (3, 'Transport');
INSERT INTO `mydb`.`kategory` (`id`, `name`) VALUES (4, 'Vehicle');
INSERT INTO `mydb`.`kategory` (`id`, `name`) VALUES (5, 'Entertainment');
INSERT INTO `mydb`.`kategory` (`id`, `name`) VALUES (6, 'Shopping');
INSERT INTO `mydb`.`kategory` (`id`, `name`) VALUES (7, 'Communication');
INSERT INTO `mydb`.`kategory` (`id`, `name`) VALUES (8, 'Default');
COMMIT;

