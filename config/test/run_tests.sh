#!/bin/bash

current_path=$(pwd)

parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"

docker-compose -f api.docker-compose.yml up --build --exit-code-from test_api --abort-on-container-exit
if [ $? -eq 0 ];
then
	echo "API test was successful."
else
	echo "API test failed."
	exit 1
fi

echo "Here be Frontend test"
# docker-compose -f frontend.docker-compose.yml up --build --exit-code-from test_e2etests --abort-on-container-exit
if [ $? -eq 0 ];
then
	echo "Frontend test was successful."
else
	echo "Frontend test failed."
	exit 1
fi

cd "$current_path"
