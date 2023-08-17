CREATE DATABASE portfolio;

USE portfolio;

CREATE TABLE holdings
(
   id          varchar(11) 	    NOT NULL,
   holdingName       varchar(40)       NOT NULL,
   holdingType       varchar(20)       NOT NULL,
   PRIMARY KEY(id)
);

CREATE TABLE stocks
(
   id         varchar(11)           NOT NULL,
   holdingName       varchar(40)           NULL,
   dateOfPurchase           date           NULL,
   priceAtPurchase          decimal(4,2)               NULL,
   qty        decimal(4,2)           NULL ,
   PRIMARY KEY(id)
);

CREATE TABLE bonds
(
   id         varchar(11)           NOT NULL,
   holdingName       varchar(40)           NULL,
   dateOfPurchase           date           NULL,
   priceAtPurchase          decimal(4,2)               NULL,
   qty        decimal(4,2)           NULL ,
   parValue          decimal(4,2)               NULL,
   maturityDate           date           NULL,
   PRIMARY KEY(id)
);

CREATE TABLE cash
(
   id         varchar(11)           NOT NULL,
   holdingName       varchar(40)           NULL,
   dateOfPurchase           date           NULL,
   exchAtPurchase          decimal(4,2)               NULL,
   exchCurrent          decimal(4,2)               NULL,
   qty        decimal(4,2)           NULL ,
   PRIMARY KEY(id)
);
