@echo off
title GestaoFarma - Database Explorer
setlocal

:: %~dp0 garante portabilidade absoluta entre seus 4 ambientes
set "ROOT_DIR=%~dp0"
set "EXE=%ROOT_DIR%data\sqlite-page-explorer.exe.com"
set "DB=%ROOT_DIR%data\farmacia.db"

if not exist "%EXE%" (echo [ERRO] Binario ausente: %EXE% & pause & exit /b)
if not exist "%DB%" (echo [ERRO] Banco ausente: %DB% & pause & exit /b)

:: O comando 'start' garante a abertura no Windows, enquanto '-B' impede a segunda aba
start "" "http://127.0.0.1:8080"

echo [SERVER] Servidor ativo na porta 8080. Pressione CTRL+C para encerrar.
"%EXE%" -p 8080 -B "%DB%"

endlocal