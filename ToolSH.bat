@echo off
color 3f
title Git����
mode con lines=30 cols=60
:LABEL_MENU
color 3f
echo.
echo.
echo             �~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~
echo             �~                                �~
echo             �~      ***Ƥ����Git����***       �~
echo             �~                                �~
echo             �~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~
echo.
echo ------------------------------------------------------------
echo.
echo			  1.��ʼ���û���������
echo.
echo			  2.��Զ�̷�֧�����ļ�
echo.
echo			  3.ͬ�����ظ��ĵ�Զ��
echo.
echo			  4.ǿ�Ʒ������صĸ��ģ�Σ�գ�
echo.
echo			  5.ǿ���ñ��ذ汾���ǣ�Σ�գ�
echo.
echo			  6.ǿ��ֻ�������°汾��Σ�գ�
echo.
echo			  7.�鿴���޸İ汾��֧
echo.
echo			  q.�����޸Ĳ��˳�����
echo.
echo ------------------------------------------------------------
echo.
set /p sel=������ѡ��ǰ������:
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
  echo ���������ȷ�����������룡
  timeout /t 1 >nul
  goto LABEL_MENU
)
REM ###############################################################
:LABEL_1
cls
color 8f
echo.
echo.
echo             �~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~
echo             �~                                �~
echo             �~      ***���������Ϣ***        �~
echo             �~                                �~
echo             �~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~
echo.
echo ------------------------------------------------------------
echo.
set /p yxh=����������:
git config --global user.email %yxh%
echo.
set /p yhm=����������:
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
echo             �~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~
echo             �~                                �~
echo             �~       ***������������***       �~
echo             �~                                �~
echo             �~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~
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
echo             �~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~
echo             �~                                �~
echo             �~       ***�����ϴ�����***       �~
echo             �~                                �~
echo             �~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~
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
echo             �~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~
echo             �~                                �~
echo             �~       ***׼�����Ǳ���***       �~
echo             �~                                �~
echo             �~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~
set Vbscript=Msgbox("��ȷ��Ҫ�������ظ��������б����޸Ķ�����ʧ������",1,"���ݰ�ȫȷ��")
for /f "Delims=" %%a in ('MsHta VBScript:Execute("CreateObject(""Scripting.Filesystemobject"").GetStandardStream(1).Write(%Vbscript:"=""%)"^)(Close^)') do Set "MsHtaReturnValue=%%a"
set ReturnValue1=ȷ��
set ReturnValue2=ȡ��
if %MsHtaReturnValue% == 1 (
    echo.
    echo.
    echo -------------------�����������ݣ�ǿ��ͬ��-------------------
    timeout /t 1 >nul
    cls
    color f4
    echo.
    echo.
    echo.
    echo             �~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~
    echo             �~                                �~
    echo             �~       ***�û���������***       �~
    echo             �~                                �~
    echo             �~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~
    echo.
    echo.
    echo --------------������Զ���ʼ��ȡ�������Ͻǹر�--------------
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
    echo             �~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~
    echo             �~                                �~
    echo             �~       ***�û�����ͬ��***       �~
    echo             �~                                �~
    echo             �~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~
    echo.
    echo.
    echo -------------------�û�����ͬ����ͬ����ֹ-------------------
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
echo             �~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~
echo             �~                                �~
echo             �~       ***ǿ�Ƹ���Զ��***       �~
echo             �~                                �~
echo             �~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~
set Vbscript=Msgbox("��ȷ��Ҫ����Զ�̸����𣿱���֮ǰ���޸Ķ������ö�ʧ������",1,"���ݰ�ȫȷ��")
for /f "Delims=" %%a in ('MsHta VBScript:Execute("CreateObject(""Scripting.Filesystemobject"").GetStandardStream(1).Write(%Vbscript:"=""%)"^)(Close^)') do Set "MsHtaReturnValue=%%a"
set ReturnValue1=ȷ��
set ReturnValue2=ȡ��
if %MsHtaReturnValue% == 1 (
    echo.
    echo.
    echo -------------------�����������ݣ�ǿ��ͬ��-------------------
    timeout /t 1 >nul
    cls
    color f4
    echo.
    echo.
    echo.
    echo             �~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~
    echo             �~                                �~
    echo             �~       ***׼����������***       �~
    echo             �~                                �~
    echo             �~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~
    echo.
    echo.
    echo --------------������Զ���ʼ��ȡ�������Ͻǹر�--------------
    echo.
    echo.
    timeout /t 5
    echo.
    echo.
    cls
    color 4f
    echo.
    echo.
    echo             �~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~
    echo             �~                                �~
    echo             �~       ***���ڸ�������***       �~
    echo             �~                                �~
    echo             �~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~
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
    echo             �~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~
    echo             �~                                �~
    echo             �~       ***�û�����ͬ��***       �~
    echo             �~                                �~
    echo             �~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~
    echo.
    echo.
    echo -------------------�û�����ͬ����ͬ����ֹ-------------------
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
echo             �~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~
echo             �~                                �~
echo             �~       ***������ʷ�汾***       �~
echo             �~                                �~
echo             �~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~
set Vbscript=Msgbox("��ȷ��Ҫ������ʷ�汾��֮ǰ�ļ�¼�޸Ķ������ö�ʧ������",1,"���ݰ�ȫȷ��")
for /f "Delims=" %%a in ('MsHta VBScript:Execute("CreateObject(""Scripting.Filesystemobject"").GetStandardStream(1).Write(%Vbscript:"=""%)"^)(Close^)') do Set "MsHtaReturnValue=%%a"
set ReturnValue1=ȷ��
set ReturnValue2=ȡ��
if %MsHtaReturnValue% == 1 (
    echo.
    echo.
    echo -------------------�����������ݣ�ǿ��ͬ��-------------------
    timeout /t 1 >nul
    cls
    color f4
    echo.
    echo.
    echo.
    echo             �~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~
    echo             �~                                �~
    echo             �~       ***׼�������汾***       �~
    echo             �~                                �~
    echo             �~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~
    echo.
    set /p fzh=����������޸ķ�֧��Ĭ��master��:
    if not defined fzh (
      set fzh=master
      echo Ĭ������master��֧����ʷ��¼������
    ) else (
      echo ��Ҫ����%fzh%��֧����ʷ��¼������
    )
    echo.
    echo --------------������Զ���ʼ��ȡ�������Ͻǹر�--------------
    echo.
    echo.
    timeout /t 5
    echo.
    echo.
    cls
    color 4f
    echo.
    echo.
    echo             �~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~
    echo             �~                                �~
    echo             �~       ***���ڶ����汾***       �~
    echo             �~                                �~
    echo             �~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~
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
    echo             �~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~
    echo             �~                                �~
    echo             �~       ***�û���������***       �~
    echo             �~                                �~
    echo             �~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~
    echo.
    echo.
    echo -------------------�û�����������ͬ����ֹ-------------------
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
echo             �~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~
echo             �~                                �~
echo             �~       ***�л��汾��֧***       �~
echo             �~                                �~
echo             �~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~
echo.
echo ---------------------------ȫ����֧-------------------------
git branch
color cf
echo ------------------------------------------------------------
echo.
set /p mbh=�������л��ķ�֧���ƣ�
echo.
echo �����л���%mbh%�������ʼִ��......
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
echo             �~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~
echo             �~                                �~
echo             �~       ***�����ɹ�ִ��***       �~
echo             �~                                �~
echo             �~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~�~
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