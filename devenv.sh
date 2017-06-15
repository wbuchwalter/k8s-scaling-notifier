#!/bin/bash
docker run -it -v /Users/Will/.kube/config:/root/.kube/config -v ${PWD}:/app watcher /bin/bash