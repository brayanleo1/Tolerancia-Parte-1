-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema ecomerce2
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema ecomerce2
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `ecomerce2` ;
USE `ecomerce2` ;

-- -----------------------------------------------------
-- Table `ecomerce2`.`Product`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ecomerce2`.`Product` (
  `idProduct` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `value` FLOAT NOT NULL,
  PRIMARY KEY (`idProduct`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ecomerce2`.`User`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ecomerce2`.`User` (
  `idUser` INT NOT NULL AUTO_INCREMENT,
  `Bonus` INT ZEROFILL NOT NULL,
  PRIMARY KEY (`idUser`))
ENGINE = InnoDB;



-- -----------------------------------------------------
-- Table `ecomerce2`.`Transaction`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ecomerce2`.`Transaction` (
  `idTransaction` INT NOT NULL,
  `Product_idProduct` INT NOT NULL,
  PRIMARY KEY (`idTransaction`),
  INDEX `fk_Transaction_Product1_idx` (`Product_idProduct` ASC) VISIBLE,
  CONSTRAINT `fk_Transaction_Product1`
    FOREIGN KEY (`Product_idProduct`)
    REFERENCES `ecomerce2`.`Product` (`idProduct`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
