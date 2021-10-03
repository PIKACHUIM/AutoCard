<?php

    function checkcode($token){
    echo "<html><head><title>皮卡丘自动打卡系统</title></head></html>";
    include 'code/CaptchaClient.php';
    $appId = "b4f11125fb26b4fd3010ba2146cf36a7";
    $appMd = "857c0a73e4cd74993102e79a2323a884";
    $client = new CaptchaClient($appId,$appMd);
    $client->setTimeOut(2);
    $vertoken = $token;
    $response = $client->verifyToken($vertoken);
        if(!$response->result){
            echo "<script>alert('请先完成验证');</script>";
            echo "<script>history.back(-1);</script>";
        }
        else return true;
    }


?>