-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 04-12-2023 a las 22:18:38
-- Versión del servidor: 10.4.24-MariaDB
-- Versión de PHP: 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `lifa_empresa`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categoria`
--

CREATE TABLE `categoria` (
  `CategoriaId` int(11) NOT NULL,
  `Nombre` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `categoria`
--

INSERT INTO `categoria` (`CategoriaId`, `Nombre`) VALUES
(1, 'ELECTRICO'),
(2, 'MANUAL');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `deposito`
--

CREATE TABLE `deposito` (
  `DepositoId` int(11) NOT NULL,
  `Nombre` varchar(45) NOT NULL,
  `Descripcion` varchar(45) DEFAULT NULL,
  `FechaInicio` date DEFAULT NULL,
  `FechaFin` date DEFAULT NULL,
  `Estado` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `deposito`
--

INSERT INTO `deposito` (`DepositoId`, `Nombre`, `Descripcion`, `FechaInicio`, `FechaFin`, `Estado`) VALUES
(6, 'Central', 'Solis 299', '0000-00-00', '0000-00-00', 'EN PROCESO'),
(7, 'El Jardin', 'Independencia 198', '2023-06-16', '2023-12-01', 'EN PROCESO'),
(8, 'Consumo', 'Consumo de Herramientas/Materiales', '0000-00-00', '0000-00-00', 'EN PROCESO'),
(9, 'Perdidas', 'Perdidas de Herramientas/Materiales', '0000-00-00', '0000-00-00', 'EN PROCESO');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `deposito_herramienta`
--

CREATE TABLE `deposito_herramienta` (
  `Deposito_HerramientaId` int(10) NOT NULL,
  `Cantidad` int(10) NOT NULL,
  `HerramientaId` int(10) NOT NULL,
  `DepositoId` int(10) DEFAULT NULL,
  `Fecha` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `deposito_herramienta`
--

INSERT INTO `deposito_herramienta` (`Deposito_HerramientaId`, `Cantidad`, `HerramientaId`, `DepositoId`, `Fecha`) VALUES
(61, 4, 80, 6, '2023-11-13'),
(62, 12, 79, 7, '2023-11-13'),
(63, 95, 80, 7, '2023-11-13'),
(64, 10, 79, 6, '2023-11-13'),
(65, 18, 85, 6, '0000-00-00'),
(66, 8, 84, 6, '0000-00-00'),
(67, 6, 87, 6, '2023-11-20'),
(68, 1, 89, 6, '0000-00-00'),
(69, 2, 90, 6, '0000-00-00'),
(70, 1, 80, 8, '2023-12-04'),
(71, 1, 87, 7, '2023-12-04'),
(72, 4, 84, 7, '2023-12-04');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `deposito_material`
--

CREATE TABLE `deposito_material` (
  `Deposito_MaterialId` int(11) NOT NULL,
  `Cantidad` int(11) NOT NULL,
  `MaterialId` int(11) NOT NULL,
  `DepositoId` int(11) NOT NULL,
  `Fecha` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `deposito_material`
--

INSERT INTO `deposito_material` (`Deposito_MaterialId`, `Cantidad`, `MaterialId`, `DepositoId`, `Fecha`) VALUES
(19, 5, 2, 6, '2023-11-09'),
(20, 5, 3, 6, '2023-11-13'),
(21, 8, 2, 7, '2023-11-13'),
(22, 5, 3, 7, '2023-11-13'),
(23, 4, 6, 6, '0000-00-00'),
(24, 6, 6, 7, '2023-11-29'),
(25, 3, 2, 8, '2023-11-29');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `empleado`
--

CREATE TABLE `empleado` (
  `EmpleadoId` int(11) NOT NULL,
  `Nombre` varchar(45) NOT NULL,
  `FechaNacimiento` date NOT NULL,
  `Direccion` varchar(45) NOT NULL,
  `Telefono` varchar(45) NOT NULL,
  `Email` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `empleado`
--

INSERT INTO `empleado` (`EmpleadoId`, `Nombre`, `FechaNacimiento`, `Direccion`, `Telefono`, `Email`) VALUES
(2, 'Fernando', '1988-08-29', 'lamadrid 135', '42323132', 'fernado@gmail.com');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `herramienta`
--

CREATE TABLE `herramienta` (
  `HerramientaId` int(11) NOT NULL,
  `Nombre` varchar(45) NOT NULL,
  `CategoriaId` int(11) DEFAULT NULL,
  `Cantidad` int(11) DEFAULT NULL,
  `Estado` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `herramienta`
--

INSERT INTO `herramienta` (`HerramientaId`, `Nombre`, `CategoriaId`, `Cantidad`, `Estado`) VALUES
(79, 'RASTRILLO', 1, 22, 'FUNCIONA'),
(80, 'MARTILLO', 2, 100, 'FUNCIONA'),
(84, 'AMOLADORA', 1, 12, 'FUNCIONA'),
(85, 'MACHETE', 2, 18, 'FUNCIONA'),
(87, 'TESTER DIGITAL', 1, 7, 'FUNCIONA'),
(89, 'ALICATE', 2, 1, 'FUNCIONA'),
(90, 'MOUSE', 1, 2, 'FUNCIONA');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `material`
--

CREATE TABLE `material` (
  `MaterialId` int(11) NOT NULL,
  `Nombre` varchar(100) NOT NULL,
  `Descripcion` varchar(100) DEFAULT NULL,
  `Cantidad` int(11) NOT NULL,
  `Medida` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `material`
--

INSERT INTO `material` (`MaterialId`, `Nombre`, `Descripcion`, `Cantidad`, `Medida`) VALUES
(2, 'CEMENTO', 'Loma Negra', 16, 'UNIDAD'),
(3, 'RIPIO', 'EL MEJOR', 10, 'UNIDAD'),
(6, 'PLASTICOR', 'PLASTICOR MARCA LOMA NEGRA', 10, 'KILOGRAMO');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `movimientos`
--

CREATE TABLE `movimientos` (
  `MovimientoId` int(11) NOT NULL,
  `Tipo` varchar(50) NOT NULL,
  `Origen` int(11) DEFAULT NULL,
  `Destino` int(11) NOT NULL,
  `Fecha` date NOT NULL,
  `NumeroRemito` varchar(20) DEFAULT NULL,
  `ProveedorId` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `movimientos`
--

INSERT INTO `movimientos` (`MovimientoId`, `Tipo`, `Origen`, `Destino`, `Fecha`, `NumeroRemito`, `ProveedorId`) VALUES
(125, '2', 7, 6, '2023-11-17', '2', NULL),
(138, '1', 100, 6, '0000-00-00', '00001-8585100125', NULL),
(139, '1', 101, 6, '2023-11-21', '00001-858596', NULL),
(140, '2', 6, 7, '2023-11-29', '5', NULL),
(142, '2', 6, 8, '2023-11-29', '7', NULL),
(143, '2', 6, 8, '2023-12-04', '8', NULL),
(146, '2', 6, 7, '2023-12-04', '10', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `movimientos_detalle`
--

CREATE TABLE `movimientos_detalle` (
  `MovimientosDetalleId` int(11) NOT NULL,
  `MovimientosId` int(11) NOT NULL,
  `HerramientaId` int(11) DEFAULT NULL,
  `CantidadHerramienta` int(11) DEFAULT NULL,
  `MaterialId` int(11) DEFAULT NULL,
  `CantidadMaterial` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `movimientos_detalle`
--

INSERT INTO `movimientos_detalle` (`MovimientosDetalleId`, `MovimientosId`, `HerramientaId`, `CantidadHerramienta`, `MaterialId`, `CantidadMaterial`) VALUES
(13, 125, 80, 52, NULL, NULL),
(23, 138, NULL, NULL, 2, 2),
(24, 139, 87, 7, NULL, NULL),
(25, 140, NULL, NULL, 6, 5),
(26, 142, NULL, NULL, 2, 2),
(27, 143, 80, 3, NULL, NULL),
(28, 143, NULL, NULL, 2, 3),
(33, 146, 84, 2, NULL, NULL),
(34, 146, NULL, NULL, 3, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proveedor`
--

