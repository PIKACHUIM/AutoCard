<?php


/*----------------------执行指定的命令----------------------
		用法：db_exec("插入语句")
		返回：bool-true：成功
----------------------------------------------------------*/
function db_exec($db_exec_comm){
          $db_exec_path = dirname(dirname(__FILE__));
  $db_json_file = file_get_contents('../config.json');
  $db_json_data = json_decode($db_json_file,true);
  $db_exec_conn = mysqli_connect( 
  $db_json_data['db_host'],$db_json_data['db_user'],$db_json_data['db_pass'],$db_json_data['db_name']);
  $db_exec_data = $db_exec_conn->query($db_exec_comm);
  if($db_conf_dbug == true and $db_exec_conn ->error!="")
    echo   "\n[数据库错误]".$db_exec_conn ->error."\n";
         $db_exec_conn ->close();
  return $db_exec_data;
}

/*---------------------更新特定表特定值---------------------
		用法：db_putc(参数列表)
		参数：$db_put_form  //数据表名
              $db_put_name  //查找项名
              $db_put_item  //查找内容
              $db_put_toch  //修改项名
              $db_put_data  //修改内容
		返回：bool-true：成功
----------------------------------------------------------*/
function db_putc($db_putc_form,  //数据表名
                 $db_putc_name,  //查找项名
                 $db_putc_item,  //查找内容
                 $db_putc_toch,  //修改项名
                 $db_putc_data){ //修改内容
          $db_putc_path = dirname(dirname(__FILE__));
          $db_putc_temp="UPDATE "
                       .$db_putc_form
                       ." SET "
                       .$db_putc_toch
                       ."="
                       .$db_putc_data
                       ." WHERE "
                       .$db_putc_name
                       ."="
                       ."\""
                       .$db_putc_item
                       ."\"";
  if($db_conf_dbug == true)
    echo "\n[数据库调试]".$db_putc_temp."\n";
  db_exec($db_putc_temp);
  return true;
}


/*-----------------------查找数据库内容---------------------
		用法：db_getc('数据表名')
		返回：查找的数据内容
------------------------------------------------------------*/
function db_getc($db_getc_form,  //数据表名
                 $db_getc_name,  //查找项名
                 $db_getc_item,  //查找内容
                 $db_getc_dtnm){ //返回类目
            $db_getc_path = dirname(dirname(__FILE__));
    $db_getc_sqlu = 'SELECT * FROM '
                    .$db_getc_form
                    ." WHERE "
                    .$db_getc_name
                    ."="
                    ."\""
                    .$db_getc_item
                    ."\""
                    ;
    if($db_conf_dbug == true and $db_conf_getc==true)
        echo "\n[数据库调试]".$db_getc_sqlu."\n";
    $db_getc_data = db_exec($db_getc_sqlu);
            $db_getc_rows = $db_getc_data ->fetch_assoc();
    return  $db_getc_rows[$db_getc_dtnm];
}


/*-----------------------删除数据库内容---------------------
		用法：db_delc('数据表名')
		返回：查找的数据内容
------------------------------------------------------------*/
function db_delc($db_getc_form,  //数据表名
                 $db_getc_name,  //删除项名
                 $db_getc_item   //删除内容
                 ){
            $db_getc_path = dirname(dirname(__FILE__));
    include $db_getc_path.'/config/db.php';
    $db_getc_sqlu = 'DELETE FROM '
                    .$db_getc_form
                    ." WHERE "
                    .$db_getc_name
                    ."="
                    ."\""
                    .$db_getc_item
                    ."\""
                    ;
    $db_getc_data = db_exec($db_getc_sqlu);
    if($db_conf_dbug == true)
        echo "\n[数据库调试]".$db_getc_sqlu."\n";
    return  $db_getc_data;
}


/*-----------------------查找整个数据表---------------------
		用法：db_alls('数据表名')
		返回：整张表内容db->form
------------------------------------------------------------*/
function db_alls($db_alls_from){
    $db_alls_path = dirname(dirname(__FILE__));
    $db_alls_sqlu = 'SELECT * FROM '.$db_alls_from;
    return db_exec($db_alls_sqlu);
}

function db_alld($db_alls_from,$db_alls_item){
    $db_retu = array();
    $db_temp = db_alls($db_alls_from);
    while($db_rows=$db_temp->fetch_assoc())
        array_push($db_retu,$db_rows[$db_alls_item]);
    return $db_retu;
}

?>