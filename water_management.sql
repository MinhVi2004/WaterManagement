-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Máy chủ: 127.0.0.1
-- Thời gian đã tạo: Th4 29, 2025 lúc 09:50 AM
-- Phiên bản máy phục vụ: 10.4.32-MariaDB
-- Phiên bản PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Cơ sở dữ liệu: `water_management`
--

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `bills`
--

CREATE TABLE `bills` (
  `id` int(11) NOT NULL,
  `customer_id` int(11) NOT NULL,
  `meter_id` int(11) NOT NULL,
  `reading_id` int(11) NOT NULL,
  `amount` int(11) NOT NULL,
  `totalBill` bigint(20) NOT NULL,
  `status` enum('Chờ Thanh Toán','Đã Thanh Toán','Quá Hạn') DEFAULT 'Chờ Thanh Toán',
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `processed_by` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `bills`
--

INSERT INTO `bills` (`id`, `customer_id`, `meter_id`, `reading_id`, `amount`, `totalBill`, `status`, `created_at`, `processed_by`) VALUES
(2, 1, 1, 5, 250, 750, 'Chờ Thanh Toán', '2025-04-25 00:00:00', 1),
(3, 1, 1, 6, 475000, 142500, 'Chờ Thanh Toán', '2025-04-25 00:00:00', 1),
(6, 1, 2, 9, 3000, 900, 'Chờ Thanh Toán', '2025-04-26 14:40:56', 1),
(7, 1, 2, 10, 500, 1500000, 'Chờ Thanh Toán', '2025-04-26 14:43:23', 1),
(8, 3, 8, 11, 100, 300000, 'Chờ Thanh Toán', '2025-04-26 17:59:50', 1),
(9, 3, 8, 12, 400, 1200000, 'Chờ Thanh Toán', '2025-04-26 18:31:32', 1);

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `customers`
--

CREATE TABLE `customers` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `address` varchar(255) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `status` enum('Bình Thường','Vô Hiệu Hóa') NOT NULL DEFAULT 'Bình Thường'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `customers`
--

INSERT INTO `customers` (`id`, `name`, `email`, `phone`, `address`, `created_at`, `status`) VALUES
(1, 'Minh Vi', 'dvmv2017@gmail.com', '0772912452', 'Hóc Môn 123, Tphcm', '2025-03-25 00:00:00', 'Bình Thường'),
(3, 'Minh Vi 2', 'dvmv2021@gmail.com', '0772912453', '63/2e ', '2025-03-25 00:00:00', 'Bình Thường');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `employees`
--

CREATE TABLE `employees` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `phone` varchar(255) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('ADMIN','STAFF') NOT NULL DEFAULT 'STAFF',
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `status` bit(1) NOT NULL DEFAULT b'1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `employees`
--

INSERT INTO `employees` (`id`, `name`, `phone`, `email`, `password`, `role`, `created_at`, `status`) VALUES
(1, 'Staff 01', '0911253098', 'staff', 'minhvi', 'STAFF', '2025-03-25 13:34:14', b'0'),
(2, 'Admin', '0772924524', 'admin', 'admin', 'ADMIN', '2025-04-15 13:28:46', b'1'),
(3, 'Abc', '1232131231', '312312@ga.com', '3213123', 'STAFF', '2000-01-01 00:00:00', b'0'),
(6, 'Abc', '0123456789', '123@ga.com', '3213123', 'STAFF', '2000-01-01 00:00:00', b'1');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `meter_readings`
--

CREATE TABLE `meter_readings` (
  `id` int(11) NOT NULL,
  `meter_id` int(11) NOT NULL,
  `reading_before` decimal(30,2) NOT NULL,
  `reading_value` decimal(30,2) NOT NULL,
  `image_url` varchar(255) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `meter_readings`
--

INSERT INTO `meter_readings` (`id`, `meter_id`, `reading_before`, `reading_value`, `image_url`, `created_at`) VALUES
(3, 1, 500.00, 2000.00, 'abc', '2025-04-25 14:05:03'),
(4, 1, 2000.00, 2250.00, '1_1_25042025_165308.jpg', '2025-04-25 16:53:16'),
(5, 1, 2250.00, 2500.00, '1_1_25042025_170338.jpg', '2025-04-25 17:03:41'),
(6, 1, 2500.00, 50000.00, '1_1_25042025_170757.jpg', '2025-04-25 17:08:01'),
(7, 2, 0.00, 2000.00, '2_2_26042025_142323.jpg', '2025-04-26 14:23:28'),
(8, 2, 2000.00, 2200.00, '2_2_26042025_142659.jpg', '2025-04-26 14:27:03'),
(9, 2, 2200.00, 2500.00, '1_2_26042025_144055.jpg', '2025-04-26 14:40:56'),
(10, 2, 2500.00, 3000.00, '1_2_26042025_144318.jpg', '2025-04-26 14:43:23'),
(11, 8, 0.00, 100.00, '3_8_26042025_175948.jpg', '2025-04-26 17:59:50'),
(12, 8, 100.00, 500.00, '3_8_26042025_183128.jpg', '2025-04-26 18:31:32');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `water_meters`
--

CREATE TABLE `water_meters` (
  `id` int(11) NOT NULL,
  `customer_id` int(11) NOT NULL,
  `meter_number` bigint(20) NOT NULL DEFAULT 0,
  `location` varchar(255) NOT NULL,
  `installed_at` datetime NOT NULL DEFAULT current_timestamp(),
  `status` enum('Bình Thường','Vô Hiệu Hóa') NOT NULL DEFAULT 'Bình Thường'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `water_meters`
--

INSERT INTO `water_meters` (`id`, `customer_id`, `meter_number`, `location`, `installed_at`, `status`) VALUES
(1, 1, 50000, 'Hóc Môn', '2025-03-25 13:33:26', 'Bình Thường'),
(2, 1, 3000, 'Quận 5', '2025-04-25 14:41:02', 'Bình Thường'),
(3, 3, 0, 'Tây Ninh', '2025-04-26 16:06:12', 'Bình Thường'),
(8, 3, 500, 'Hà Nội', '2025-04-26 17:57:02', 'Bình Thường');

--
-- Chỉ mục cho các bảng đã đổ
--

--
-- Chỉ mục cho bảng `bills`
--
ALTER TABLE `bills`
  ADD PRIMARY KEY (`id`),
  ADD KEY `customer_id` (`customer_id`),
  ADD KEY `meter_id` (`meter_id`),
  ADD KEY `reading_id` (`reading_id`),
  ADD KEY `processed_by` (`processed_by`);

--
-- Chỉ mục cho bảng `customers`
--
ALTER TABLE `customers`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Chỉ mục cho bảng `employees`
--
ALTER TABLE `employees`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `phone` (`phone`);

--
-- Chỉ mục cho bảng `meter_readings`
--
ALTER TABLE `meter_readings`
  ADD PRIMARY KEY (`id`),
  ADD KEY `meter_id` (`meter_id`);

--
-- Chỉ mục cho bảng `water_meters`
--
ALTER TABLE `water_meters`
  ADD PRIMARY KEY (`id`),
  ADD KEY `customer_id` (`customer_id`);

--
-- AUTO_INCREMENT cho các bảng đã đổ
--

--
-- AUTO_INCREMENT cho bảng `bills`
--
ALTER TABLE `bills`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT cho bảng `customers`
--
ALTER TABLE `customers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT cho bảng `employees`
--
ALTER TABLE `employees`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT cho bảng `meter_readings`
--
ALTER TABLE `meter_readings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT cho bảng `water_meters`
--
ALTER TABLE `water_meters`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Các ràng buộc cho các bảng đã đổ
--

--
-- Các ràng buộc cho bảng `bills`
--
ALTER TABLE `bills`
  ADD CONSTRAINT `bills_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `bills_ibfk_2` FOREIGN KEY (`meter_id`) REFERENCES `water_meters` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `bills_ibfk_3` FOREIGN KEY (`reading_id`) REFERENCES `meter_readings` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `bills_ibfk_4` FOREIGN KEY (`processed_by`) REFERENCES `employees` (`id`) ON DELETE SET NULL;

--
-- Các ràng buộc cho bảng `meter_readings`
--
ALTER TABLE `meter_readings`
  ADD CONSTRAINT `meter_readings_ibfk_1` FOREIGN KEY (`meter_id`) REFERENCES `water_meters` (`id`) ON DELETE CASCADE;

--
-- Các ràng buộc cho bảng `water_meters`
--
ALTER TABLE `water_meters`
  ADD CONSTRAINT `water_meters_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
