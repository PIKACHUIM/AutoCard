<html>
    <head>
        <title>SCU自动打卡系统</title>
        <meta name="viewport" content="width=device-width,initial-scale=1.8, minimum-scale=1.8 maximum-scale=1.8, user-scalable=no"/>
    </head>
    <body>
        <h2>SCU自动打卡系统</h2>
        <h3>步骤一</h3>
        <a href="https://wfw.scu.edu.cn/ncov/wap/default/index">前往微服务</a>确认学号和密码
        <h3>步骤二</h3>
        <form action="new.php" method="post">
            <br />
            <div class="">
                <input name='user' type="text"     placeholder="学号">
            </div>
            <br />
            <div class="">
                <input name='pass' type="password" placeholder="密码">
            </div>
            <br />
            <div class="">
                <input name='mail' type="mail" placeholder="邮箱">
            </div>
            <br />
            <div class="">
                <div style="display:inline">邮件通知：</div>
                <select name='sets' disabled="disabled">
                    <option value="1">总是发送邮件</option>
                    <option value="0">永不发送邮件</option>
                    <option value="2">失败时才发送</option>
                </select>
            </div>
            <br />
            <button type="submit">确认上述信息无误，提交数据</button>
        </form>  
    </body>
</html>
