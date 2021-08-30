<?php
echo $_POST['type'];
	include '../mod/db.php';
    echo "<title>SCU自动打卡系统</title>";
    if($_POST['user']=='') {
        echo "<script>alert('请输入学号！');</script>";
        echo "<script>history.back(-1);</script>";
    }
	elseif($_POST['type']!=1 && db_getc("pc_user","user",$_POST['user'],"pass")!='') {
        echo "<script>alert('你已添加过！');</script>";
        echo "<script>history.back(-1);</script>";
    }
    elseif($_POST['pass']=='' && $_POST['type']!=1) {
        echo "<script>alert('请输入密码！');</script>";
        echo "<script>history.back(-1);</script>";
    }
    elseif($_POST['mail']=='') {
        echo "<script>alert('请输入邮箱！');</script>";
        echo "<script>history.back(-1);</script>";
    }
	elseif(!filter_var($_POST['mail'], FILTER_VALIDATE_EMAIL)) {
        echo "<script>alert('检查邮箱格式');</script>";
        echo "<script>history.back(-1);</script>";
    }
    else{
		if($_POST['type']!=1){
			$save_sql = "INSERT INTO pc_user (user,pass,mail,flag,tips,time,name) VALUES("
			."'".$_POST['user']."',"
			."'".$_POST['pass']."',"
			."'".$_POST['mail']."',"
			."'".$_POST['flag']."',"
			."'".$_POST['tips']."',"
			."'".$_POST['time']."',"
			."'".$_POST['name']."')";
			db_exec($save_sql);
			echo "<script>alert('添加打卡成功！');</script>";
		}
		else{
			if($_POST['pass']!='')
			db_putc("pc_user","user",$_POST['user'],"pass","'".$_POST['pass']."'");
			db_putc("pc_user","user",$_POST['user'],"mail","'".$_POST['mail']."'");
			db_putc("pc_user","user",$_POST['user'],"flag","'".$_POST['flag']."'");
			db_putc("pc_user","user",$_POST['user'],"tips","'".$_POST['tips']."'");
			db_putc("pc_user","user",$_POST['user'],"name","'".$_POST['name']."'");
			db_putc("pc_user","user",$_POST['user'],"time","'".$_POST['time']."'");
			echo "<script>alert('修改信息成功！');</script>";
		}
        echo "<script>window.location.href=\"../index.php\";</script>";
    }
?>