#!/bin/bash

docker build -t akira-server .
docker run -p 8080:8080 akira-server