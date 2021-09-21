UPDATE pc_user SET succ=(SELECT COUNT(*) FROM pc_logs WHERE flag='打卡成功' AND pc_user.user=user)
UPDATE pc_user SET fail=(SELECT COUNT(*) FROM pc_logs WHERE flag!='打卡成功' AND pc_user.user=user)