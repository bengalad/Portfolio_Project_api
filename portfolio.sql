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
   priceAtPurchase          decimal(10,2)               NULL,
   qty        decimal(10,2)           NULL ,
   PRIMARY KEY(id)
);

CREATE TABLE bonds
(
   id         varchar(11)           NOT NULL,
   holdingName       varchar(40)           NULL,
   dateOfPurchase           date           NULL,
   priceAtPurchase          decimal(10,2)               NULL,
   qty        decimal(10,2)           NULL ,
   parValue          decimal(10,2)               NULL,
   maturityDate           date           NULL,
   PRIMARY KEY(id)
);

CREATE TABLE cash
(
   id         varchar(11)           NOT NULL,
   holdingName       varchar(40)           NULL,
   dateOfPurchase           date           NULL,
   exchAtPurchase          decimal(10,2)               NULL,
   exchCurrent          decimal(10,2)               NULL,
   qty        decimal(10,2)           NULL ,
   PRIMARY KEY(id)
);


insert stocks
   values('1', 'Stock1', '2023-10-01', 10.99,
   10);
   insert stocks
   values('2', 'Stock2', '2023-10-11', 9.99,
   6);
   insert stocks
   values('3', 'Stock3', '2023-10-05', 15.99,
   50);

insert bonds
   values('4', 'Bond1', '2023-10-01', 10.99,
   10, 100, '2025-10-01');
insert bonds
   values('5', 'Bond2', '2023-8-11', 3.99,
   8, 300, '2024-10-01');
insert bonds
   values('6', 'Bond3', '2023-8-05', 7.99,
   100, 500, '2024-10-01');
   
insert cash
   values('7', 'Cash1', '2023-10-01', 10.99,
	10.99, 10);
insert cash
   values('8', 'Cash2', '2023-8-11', 3.99,
   5.99, 100);
insert cash
   values('9', 'Cash3', '2023-8-05', 7.99,
   6.99, 100);
   


