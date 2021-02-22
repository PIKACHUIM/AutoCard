<?php
    echo "<title>SCU自动打卡系统</title>";
    if($_POST['user']=='') {
        echo "<script>alert('请输入学号');</script>";
        echo "<script>history.back(-1);</script>";
    }
    elseif($_POST['pass']=='') {
        echo "<script>alert('请输入密码');</script>";
        echo "<script>history.back(-1);</script>";
    }
    elseif($_POST['mail']=='') {
        echo "<script>alert('请输入邮箱');</script>";
        echo "<script>history.back(-1);</script>";
    }
    else{
        $file = fopen("passwd.ini", "a") 
        or die("【系统错误】无法读取数据库");
        $text = $_POST['user']."|~|".$_POST['pass']."|~|".$_POST['mail']."\n";
        fwrite($file, $text);
        fclose($file);
        echo "<script>alert('添加打卡成功！');</script>";
        echo "<script>window.location.href=\"index.php\";</script>";
        //header('Location: index.php');
    }
?>