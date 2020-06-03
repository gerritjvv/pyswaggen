#!/usr/bin/env bash

dir=$(cd -P -- "$(dirname -- "$0")" && pwd -P)

CMD=$1
shift

export PATH="$PATH:/usr/local/bin"

case $CMD in
 build)
   poetry build
   ;;
test )
   poetry run pytest tests "$@"
    ;;
 * )
   echo "<cmd> test"
  ;;
esac