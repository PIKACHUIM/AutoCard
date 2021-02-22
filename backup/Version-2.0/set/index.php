<html>
    <head>
        <title>SCU自动打卡系统</title>
        <meta name="viewport" content="width=device-width,initial-scale=1.0, minimum-scale=1.0 maximum-scale=1.0, user-scalable=no"/>
    </head>
    <body>
        <h1>SCU自动打卡系统</h1>
        <h2>设置打卡信息 - 验证</h2>
        <form action="../add/index.php" method="get">
            <br />
            <div class="">
                <input style="width:100%" name='user' type="text"  placeholder="学号">
            </div>
			<input hidden name='type' value='1'>
            <br />
            <button style="width:100%" type="submit">下一步</button>
        </form>  
		<a href="../index.php">
			<button style="width:100%" >返回</button>
		</a>
    </body>
</html>
