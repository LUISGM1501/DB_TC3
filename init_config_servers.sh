#!/bin/bash

# Configurar el Replica Set para los Config Servers
docker exec -it mongocfg1 mongosh --eval '
rs.initiate({
  _id: "mongocfg",
  configsvr: true,
  members: [
    { _id: 0, host: "mongocfg1:27017" },
    { _id: 1, host: "mongocfg2:27017" },
    { _id: 2, host: "mongocfg3:27017" }
  ]
});
'
