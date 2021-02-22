@echo off
color 3f
title Git工具
mode con lines=30 cols=60
:LABEL_MENU
color 3f
echo.
echo.
echo             ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
echo             ▇                                ▇
echo             ▇      ***皮卡丘Git工具***       ▇
echo             ▇                                ▇
echo             ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
echo.
echo ------------------------------------------------------------
echo.
echo			  1.初始化用户定义数据
echo.
echo			  2.从远程分支更新文件
echo.
echo			  3.同步本地更改到远程
echo.
echo			  4.强制放弃本地的更改（危险）
echo.
echo			  5.强制用本地版本覆盖（危险）
echo.
echo			  6.强制只保留最新版本（危险）
echo.
echo			  7.查看并修改版本分支
echo.
echo			  q.放弃修改并退出工具
echo.
echo ------------------------------------------------------------
echo.
set /p sel=请输入选项前面的序号:
cls
if %sel%==0 (
  exit
) else if %sel%==1 (
  goto LABEL_1
) else if %sel%==2 (
  goto LABEL_2
) else if %sel%==3 (
  goto LABEL_3
) else if %sel%==4 (
  goto LABEL_4
) else if %sel%==5 (
  goto LABEL_5
) else if %sel%==6 (
  goto LABEL_6
) else if %sel%==7 (
  goto LABEL_7
) else if %sel%==q (
  exit
) else if %sel%==exit (
  exit
) else if %sel%==rnew (
  %0
) else if %sel%==edit (
  start notepad2 %0
  goto LABEL_MENU
)else (
  echo 输入命令不正确，请重新输入！
  timeout /t 1 >nul
  goto LABEL_MENU
)
REM ###############################################################
:LABEL_1
cls
color 8f
echo.
echo.
echo             ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
echo             ▇                                ▇
echo             ▇      ***输入你的信息***        ▇
echo             ▇                                ▇
echo             ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
echo.
echo ------------------------------------------------------------
echo.
set /p yxh=请输入邮箱:
git config --global user.email %yxh%
echo.
set /p yhm=请输入姓名:
git config --global user.name  %yhm%
timeout /t 2  >nul
goto LABEL_SUCC
REM ###############################################################



REM ###############################################################
:LABEL_2
color af
cls
echo.
echo.
echo             ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
echo             ▇                                ▇
echo             ▇       ***正在下载数据***       ▇
echo             ▇                                ▇
echo             ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
git pull || git checkout
timeout /t 5
goto LABEL_SUCC
REM ###############################################################



REM ###############################################################
:LABEL_3
cls
color af
echo.
echo.
echo             ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
echo             ▇                                ▇
echo             ▇       ***正在上传数据***       ▇
echo             ▇                                ▇
echo             ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
git add .
git commit -m "Updated"%date:~0,4%%date:~5,2%%date:~8,2%%time:~0,2%%time:~3,2%%time:~6,2%
git push
goto LABEL_SUCC
REM ###############################################################



REM ###############################################################
:LABEL_4
cls
color cf
echo.
echo.
echo.
echo             ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
echo             ▇                                ▇
echo             ▇       ***准备覆盖本地***       ▇
echo             ▇                                ▇
echo             ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
set Vbscript=Msgbox("你确定要放弃本地更改吗？所有本地修改都将丢失！！！",1,"数据安全确认")
for /f "Delims=" %%a in ('MsHta VBScript:Execute("CreateObject(""Scripting.Filesystemobject"").GetStandardStream(1).Write(%Vbscript:"=""%)"^)(Close^)') do Set "MsHtaReturnValue=%%a"
set ReturnValue1=确定
set ReturnValue2=取消
if %MsHtaReturnValue% == 1 (
    echo.
    echo.
    echo -------------------丢弃本地数据，强制同步-------------------
    timeout /t 1 >nul
    cls
    color f4
    echo.
    echo.
    echo.
    echo             ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
    echo             ▇                                ▇
    echo             ▇       ***用户丢弃数据***       ▇
    echo             ▇                                ▇
    echo             ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
    echo.
    echo.
    echo --------------五秒后自动开始，取消请右上角关闭--------------
    echo.
    echo.
    timeout /t 5
    echo.
    echo.
    cls
    git fetch --all
    git reset --hard origin/master
    git pull
    timeout /t 2 >nul
    goto LABEL_SUCC
) else (
    cls
    color 4f
    echo.
    echo.
    echo.
    echo             ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
    echo             ▇                                ▇
    echo             ▇       ***用户放弃同步***       ▇
    echo             ▇                                ▇
    echo             ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
    echo.
    echo.
    echo -------------------用户放弃同步，同步中止-------------------
    timeout /t 3  >nul
    goto LABEL_SUCC
)
goto LABEL_SUCC
REM ###############################################################



