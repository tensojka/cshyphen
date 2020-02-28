#!/bin/sh

# generates src/cs-all-cstenten.wls from /tmp/cstenten.out (majka output) and src/ujc.wls


grep '^[$@]' /tmp/cstenten.out \
| sed -e 's/\t/\n/g' \
| sed -e '/[$@]/d' \
|sed -i 's/#subst.$//' \
| grep -xv '[0-9]*' > src/cs-all-cstenten.wls
make -s out/ujc.wls
cat out/ujc.wls >> src/cs-all-cstenten.wls
sort -u -o src/cs-all-cstenten.wls src/cs-all-cstenten.wls
sed -i 's/\#*//' src/cs-all-cstenten.wls
