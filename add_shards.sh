#!/bin/bash

# Agregar shards al router (mongos)
mongosh --eval '
sh.addShard("mongors1/mongors1n1:27017,mongors1n2:27017,mongors1n3:27017");
sh.addShard("mongors2/mongors2n1:27017,mongors2n2:27017,mongors2n3:27017");
sh.addShard("mongors3/mongors3n1:27017,mongors3n2:27017,mongors3n3:27017");
'
