-- phpMyAdmin SQL Dump
-- version 4.9.0.1
-- https://www.phpmyadmin.net/
--
-- 主机： localhost:3306
-- 生成日期： 2021-02-04 20:21:49
-- 服务器版本： 5.6.44-log
-- PHP 版本： 7.3.21

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 数据库： `pika_card`
--

-- --------------------------------------------------------

--
-- 表的结构 `pc_info`
--

CREATE TABLE `pc_info` (
  `id` tinyint(4) NOT NULL COMMENT '数据编号',
  `name` text NOT NULL COMMENT '数据名称',
  `data` text NOT NULL COMMENT '数据内容',
  `tips` text NOT NULL COMMENT '数据备注'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `pc_info`
--

INSERT INTO `pc_info` (`id`, `name`, `data`, `tips`) VALUES
(1, 'mail_user', '', '邮箱地址'),
(2, 'mail_pass', '', '邮箱密码'),
(3, 'mail_host', '', '邮箱网址'),
(4, 'mail_port', '', '邮箱端口');

-- --------------------------------------------------------

--
-- 表的结构 `pc_logs`
--

CREATE TABLE `pc_logs` (
  `dkid` bigint(11) NOT NULL COMMENT '打卡编号',
  `time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '打卡时间',
  `user` text NOT NULL COMMENT '用户编号',
  `flag` text NOT NULL COMMENT '打卡状态',
  `info` text NOT NULL COMMENT '详细信息'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `pc_user`
--

CREATE TABLE `pc_user` (
  `user` bigint(20) NOT NULL COMMENT '用户学号',
  `pass` text NOT NULL COMMENT '用户密码',
  `mail` text NOT NULL COMMENT '用户邮箱',
  `succ` smallint(6) NOT NULL DEFAULT '0' COMMENT '成功次数',
  `fail` smallint(6) DEFAULT '0' COMMENT '失败次数',
  `flag` tinyint(1) NOT NULL COMMENT '启用打卡',
  `tips` tinyint(1) NOT NULL COMMENT '邮件通知',
  `time` tinyint(4) NOT NULL COMMENT '自定时间',
  `name` text NOT NULL COMMENT '用户姓名'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转储表的索引
--

--
-- 表的索引 `pc_info`
--
ALTER TABLE `pc_info`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `pc_logs`
--
ALTER TABLE `pc_logs`
  ADD PRIMARY KEY (`dkid`);

--
-- 表的索引 `pc_user`
--
ALTER TABLE `pc_user`
  ADD PRIMARY KEY (`user`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
