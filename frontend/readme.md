# hvz - Frontend

## Technology
The frontend uses Vue version 2 and the css framework Bulma (v0.9). 
In addition the vue-select component is used.

parcel (v1.12) is used as a bundler (should be migrated to vue cli in the near future). The build output of the bundler is not commited to the repo, so a local build needs to be run. The output of the build (.dist) is mapped in the nginx configuration,.

You need to have node and npm installed on your host for this setup. And of course you should run `npm install` in the `frontend` directory.

E2E tests are written with python and pytest using the splinter library for interaction with the browser.

As the tests are manipulating the database directly using sqlalchemy core and as the tests are running on the host at the moment and not in a container, the postgres container needs to publish the port `5432` (standard postgres port).


## Dev & Test Notes
In order to develop on the frontend the `docker-compose.yml` file needs to be upped. At the moment this includes a container with a headless firefox browser which is used for the E2E tests. 

As already stated above the output of the bundler (directory `.dist`) is mapped in the nginx configuration. 

In order to start the build of the frontend you need to initiate the command 
```
cd frontend
npm run watch
```

After that the bundler will watch for changes and rebuild the frontend. This also enabled hot module reloading. 

The E2E tests are written in python 3.8. You should setup a virtual environment in the `frontend` directory. A `requirements.txt` file is located in this directory to help with the installation of the needed libraries in the virtual environment. 

To run the E2E tests you have to execute the following commands:
```
cd frontend
./venv/scripts/activate
pytest 
```

