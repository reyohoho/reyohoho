#!/usr/bin/sh
ps -ef | grep 'kinoserver:app' | awk '{print $2}'  | xargs -r kill -9
sudo /usr/bin/lsof -i -P |grep 5788| grep 'python3.1' | awk '{print $2}'| xargs -r kill -9
rm /home/bot/kino_server_int.log
rm /home/bot/kino_server.log
rm /home/bot/demo_cache.sqlite
echo -e 'AUTH PrE$$ton2334214@!\nflushall' | redis-cli
nohup /home/bot/.local/bin/sanic kinoserver:app -p 5788 -H 0.0.0.0 --workers=8 2>&1 >> kinoserver.log &