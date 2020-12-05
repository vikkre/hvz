#!/bin/bash

parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
pushd "$parent_path"

docker-compose -f api.docker-compose.yml up --build --exit-code-from test_api --abort-on-container-exit
if [ $? -eq 0 ];
then
	echo "API test was successful."
else
	echo "API test failed."
	popd
	exit 1
fi

docker-compose -f ../../docker-compose.yml -f ../e2etests/docker-compose.yml up --build --exit-code-from e2etests --abort-on-container-exit
if [ $? -eq 0 ];
then
	echo "Frontend test was successful."
else
	echo "Frontend test failed."
	popd
	exit 1
fi

echo "All tests ran successful"
popd
