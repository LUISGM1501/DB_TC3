#!/bin/bash

# Agregar los shards al router mongos
mongosh --eval 'sh.addShard("mongors1/mongors1n1:27017")'
mongosh --eval 'sh.addShard("mongors2/mongors2n1:27017")'
mongosh --eval 'sh.addShard("mongors3/mongors3n1:27017")'
