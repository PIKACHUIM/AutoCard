<html>
    <head>
        <title>SCU自动打卡系统</title>
        <meta name="viewport" content="width=device-width,initial-scale=1.82, minimum-scale=1.82 maximum-scale=1.82, user-scalable=no"/>
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
        <h2>SCU自动打卡系统</h2>
        <div style="width:52%">
            <h3 align=center>
            使用说明
            </h3>
            <div style="font-size:10px" align=center>
                本系统每天上午9点(CST)自动打卡
                <br />
                失败会发送邮件
                <br />
                使用上一次的地点上报
                <br />
                不收集你的隐私
                <br />
                如果需要手动打卡
                <br />
                请在九点以前或者提前撤销打卡
                <br />
            </div>
        </div>
        <br />
        <button type="button" style="width:50%;background-color: #1E90FF;" onclick="window.location.href='add.php'">添加打卡账号</button>
        <div style="width:52%">
            <div style="font-size:10px" align=center>
                <br />
                如果需要停止自动打卡
                <br />
                请点击下方按钮
                <br />
            </div>
        </div>
        <br />
        <button type="button" style="width:50%;background-color: #FF3030;" onclick="window.location.href='del.php'">撤销自动打卡</button>
    </body>
</html>
