#!/bin/bash
docker run -it -v $HOME/.kube/config:/root/.kube/config -v ${PWD}:/app wbuchwalter/k8s-scaling-notifier /bin/bash