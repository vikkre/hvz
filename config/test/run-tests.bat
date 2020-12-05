@setlocal
@echo off
pushd %~dp0
:: api tests
docker-compose  ^
        -f .\api.docker-compose.yml ^
        up --build --abort-on-container-exit --exit-code-from test_api
set api_test_exit_code=%errorlevel%
:: frontend tests
docker-compose  ^
        -f .\..\..\docker-compose.yml ^
        -f .\..\e2etests\docker-compose.yml ^
        up --build --abort-on-container-exit --exit-code-from e2etests
set e2e_test_exit_code=%errorlevel%

set /a exit_code=%api_test_exit_code% + %e2e_test_exit_code% 

exit /b %exit_code%