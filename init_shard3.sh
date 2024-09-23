#!/bin/bash

# Configurar el Replica Set para Shard 3
docker exec -it mongors3n1 mongosh --eval '
rs.initiate({
  _id: "mongors3",
  members: [
    { _id: 0, host: "mongors3n1:27017" },
    { _id: 1, host: "mongors3n2:27017" },
    { _id: 2, host: "mongors3n3:27017" }
  ]
});
'
