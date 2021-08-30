<?php
	include '../mod/db.php';
    echo "<title>SCU自动打卡系统</title>";
    if($_POST['user']=='') {
        echo "<script>alert('请输入学号');</script>";
        echo "<script>history.back(-1);</script>";
    }
    else{
        if(db_getc("pc_user","user",$_POST['user'],"pass")==''){
            echo "<script>alert('没有此用户信息');</script>";
            echo "<script>history.back(-1);</script>";
        }
        else{
			db_delc("pc_user","user",$_POST['user']);
            echo "<script>alert('撤销打卡成功！');</script>";
            echo "<script>window.location.href=\"../index.php\";</script>";
        }
        //header('Location: index.php');
    }
?>