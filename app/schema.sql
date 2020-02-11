-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema ece1779
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema ece1779
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `ece1779` DEFAULT CHARACTER SET utf8 ;
USE `ece1779` ;

-- -----------------------------------------------------
-- Table `ece1779`.`account`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ece1779`.`account` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(100) NOT NULL,
  `password_hash` BINARY(32) NOT NULL,
  `salt` BINARY(4) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ece1779`.`photo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ece1779`.`photo` (
  `id` INT NOT NULL,
  `account_id` INT NOT NULL,
  `name` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `fk_photo_account_idx` (`account_id` ASC) VISIBLE,
  CONSTRAINT `fk_photo_account`
    FOREIGN KEY (`account_id`)
    REFERENCES `ece1779`.`account` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
