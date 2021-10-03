<?php 
	include '../mod/db.php';
	if($_GET['type']==1)
		if(db_getc("pc_user","user",$_GET['user'],"pass")==''){
			echo "<script>alert('找不到此学号');</script>";
			echo "<script>history.back(-1);</script>";
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
	<?php
		if($_GET['type']!=1)
			echo "
			<h3>步骤一</h3>
			<h4><a href='https://wfw.scu.edu.cn/ncov/wap/default/index' target='_blank'>前往微服务</a>&nbsp;&nbsp;确认你的学号和密码</h4>
			<h4>此步骤十分重要，请务必前往确认</h4>
			<h3>步骤二</h3>
			";
		else
			echo "<h3>打卡设置与信息修改 - 数据</h3>"
	?>
        
        <form action="saves.php" method="post">
            <br />
            <div class="">学号：
                <input  style="width:80%;max-width:530px" name='user' type="text" placeholder="学号"                     value='<?php 
					echo db_getc("pc_user","user",$_GET['user'],"user"); 
				?>' <?php if($_GET['type']==1) echo 'readonly="readonly"'; ?> />
            </div>
            <br />
            <div class="">密码：
				<?php
					if($_GET['type']!=1)
						echo '<input style="width:80%;max-width:530px" name="pass" type="password" placeholder="密码 (微服务登录密码)">';
					else
						echo '<input style="width:80%;max-width:530px" name="pass" type="password" placeholder="密码 (留空则不会修改)">';
				?>
            </div>
            <br />
            <div class="">邮箱：
                <input style="width:80%;max-width:530px" name='mail' type="mail"     placeholder="邮箱 (必填，用于通知)" value='<?php 
					echo db_getc("pc_user","user",$_GET['user'],"mail"); 
				?>'>
            </div>
            <br />
			<div class="">姓名：
                <input style="width:80%;max-width:530px" name='name' type="text"     placeholder="姓名 (必填，找回密码）" value='<?php 
					echo db_getc("pc_user","user",$_GET['user'],"name"); 
				?>'>
            </div>
            <br />
			<div class="">
                <div style="display:inline">打卡时间：</div>
                <select name='time' style="width:71%;max-width:490px" >
                    <option value="0" <?php if(db_getc("pc_user","user",$_GET['user'],"time")==0) echo "selected"; ?> >每日09:00打卡</option>
                    <option value="1" <?php if(db_getc("pc_user","user",$_GET['user'],"time")==1) echo "selected"; ?> >每日00:10打卡</option>
					<option value="2" <?php if(db_getc("pc_user","user",$_GET['user'],"time")==2) echo "selected"; ?> >每日07:00打卡</option>
					<option value="3" <?php if(db_getc("pc_user","user",$_GET['user'],"time")==3) echo "selected"; ?> >每日11:00打卡</option>
                </select>
            </div>
			<br />
			<div class="">
                <div style="display:inline">自动打卡：</div>
                <select name='flag' style="width:71%;max-width:490px">
                    <option value="1" <?php if($_GET['type']!=1 || db_getc("pc_user","user",$_GET['user'],"flag")==1) echo "selected"; ?> >启用自动打卡</option>
                    <option value="0" <?php if($_GET['type']==1 && db_getc("pc_user","user",$_GET['user'],"flag")==0) echo "selected"; ?> >停用自动打卡</option>
                </select>
            </div>
            <br />
            <div class="">
                <div style="display:inline">邮件通知：</div>
                <select name='tips' style="width:71%;max-width:490px" >
					<option value="0"  <?php if(db_getc("pc_user","user",$_GET['user'],"tips")==0) echo "selected"; ?> >失败时才发送</option>
                    <option value="1"  <?php if(db_getc("pc_user","user",$_GET['user'],"tips")==1) echo "selected"; ?> >总是发送邮件</option>
                </select>
            </div>
            <br />
            
            <input id="login-vertoken" name="token" type="hidden" required data-msg="请完成验证" class="input-material" />
            <div id="c1" style="min-width:24.5em;padding:2%;max-width:550px"></div>
            
			<input hidden name='type' value='<?php echo $_GET['type']; ?>'><br />
            <button type="submit" style="background-color: #1E90FF;max-width:600px" >确认上述信息无误，提交数据</button>
        </form>
		<a href="../index.php">
			<button style="background-color: #A9A9A9;max-width:600px" >返回</button>
		</a>
		<script src="https://cdn.dingxiang-inc.com/ctu-group/captcha-ui/index.js"></script>
        <script type="text/javascript">var passtoken = "";
            var myCaptcha = _dx.Captcha(document.getElementById('c1'), {
                appId: 'b4f11125fb26b4fd3010ba2146cf36a7',
                style: 'inline',
                inlineFloatPosition: 'down',
                success: function(token) {
                    passtoken = token;
                    document.getElementById("login-vertoken").value = passtoken;
                }
            })
        </script>
    </body>
</html>
