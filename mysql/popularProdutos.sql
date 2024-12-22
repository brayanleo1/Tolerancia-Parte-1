USE `ecomerce2`;

-- Inserindo dados na tabela Product
INSERT INTO `Product` (`name`, `value`) VALUES
('Product A', 19.99),
('Product B', 29.99),
('Product C', 39.99),
('Product D', 49.99);

-- Inserindo dados na tabela User
INSERT INTO `User` (`Bonus`) VALUES
(0050),
(0100),
(0200),
(0005);



-- Inserindo dados na tabela Transaction
INSERT INTO `Transaction` (`idTransaction`, `Product_idProduct`) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 1);