REM ###############################################################
:LABEL_5
cls
color cf
echo.
echo.
echo.
echo             ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
echo             ▇                                ▇
echo             ▇       ***强制覆盖远程***       ▇
echo             ▇                                ▇
echo             ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
set Vbscript=Msgbox("你确定要覆盖远程更改吗？别人之前的修改都将永久丢失！！！",1,"数据安全确认")
for /f "Delims=" %%a in ('MsHta VBScript:Execute("CreateObject(""Scripting.Filesystemobject"").GetStandardStream(1).Write(%Vbscript:"=""%)"^)(Close^)') do Set "MsHtaReturnValue=%%a"
set ReturnValue1=确定
set ReturnValue2=取消
if %MsHtaReturnValue% == 1 (
    echo.
    echo.
    echo -------------------丢弃本地数据，强制同步-------------------
    timeout /t 1 >nul
    cls
    color f4
    echo.
    echo.
    echo.
    echo             ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
    echo             ▇                                ▇
    echo             ▇       ***准备覆盖数据***       ▇
    echo             ▇                                ▇
    echo             ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
    echo.
    echo.
    echo --------------五秒后自动开始，取消请右上角关闭--------------
    echo.
    echo.
    timeout /t 5
    echo.
    echo.
    cls
    color 4f
    echo.
    echo.
    echo             ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
    echo             ▇                                ▇
    echo             ▇       ***正在覆盖数据***       ▇
    echo             ▇                                ▇
    echo             ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
    git add .
    git commit -m "Updated"%date:~0,4%%date:~5,2%%date:~8,2%%time:~0,2%%time:~3,2%%time:~6,2%
    git push -f
    timeout /t 2 >nul
    goto LABEL_SUCC
) else (
    cls
    color 4f
    echo.
    echo.
    echo.
    echo             ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
    echo             ▇                                ▇
    echo             ▇       ***用户放弃同步***       ▇
    echo             ▇                                ▇
    echo             ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
    echo.
    echo.
    echo -------------------用户放弃同步，同步中止-------------------
    timeout /t 3  >nul
    goto LABEL_SUCC
)
goto LABEL_SUCC
REM ###############################################################



REM ###############################################################
:LABEL_6
cls
color cf
echo.
echo.
echo.
echo             ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
echo             ▇                                ▇
echo             ▇       ***丢弃历史版本***       ▇
echo             ▇                                ▇
echo             ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
set Vbscript=Msgbox("你确定要丢弃历史版本吗？之前的记录修改都将永久丢失！！！",1,"数据安全确认")
for /f "Delims=" %%a in ('MsHta VBScript:Execute("CreateObject(""Scripting.Filesystemobject"").GetStandardStream(1).Write(%Vbscript:"=""%)"^)(Close^)') do Set "MsHtaReturnValue=%%a"
set ReturnValue1=确定
set ReturnValue2=取消
if %MsHtaReturnValue% == 1 (
    echo.
    echo.
    echo -------------------丢弃本地数据，强制同步-------------------
    timeout /t 1 >nul
    cls
    color f4
    echo.
    echo.
    echo.
    echo             ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
    echo             ▇                                ▇
    echo             ▇       ***准备丢弃版本***       ▇
    echo             ▇                                ▇
    echo             ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
    echo.
    set /p fzh=请输入放弃修改分支（默认master）:
    if not defined fzh (
      set fzh=master
      echo 默认舍弃master分支的历史记录！！！
    ) else (
      echo 将要舍弃%fzh%分支的历史记录！！！
    )
    echo.
    echo --------------五秒后自动开始，取消请右上角关闭--------------
    echo.
    echo.
    timeout /t 5
    echo.
    echo.
    cls
    color 4f
    echo.
    echo.
    echo             ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
    echo             ▇                                ▇
    echo             ▇       ***正在丢弃版本***       ▇
    echo             ▇                                ▇
    echo             ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
    git add .
    git commit -m "Updated"%date:~0,4%%date:~5,2%%date:~8,2%%time:~0,2%%time:~3,2%%time:~6,2%
    git push -f
    goto LABEL_SUCC
) else (
    cls
    color 4f
    echo.
    echo.
    echo.
    echo             ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
    echo             ▇                                ▇
    echo             ▇       ***用户放弃丢弃***       ▇
    echo             ▇                                ▇
    echo             ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
    echo.
    echo.
    echo -------------------用户放弃丢弃，同步中止-------------------
    timeout /t 3  >nul
    goto LABEL_SUCC
)
goto LABEL_SUCC
REM ###############################################################


REM ###############################################################
:LABEL_7
cls
color cf
echo.
echo.
echo.
echo             ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
echo             ▇                                ▇
echo             ▇       ***切换版本分支***       ▇
echo             ▇                                ▇
echo             ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
echo.
echo ---------------------------全部分支-------------------------
git branch
color cf
echo ------------------------------------------------------------
echo.
set /p mbh=请输入切换的分支名称：
echo.
echo 即将切换到%mbh%，五秒后开始执行......
timeout /t 5  >nul
git checkout %mbh%
timeout /t 3  >nul
goto LABEL_SUCC
REM ###############################################################


REM ###############################################################
:LABEL_SUCC
cls
color 2f
echo.
echo.
echo             ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
echo             ▇                                ▇
echo             ▇       ***操作成功执行***       ▇
echo             ▇                                ▇
echo             ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
echo.
echo.
echo.
echo.
echo.
echo.
echo.
echo.
echo.
echo.
echo.
echo.
echo.
echo.
echo.
echo.
echo.
echo.
timeout /t 3  >nul
goto LABEL_MENU
REM ###############################################################