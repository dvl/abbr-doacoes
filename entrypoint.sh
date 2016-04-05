#!/bin/bash

gid=$(stat --format %g /usr/src/app)
uid=$(stat --format %u /usr/src/app)

groupadd --gid $gid foo 2>/dev/null
useradd --gid $gid --uid $uid foo 2>/dev/null

./bin/gosu-amd64 $uid:$gid $*
