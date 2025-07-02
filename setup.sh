#!/bin/bash
    echo "START: Building uncover"
    apt update
    apt install -y build-essential ca-certificates wget unzip git
    apt install -y python3 python3-pip python-is-python3
    wget https://go.dev/dl/go1.21.6.linux-amd64.tar.gz && tar -C /usr/local -xzf go1.21.6.linux-amd64.tar.gz && rm go1.21.6.linux-amd64.tar.gz
    export GOROOT=/usr/local/go
    export GOPATH=/go
    export PATH=$GOPATH/bin:$GOROOT/bin:$PATH
    export GO111MODULE=on
    export CGO_ENABLED=1
    export SHODAN_API_KEY=1WSR9UcKwjrD2ReQtGhVrGbFqVtyVnL4
    mkdir -p /go/src
    mkdir -p /go/bin
    go install -v github.com/projectdiscovery/uncover/cmd/uncover@latest
    echo "END: Building uncover"