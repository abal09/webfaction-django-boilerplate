#!/bin/bash
# if the first Argument is not set to 1, syncdb and migrate will be executed
source script_settings.sh
source $HOME/Envs/$VENV_NAME/bin/activate

cd $HOME/src/$PROJECTNAME
git pull
rsync -avz --stats --delete --exclude 'local_settings.py' ~/src/$PROJECTNAME/website/webapps/django/project ~/webapps/$DJANGO_APP_NAME/
cd ~/webapps/$DJANGO_APP_NAME/project
if [ $1 ]; then
	:
else
	python2.7 manage.py syncdb --migrate
    python2.7 manage.py collectstatic --noinput
    cd ~/webapps/$DJANGO_APP_NAME/apache2/bin
	./restart
fi
exit 0
