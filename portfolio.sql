CREATE DATABASE portfolio;
USE portfolio;
CREATE TABLE stocks
(
   id         int           NOT NULL	auto_increment,
   holdingName       varchar(40)           NULL,
   dateOfPurchase           date           NULL,
   priceAtPurchase          decimal(10,2)               NULL,
   qty        decimal(10,2)           NULL ,
   currentPrice  decimal(10,2) 			NULL,
   ticker varchar(20) NOT NULL,
   PRIMARY KEY(id)
);

CREATE TABLE bonds
(
   id         int           NOT NULL auto_increment,
   holdingName       varchar(40)           NULL,
   dateOfPurchase           date           NULL,
   priceAtPurchase          decimal(10,2)               NULL,
   qty        decimal(10,2)           NULL ,
   coupon decimal(10,2) NULL,
   discountRate decimal(10,2) NULL,
   parValue          decimal(10,2)               NULL,
   maturityDate           date           NULL,
   currentPrice  decimal(10,2) 			NULL,
   PRIMARY KEY(id)
);

CREATE TABLE cash
(
   id         int           NOT NULL auto_increment,
   holdingName       varchar(40)           NULL,
   dateOfPurchase           date           NULL,
   exchAtPurchase          decimal(10,2)               NULL,
   exchCurrent          decimal(10,2)               NULL,
   qty        decimal(10,2)           NULL ,
   currentValue  decimal(10,2) 			NULL,
   ticker varchar(20) NOT NULL,
   PRIMARY KEY(id)
);


INSERT INTO stocks (holdingName, dateOfPurchase, priceAtPurchase, qty, currentPrice, ticker)
   values('Apple', '2023-07-31', 190, 5, 12.99, 'AAPL');
   insert stocks (holdingName, dateOfPurchase, priceAtPurchase, qty, currentPrice, ticker)
   values('Crocs', '2020-01-06', 43, 10, 44, 'CROX');
   insert stocks (holdingName, dateOfPurchase, priceAtPurchase, qty, currentPrice, ticker)
   values('NVIDIA', '2023-10-10', 112, 2, 100, 'NVDA');

insert into bonds (holdingName, dateOfPurchase, priceAtPurchase, qty, coupon,
   discountRate, parValue, maturityDate)          
   values('Ford Motors', '2022-08-08', 105, 1, 6.24, 0.05, 1000, '2028-10-01');
insert into bonds (holdingName, dateOfPurchase, priceAtPurchase, qty, coupon,
   discountRate, parValue, maturityDate)
   values('UK GILT', '2023-08-21', 92.25,
   5, 58, 0.052, 100, '2025-08-21');
   
insert into cash (holdingName, dateOfPurchase, exchAtPurchase, exchCurrent, qty, currentValue, ticker)
   values('GPB', '2022-11-11', 1.18, 2, 100, 140, 'GBPUSD=X');
insert into cash (holdingName, dateOfPurchase, exchAtPurchase, exchCurrent, qty, currentValue, ticker)
   values('Euros', '2018-10-01', 1.13, 1.2, 200, 190, 'EURUSD=X');
