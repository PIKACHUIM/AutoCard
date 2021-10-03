<html>
    <title>打卡结果</title>
    <meta name="viewport" content="width=device-width,initial-scale=1.0, minimum-scale=1.0 maximum-scale=1.0, user-scalable=no"/>
    <link rel="stylesheet" href="../css/style.css">
    <style>
    body{
         font-family: 'simsun';
         font-size: 0.7em;
    }
    </style>
    <body>
        ------------------------------执行结果-------------------------------<br/>
        ------------------OCR模块载入结果:
    </body>
</html>
<?PHP
$scu_uid = $_GET['user'];
if(preg_match("/^\d{13}$/",$scu_uid)){
    $outputs = exec('export PYTHONIOENCODING=utf-8 && path=$(pwd) && export PATH=/home/scurm/miniconda3/envs/card/bin:$PATH && cd /www/wwwroot/card.geekbang.cf/ && python server.py stid'.$scu_uid.' >now/logs.log');
    $logfile = fopen("logs.log", "r") or die("无法获取日志信息");
    $logtext = fread($logfile,filesize("logs.log"));
    echo str_replace("\n","<br/>",$logtext);
    fclose($logfile);
    echo $outputs;
    echo "<br />";
    echo "<a href=\"../index.php\"><button style=\"width:100%;max-width:540px\" >返回</button></a>";
}
else {
    echo $scu_uid;
    echo "<script>alert('学号无效或非法请求')</script>";
    echo "<script>window.location.href=\"http://card.52pika.cn/\"</script>";
}
?> 