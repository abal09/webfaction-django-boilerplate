"""Fabfile for the ``webfaction-django-boilerplate``.

Make sure to setup your ``fabric_settings.py`` first. As a start, just copy
``fabric_settings.py.sample``.

"""
from __future__ import with_statement

from fabric.api import (
    cd,
    env,
    lcd,
    local,
    run,
    settings,
)

import fabric_settings as fab_settings


env.hosts = fab_settings.ENV_HOSTS
env.user = fab_settings.ENV_USER


BASHRC_SETTING1 = 'export VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python2.7'
BASHRC_SETTING2 = 'export WORKON_HOME=$HOME/Envs'
BASHRC_SETTING3 = 'source /home/{0}/bin/virtualenvwrapper.sh'.format(env.user)
BASHRC_SETTING4 = 'export PIP_VIRTUALENV_BASE=$WORKON_HOME'
BASHRC_SETTING5 = 'export PIP_RESPECT_VIRTUALENV=true'


def _insert_string_into_file(search_string, file_):
    """Searches for a string in a file. Inserts string if not found."""
    with settings(warn_only=True):
        result = run("grep '{0}' {1}".format(search_string, file_))
        if result.failed:
            run("echo '{0}' >> {1}".format(search_string, file_))


def add_bashrc_settings():
    with cd('$HOME'):
        with settings(warn_only=True):
            _insert_string_into_file(BASHRC_SETTING1, '.bashrc')
            _insert_string_into_file(BASHRC_SETTING2, '.bashrc')
            _insert_string_into_file(BASHRC_SETTING3, '.bashrc')
            _insert_string_into_file(BASHRC_SETTING4, '.bashrc')
            _insert_string_into_file(BASHRC_SETTING5, '.bashrc')


def create_git_repo():
    with cd('$HOME/webapps/git'):
        run('git init --bare ./repos/{0}'.format(fab_settings.GIT_REPO_NAME))
    with cd('$HOME/webapps/git/repos/{0}'.format(fab_settings.GIT_REPO_NAME)):
        run('git config http.receivepack true')


def create_ssh_dir():
    with cd('$HOME'):
        with settings(warn_only=True):
            run('mkdir .ssh')
            run('touch .ssh/authorized_keys')
            run('chmod 600 .ssh/authorized_keys')
            run('chmod 700 .ssh')


def create_virtualenv():
    with cd('$HOME'):
        run('mkvirtualenv -p python2.7 {0}'.format(fab_settings.VENV_NAME))


def install_virtualenv():
    with cd('$HOME'):
        run('mkdir -p $HOME/lin/python2.7')
        run('easy_install-2.7 virtualenv')
        run('easy_install-2.7 pip')
        run('pip install virtualenvwrapper')
        run('mkdir -p $HOME/Envs')


def install_server():
    install_virtualenv()
    add_bashrc_settings()
    create_virtualenv()
    create_git_repo()


def install_local_repo():
    with lcd(fab_settings.PROJECT_ROOT):
        local('rm -rf .git')
        local('rm .gitmodules')
        local('rm -rf website/webapps/django/project/submodules/Skeleton')
        local('git init')
        local('git submodule add git://github.com/dhgamache/Skeleton.git website/webapps/django/project/submodules/Skeleton')
    with lcd(fab_settings.DJANGO_PROJECT_ROOT):
        local('cp settings/local/local_settings.py.sample settings/local/local_settings.py')
        local('cp settings/local/gorun_settings.py.sample gorun_settings.py')
        local('python manage.py syncdb --all --noinput')
        local('python manage.py migrate --fake')
        local('python manage.py loaddata bootstrap_auth.json')
    with lcd(fab_settings.PROJECT_ROOT):
        local('git add .')
        local('git commit -am "Initial commit."')
