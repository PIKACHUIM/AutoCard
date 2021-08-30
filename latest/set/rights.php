<?php
	include '../mod/db.php';
	echo "--------------开始执行数据修复操作--------------\n;
	";
    $save_sql = "UPDATE pcard.pc_user SET succ=(SELECT COUNT(*) FROM pc_logs WHERE flag='打卡成功' AND pc_user.user=user)";
    echo db_exec($save_sql);
    $save_sql = "UPDATE pcard.pc_user SET fail=(SELECT COUNT(*) FROM pc_logs WHERE flag!='打卡成功' AND pc_user.user=user)";
	echo db_exec($save_sql);
	echo "--------------执行数据修复操作成功--------------\n";
?>