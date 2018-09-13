DEST=/home/ubuntu/www/blogapi
HOST=52.78.50.81

rsync -arv -progress --delete -e "ssh -i ~/.ssh/lightsail_private.pem" --exclude-from './.rsyncignore' ./ ubuntu@$HOST:$DEST
