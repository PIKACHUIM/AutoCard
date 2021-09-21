<html>
    <head>
        <title>SCU自动打卡系统 2.4</title>
        <meta name="viewport" content="width=device-width,initial-scale=1.0, minimum-scale=1.0 maximum-scale=1.0, user-scalable=no"/>
        <style>
                button {
                    
                    background-image: -webkit-linear-gradient(hsla(0,0%,100%,.05), hsla(0,0%,0%,.1));
                    background-image:    -moz-linear-gradient(hsla(0,0%,100%,.05), hsla(0,0%,0%,.1));
                    background-image:     -ms-linear-gradient(hsla(0,0%,100%,.05), hsla(0,0%,0%,.1));
                    background-image:      -o-linear-gradient(hsla(0,0%,100%,.05), hsla(0,0%,0%,.1));
                    background-image:         linear-gradient(hsla(0,0%,100%,.05), hsla(0,0%,0%,.1));
                    border: none;
                    border-radius: .5em;
                    box-shadow: inset 0 0 0 1px hsla(0,0%,0%,.2),
                                inset 0 2px 0 hsla(0,0%,100%,.1),
                                inset 0 1.2em 0 hsla(0,0%,100%,0.1),
                                inset 0 -.2em 0 hsla(0,0%,100%,.1),
                                inset 0 -.25em 0 hsla(0,0%,0%,.25),
                                0 .25em .25em hsla(0,0%,0%,.05);
                    color: #fff;
                    cursor: pointer;
                    display: inline-block;
                    font-family: sans-serif;
                    font-size: 1em;
                    font-weight: bold;
                    line-height: 1.5;
                    margin: 0 .5em 1em;
                    padding: .5em 1.5em .75em;
                    position: relative;
                    text-decoration: none;
                    text-shadow: 0 1px 1px hsla(0,0%,100%,.25);
                    vertical-align: middle;
            }
            button:hover {
                    outline: none;
            }
            button:hover,
            button:focus {
                    box-shadow: inset 0 0 0 1px hsla(0,0%,0%,.2),
                                inset 0 2px 0 hsla(0,0%,100%,.1),
                                inset 0 1.2em 0 hsla(0,0%,100%,.1),
                                inset 0 -.2em 0 hsla(0,0%,100%,.1),
                                inset 0 -.25em 0 hsla(0,0%,0%,.25),
                                inset 0 0 0 3em hsla(0,0%,100%,.2),
                                0 .25em .25em hsla(0,0%,0%,.05);
            }
            button:active {
                    box-shadow: inset 0 0 0 1px hsla(0,0%,0%,.2),
                                inset 0 2px 0 hsla(0,0%,100%,.1),
                                inset 0 1.2em 0 hsla(0,0%,100%,.1),
                                inset 0 0 0 3em hsla(0,0%,100%,.2),
                                inset 0 .25em .5em hsla(0,0%,0%,.05),
                                0 -1px 1px hsla(0,0%,0%,.1),
                                0 1px 1px hsla(0,0%,100%,.25);
                    margin-top: .25em;
                    outline: none;
                    padding-bottom: .5em;
            }                  
        </style>
    </head>
    <body>
        <div style="width:100%">
		<h1 align=center>SCU自动打卡系统</h1>
            <h2 align=center>
            版本2.4 使用说明
            </h2>
            <div style="font-size:18px" align=center>
                本系统每天按照你选择的时间进行打卡
                <br />
                失败会发送邮件
                <br /><br />
                自动打卡使用昨天的数据
                <br />
                <b>因此本系统不会收集你的隐私信息</b>
                <br /><br />
                如果需要手动打卡
                <br />
                请在设置时间前打卡或者撤销打卡
                <br />
            </div>
        </div>
        <center>
        <br />
        <button type="button" style="width:80%;background-color: #1E90FF;max-width:600px" onclick="window.location.href='/add/?type=0'">添加打卡账号</button>
        <br />
        <button type="button" style="width:80%;background-color: #FF3030;max-width:600px" onclick="window.location.href='/del/'">撤销自动打卡</button>
        <br />
        <button type="button" style="width:80%;background-color: #FFD700;max-width:600px" onclick="window.location.href='/set/'">编辑打卡信息</button>
        <br />
        <button type="button" style="width:80%;background-color: #00FF00;max-width:600px" onclick="window.location.href='/log/'">查看打卡历史</button>
        </center>
    </body>
</html>
