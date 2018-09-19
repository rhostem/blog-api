USER=ubuntu
DEST=/home/ubuntu/www/blogapi
HOST=52.78.50.81

rsync -arv -progress --delete -e "ssh -i ~/.ssh/lightsail_private.pem" --exclude-from './.rsyncignore' ./ $USER@$HOST:$DEST

# 앱 시작
ssh -i ~/.ssh/lightsail_private.pem $USER@$HOST "cd $DEST && sudo service blogapi restart"