CREATE TABLE `proveedor` (
  `ProveedorId` int(11) NOT NULL,
  `NombreProveedor` varchar(45) NOT NULL,
  `Cuit` int(11) NOT NULL,
  `Direccion` varchar(45) NOT NULL,
  `Telefono` varchar(45) NOT NULL,
  `Email` varchar(45) NOT NULL,
  `Contacto` varchar(45) NOT NULL,
  `TelefonoContacto` varchar(45) NOT NULL,
  `Estado` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `proveedor`
--

INSERT INTO `proveedor` (`ProveedorId`, `NombreProveedor`, `Cuit`, `Direccion`, `Telefono`, `Email`, `Contacto`, `TelefonoContacto`, `Estado`) VALUES
(100, 'Lo Bruno', 2147483647, 'Solis 87', '42323132', 'lobruno@gmail.com', 'Perez Jose', '32312313', 'Activo'),
(101, 'CASA PVC', 187963976, 'COLON 89', '03854228578', 'casadelpvc@hotmail.com', 'Fernando', '3856987863', 'ACTIVO'),
(102, 'EL AMIGO', 2147483647, 'Belgrano 786', '03854227896', 'elamigo@hotmail.com', 'Daniel', '3856986347', 'ACTIVO');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `remito`
--

CREATE TABLE `remito` (
  `RemitoId` int(11) NOT NULL,
  `Fecha` date NOT NULL,
  `ProveedorId` int(11) NOT NULL,
  `UsuarioId` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `remitodetalle`
--

CREATE TABLE `remitodetalle` (
  `RemitoiD` int(11) NOT NULL,
  `HerramientasId` int(11) NOT NULL,
  `Cantidad` int(11) DEFAULT NULL,
  `Precio` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `rol_usuario`
--

CREATE TABLE `rol_usuario` (
  `idRol` int(11) NOT NULL,
  `Descripcion` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `rol_usuario`
--

INSERT INTO `rol_usuario` (`idRol`, `Descripcion`) VALUES
(1, 'Administrador'),
(2, 'Usuario');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `UsuarioId` int(11) NOT NULL,
  `correo` varchar(45) NOT NULL,
  `password` varchar(100) NOT NULL,
  `idRol` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`UsuarioId`, `correo`, `password`, `idRol`) VALUES
(6, 'diego09@hotmail.com', '$2b$12$Rd1rkgPT6CBN4xnh/m42G..mo5BEbmHKlAd6QRtUMZvK2RAGAHTyi', 1),
(7, 'dfpecora@gmail.com', '$2b$12$i7Ke/bTVJRI7d8mfGVnW2u1Gt9BdS.vDXgJj.aGgAfPdLvQdMg8BC', 1),
(19, 'luis@hotmail.com', '$2b$12$HdRFD/kJ5i3IuGijkiJd..DcpNPTWrpAa20jUv7oCUyaTsHqd565a', 2),
(20, 'luiscarranza@gmail.com', '$2b$12$EPFoDVFPefKM4kKYzci5zubxaL79zqmIeB/2Dt/Sd1wV/nGxfSBPO', 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `vehiculo`
--

CREATE TABLE `vehiculo` (
  `VehiculoId` int(7) NOT NULL,
  `Patente` varchar(10) NOT NULL,
  `Marca` varchar(45) NOT NULL,
  `Modelo` varchar(45) NOT NULL,
  `Año` int(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `vehiculo`
--

INSERT INTO `vehiculo` (`VehiculoId`, `Patente`, `Marca`, `Modelo`, `Año`) VALUES
(3, 'AG 198 KL', 'Toyota', 'Hilux', 2022);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `categoria`
--
ALTER TABLE `categoria`
  ADD PRIMARY KEY (`CategoriaId`) USING BTREE;

--
-- Indices de la tabla `deposito`
--
ALTER TABLE `deposito`
  ADD PRIMARY KEY (`DepositoId`) USING BTREE;

--
-- Indices de la tabla `deposito_herramienta`
--
ALTER TABLE `deposito_herramienta`
  ADD PRIMARY KEY (`Deposito_HerramientaId`),
  ADD KEY `HerramientaId` (`HerramientaId`),
  ADD KEY `deposito_herramienta_ibfk_2` (`DepositoId`);

--
-- Indices de la tabla `deposito_material`
--
ALTER TABLE `deposito_material`
  ADD PRIMARY KEY (`Deposito_MaterialId`);

--
-- Indices de la tabla `empleado`
--
ALTER TABLE `empleado`
  ADD PRIMARY KEY (`EmpleadoId`);

--
-- Indices de la tabla `herramienta`
--
ALTER TABLE `herramienta`
  ADD PRIMARY KEY (`HerramientaId`),
  ADD KEY `CategoriaId_idx` (`CategoriaId`) USING BTREE;

--
-- Indices de la tabla `material`
--
ALTER TABLE `material`
  ADD PRIMARY KEY (`MaterialId`) USING BTREE;

--
-- Indices de la tabla `movimientos`
--
ALTER TABLE `movimientos`
  ADD PRIMARY KEY (`MovimientoId`);

--
-- Indices de la tabla `movimientos_detalle`
--
ALTER TABLE `movimientos_detalle`
  ADD PRIMARY KEY (`MovimientosDetalleId`),
  ADD KEY `HerramientaId` (`HerramientaId`),
  ADD KEY `MaterialId` (`MaterialId`),
  ADD KEY `MovimientosId` (`MovimientosId`);

--
-- Indices de la tabla `proveedor`
--
ALTER TABLE `proveedor`
  ADD PRIMARY KEY (`ProveedorId`);

--
-- Indices de la tabla `remito`
--
ALTER TABLE `remito`
  ADD PRIMARY KEY (`RemitoId`),
  ADD KEY `UsuarioId_idx` (`UsuarioId`),
  ADD KEY `ProveedorId` (`ProveedorId`);

--
-- Indices de la tabla `remitodetalle`
--
ALTER TABLE `remitodetalle`
  ADD PRIMARY KEY (`RemitoiD`),
  ADD KEY `RemitoId_idx` (`RemitoiD`),
  ADD KEY `HerramientasId_idx` (`HerramientasId`);

--
-- Indices de la tabla `rol_usuario`
--
ALTER TABLE `rol_usuario`
  ADD PRIMARY KEY (`idRol`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`UsuarioId`),
  ADD KEY `idRol` (`idRol`);

--
-- Indices de la tabla `vehiculo`
--
ALTER TABLE `vehiculo`
  ADD PRIMARY KEY (`VehiculoId`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `deposito`
--
ALTER TABLE `deposito`
  MODIFY `DepositoId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `deposito_herramienta`
--
ALTER TABLE `deposito_herramienta`
  MODIFY `Deposito_HerramientaId` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=73;

--
-- AUTO_INCREMENT de la tabla `deposito_material`
--
ALTER TABLE `deposito_material`
  MODIFY `Deposito_MaterialId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT de la tabla `empleado`
--
ALTER TABLE `empleado`
  MODIFY `EmpleadoId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `herramienta`
--
ALTER TABLE `herramienta`
  MODIFY `HerramientaId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=91;

--
-- AUTO_INCREMENT de la tabla `material`
--
ALTER TABLE `material`
  MODIFY `MaterialId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `movimientos`
--
ALTER TABLE `movimientos`
  MODIFY `MovimientoId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=147;

--
-- AUTO_INCREMENT de la tabla `movimientos_detalle`
--
ALTER TABLE `movimientos_detalle`
  MODIFY `MovimientosDetalleId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT de la tabla `proveedor`
--
ALTER TABLE `proveedor`
  MODIFY `ProveedorId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=104;

--
-- AUTO_INCREMENT de la tabla `remitodetalle`
--
ALTER TABLE `remitodetalle`
  MODIFY `HerramientasId` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `rol_usuario`
--
ALTER TABLE `rol_usuario`
  MODIFY `idRol` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `UsuarioId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT de la tabla `vehiculo`
--
ALTER TABLE `vehiculo`
  MODIFY `VehiculoId` int(7) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `deposito_herramienta`
--
ALTER TABLE `deposito_herramienta`
  ADD CONSTRAINT `deposito_herramienta_ibfk_1` FOREIGN KEY (`HerramientaId`) REFERENCES `herramienta` (`HerramientaId`),
  ADD CONSTRAINT `deposito_herramienta_ibfk_2` FOREIGN KEY (`DepositoId`) REFERENCES `deposito` (`DepositoId`);

--
-- Filtros para la tabla `herramienta`
--
ALTER TABLE `herramienta`
  ADD CONSTRAINT `RubroId` FOREIGN KEY (`CategoriaId`) REFERENCES `categoria` (`CategoriaId`);

--
-- Filtros para la tabla `movimientos_detalle`
--
ALTER TABLE `movimientos_detalle`
  ADD CONSTRAINT `movimientos_detalle_ibfk_1` FOREIGN KEY (`MovimientosId`) REFERENCES `movimientos` (`MovimientoId`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `remito`
--
ALTER TABLE `remito`
  ADD CONSTRAINT `ProveedorId` FOREIGN KEY (`ProveedorId`) REFERENCES `proveedor` (`ProveedorId`);

--
-- Filtros para la tabla `remitodetalle`
--
ALTER TABLE `remitodetalle`
  ADD CONSTRAINT `HerramientasId` FOREIGN KEY (`HerramientasId`) REFERENCES `herramienta` (`HerramientaId`),
  ADD CONSTRAINT `RemitoId` FOREIGN KEY (`RemitoiD`) REFERENCES `remito` (`RemitoId`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
