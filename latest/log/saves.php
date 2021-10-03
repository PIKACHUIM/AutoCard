<?php
    require_once('../checker.php');
    checkcode($_POST['token'])
?>
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
    }
?>
<html>
    <head>
        <title>SCU自动打卡系统</title>
        <meta name="viewport" content="width=device-width,initial-scale=1.0, minimum-scale=1.0 maximum-scale=1.0, user-scalable=no"/>
        <link rel="stylesheet" href="../css/style.css">
    </head>
    <body>
        <h2>SCU自动打卡系统</h2>
        <h3>查看打卡日志 - 信息</h3>
        <h4>用户账号：<?php echo db_getc("pc_user","user",$_POST['user'],"user"); ?></h4>
		<h4>用户邮箱：<?php echo db_getc("pc_user","user",$_POST['user'],"mail"); ?></h4>
		<h4>用户姓名：<?php echo db_getc("pc_user","user",$_POST['user'],"name"); ?></h4>
		<h4>启用打卡：
		<?php 
			if(db_getc("pc_user","user",$_POST['user'],"flag")==0) echo "停用"; 
			if(db_getc("pc_user","user",$_POST['user'],"flag")==1) echo "启用"; 
		?></h4>
		<h4>打卡时间：<?php 
			if(db_getc("pc_user","user",$_POST['user'],"time")==0) echo "每日09:00打卡"; 
			if(db_getc("pc_user","user",$_POST['user'],"time")==1) echo "每日00:10打卡"; 
			if(db_getc("pc_user","user",$_POST['user'],"time")==2) echo "每日07:00打卡"; 
			if(db_getc("pc_user","user",$_POST['user'],"time")==3) echo "每日11:00打卡"; 
		?></h4>
		<h4>成功次数：<?php echo db_getc("pc_user","user",$_POST['user'],"succ"); ?></h4>
		<h4>失败次数：<?php echo db_getc("pc_user","user",$_POST['user'],"fail"); ?></h4>
		<table border="1" style="width:40%">
			<tr>
				<th>编号</th>
				<th>时间</th>
				<th>账号</th>
				<th>状态</th>
				<th>信息</th>
			</tr>
			<?php 
			$saves_data = db_exec("SELECT * FROM pc_logs WHERE user=".$_POST['user']);
			while ($tmp = $saves_data->fetch_row()){
				echo '<tr>';
				echo '<td>'.$tmp[0].'</td>';
				echo '<td>'.$tmp[1].'</td>';
				echo '<td>'.$tmp[2].'</td>';
				echo '<td>'.$tmp[3].'</td>';
				echo '<td>'.$tmp[4].'</td>';
				echo '</tr>';
			}
			?>
		</table>
		<br/>
		<a href="../index.php">
			<button style="width:100%;max-width:960px;background-color: #7FFFAA" >返回</button>
		</a>
    </body>
</html>
