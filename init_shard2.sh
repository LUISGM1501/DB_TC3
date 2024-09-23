#!/bin/bash

# Configurar el Replica Set para Shard 2
docker exec -it mongors2n1 mongosh --eval '
rs.initiate({
  _id: "mongors2",
  members: [
    { _id: 0, host: "mongors2n1:27017" },
    { _id: 1, host: "mongors2n2:27017" },
    { _id: 2, host: "mongors2n3:27017" }
  ]
});
'
