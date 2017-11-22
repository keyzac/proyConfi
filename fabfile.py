__author__ = 'shinobu'
from fabric.api import *
from fabric.colors import green

env.user = 'root'
env.host_string = '104.236.217.40'
env.password = 'soft5250684'
home_path = "/root/"
settings_staging = "--settings='corebackend.settings.staging'"
activate_env_staging = "source {}/myvenv/bin/activate".format(home_path)
manage = "python manage.py"


def deploy_staging():
    print("Beginning Deploy:")
    with cd("{}/proyConfi".format(home_path)):
        run("git pull")
        run("{} && pip install -r requeriments.txt".format(activate_env_staging))
        run("{} && {} collectstatic --noinput {}".format(activate_env_staging, manage,
                                                         settings_staging))
        run("{} && {} migrate {}".format(activate_env_staging, manage, settings_staging))
        sudo("service nginx restart", pty=False)
        sudo("supervisorctl restart gunicorn", pty=False)
    print(green("Deploy conegp successful"))


def createsuperuser_staging():
    with cd("{}/conegp".format(home_path)):
        run("{} && {} createsuperuser {}".format(activate_env_staging, manage,
                                                 settings_staging))
    print(green("Createsuperuser successful"))




