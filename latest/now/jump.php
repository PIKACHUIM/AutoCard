<?php
    require_once('../checker.php');
    checkcode($_POST['token'])
?>
<?php
    $scu_uid = $_POST['user'];
?>
<!DOCTYPE html>
<html lang="en" >
<head>
    <meta name="viewport" content="width=device-width,initial-scale=1.0, minimum-scale=1.0 maximum-scale=1.0, user-scalable=no"/>
    <meta charset="UTF-8">
    <title>正在打卡</title>
    <script type="text/javascript" src="./modernizr.js" ></script>
    <link rel="stylesheet" href="./normalize.css">
    <link rel="stylesheet" href="./style.css">
    <meta http-equiv="refresh" content="2;url=exec.php?user=<?php echo $scu_uid; ?>">
</head>
<body>
    <h1>正在执行打卡操作</h1>
    <div class='loader loader3'>
      <div>
        <div>
          <div>
            <div>
              <div>
                <div></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
</body>
</html>
