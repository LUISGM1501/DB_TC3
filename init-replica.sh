#!/bin/bash

# Inicializar réplicas en los shards
mongosh --eval 'rs.initiate({_id: "mongors1", members: [{_id: 0, host: "mongors1n1:27017"}, {_id: 1, host: "mongors1n2:27017"}, {_id: 2, host: "mongors1n3:27017"}]})'

mongosh --eval 'rs.initiate({_id: "mongors2", members: [{_id: 0, host: "mongors2n1:27017"}, {_id: 1, host: "mongors2n2:27017"}, {_id: 2, host: "mongors2n3:27017"}]})'

mongosh --eval 'rs.initiate({_id: "mongors3", members: [{_id: 0, host: "mongors3n1:27017"}, {_id: 1, host: "mongors3n2:27017"}, {_id: 2, host: "mongors3n3:27017"}]})'

# Inicializar los config servers
mongosh --eval 'rs.initiate({_id: "mongocfg", configsvr: true, members: [{_id: 0, host: "mongocfg1:27017"}, {_id: 1, host: "mongocfg2:27017"}, {_id: 2, host: "mongocfg3:27017"}]})'
