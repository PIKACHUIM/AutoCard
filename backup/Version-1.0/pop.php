<?php
    echo "<title>SCU自动打卡系统</title>";
    if($_POST['user']=='') {
        echo "<script>alert('请输入学号');</script>";
        echo "<script>history.back(-1);</script>";
    }
    else{
        $flag = 0;
        $cont = "";
        $file = fopen("passwd.ini", "r") 
        or die("【系统错误】无法读取数据库");
        while (!feof($file)) {
            $line=fgets($file);
            $arry=explode("|~|",$line);
            if($arry[0]==$_POST['user']) 
                $flag=1;
            else
                $cont=$cont.$line;
        }
        fclose($file);
        $file = fopen("passwd.ini", "w");
        fwrite($file, $cont);
        fclose($file);
        if($flag==0){
            echo "<script>alert('没有此用户信息');</script>";
            echo "<script>history.back(-1);</script>";
        }
        else{
            echo "<script>alert('撤销打卡成功！');</script>";
            echo "<script>window.location.href=\"index.php\";</script>";
        }
        //header('Location: index.php');
    }
?>