# 验证打卡成功次数语句 -----------------------------------------------------------------------------
UPDATE pc_user SET succ=(SELECT COUNT(*) FROM pc_logs WHERE flag ='打卡成功' AND pc_user.user=user);
UPDATE pc_user SET fail=(SELECT COUNT(*) FROM pc_logs WHERE flag!='打卡成功' AND pc_user.user=user);
# 删除错误次数过多语句 -----------------------------------------------------------------------------
DELETE FROM pc_user WHERE succ=0 AND fail>0
# 删除没用的记录的语句 -----------------------------------------------------------------------------
DELETE FROM pc_logs WHERE NOT EXISTS(SELECT 1 FROM pc_user WHERE pc_user.user=pc_logs.user );
