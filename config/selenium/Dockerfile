FROM selenium/standalone-firefox

WORKDIR /code

RUN sudo apt-get update
RUN sudo apt-get install -y python3 python3-pip 
RUN pip3 install selenium
RUN pip3 install pytest
RUN pip3 install pytest-selenium


CMD ["/bin/bash"]