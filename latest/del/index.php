<html>
    <head>
        <title>SCU自动打卡系统</title>
        <meta name="viewport" content="width=device-width,initial-scale=1.0, minimum-scale=1.0 maximum-scale=1.0, user-scalable=no"/>
        <link rel="stylesheet" href="../css/style.css">
    </head>
    <body>
        <h1>SCU自动打卡系统</h1>
        <h2>撤销自动打卡 - 验证</h2>
        <form action="saves.php" method="post">
            <br />
            <div class="">
                <input style="width:95%;max-width:800px" name='user' type="text"  placeholder="学号">
            </div>
            <input id="login-vertoken" name="token" type="hidden" required data-msg="请完成验证" class="input-material" />
            <div id="c1" style="min-width:24.5em;padding:2%;max-width:800px"></div>
            <br />
            <button style="width:95%;background-color: #FF3030;max-width:800px" type="submit">确认信息无误，撤销打卡</button>
        </form>  
		<a href="../index.php">
			<button style="width:95%;background-color: #A9A9A9;max-width:800px" >返回</button>
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
