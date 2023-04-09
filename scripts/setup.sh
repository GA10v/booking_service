#!/bin/bash
sleep 1

echo $'\n'SETUP.sh step 1 time now: `date +"%T" `
mongosh --host mongocfg1:27017 <<EOF
  var cfg = {
    "_id": "mongors1conf",
    "configsvr": true,
    "members": [
        {
            "_id": 0,
            "host": "mongocfg1"
        },
        {
            "_id": 1,
            "host": "mongocfg2"
        },
        {
            "_id": 2,
            "host": "mongocfg3"
        }
    ]
  };
  rs.initiate(cfg, { force: true });
  rs.reconfig(cfg, { force: true });
EOF

sleep 1
echo $'\n'SETUP.sh step 2 time now: `date +"%T" `

mongosh --host mongors1n1:27017 <<EOF
  var cfg = {
    "_id": "mongors1",
    "members": [
        {
            "_id": 0,
            "host": "mongors1n1"
        },
        {
            "_id": 1,
            "host": "mongors1n2"
        },
        {
            "_id": 2,
            "host": "mongors1n3"
        }
    ]
  }
  rs.initiate(cfg, { force: true });
  rs.reconfig(cfg, { force: true });
EOF

sleep 1
echo $'\n'SETUP.sh step 3 time now: `date +"%T" `

mongosh --host mongors2n1:27017 <<EOF
  var cfg = {
    "_id": "mongors2",
    "members": [
        {
            "_id": 0,
            "host": "mongors2n1"
        },
        {
            "_id": 1,
            "host": "mongors2n2"
        },
        {
            "_id": 2,
            "host": "mongors2n3"
        }
    ]
  }
  rs.initiate(cfg, { force: true });
  rs.reconfig(cfg, { force: true });
EOF

sleep 10
echo $'\n'SETUP.sh step 4 time now: `date +"%T" `

mongosh --host mongos1:27017 <<EOF
  var cfg = "mongors1/mongors1n1"
  sh.addShard(cfg, { force: true });
EOF

echo $'\n'SETUP.sh step 5 time now: `date +"%T" `

mongosh --host mongos1:27017 <<EOF
  var cfg = "mongors2/mongors2n1"
  sh.addShard(cfg, { force: true });
EOF

echo $'\n'SETUP.sh step 6 time now: `date +"%T" `
mongosh --host mongos1:27017 <<-EOSQL
  use $MONGODB_DB;
EOSQL
sleep 5
mongosh --host mongos1:27017 <<-EOSQL
  sh.enableSharding($MONGODB_DB)
EOSQL

echo $'\n'SETUP.sh step 7 time now: `date +"%T" `
mongosh --host mongos1:27017 <<-EOSQL
  use $MONGODB_DB;
  db.createCollection($MONGODB_REVIEW_COLLECTION)
  sh.shardCollection("$MONGODB_DB.$MONGODB_REVIEW_COLLECTION", {"guest_id": "hashed", "event_id": "hashed"})
EOSQL