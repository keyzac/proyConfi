__author__ = 'shinobu'
from fabric.api import *
from fabric.colors import green

env.user = 'kevin'
env.host_string = '138.197.122.110'
env.password = 'contacto12345'
home_path = "/home/kevin"
settings_staging = "--settings='corebackend.settings.staging'"
activate_env_staging = "source {}/envs/conegpenv/bin/activate".format(home_path)
manage = "python manage.py"


def deploy_staging():
    print("Beginning Deploy:")
    with cd("{}/conegp".format(home_path)):
        run("git pull")
        run("{} && pip install -r requeriments.txt".format(activate_env_staging))
        run("{} && {} collectstatic --noinput {}".format(activate_env_staging, manage,
                                                         settings_staging))
        run("{} && {} migrate {}".format(activate_env_staging, manage, settings_staging))
        sudo("service nginx restart", pty=False)
        sudo("supervisorctl restart gunicorn_conegp", pty=False)
    print(green("Deploy conegp successful"))


def createsuperuser_staging():
    with cd("{}/conegp".format(home_path)):
        run("{} && {} createsuperuser {}".format(activate_env_staging, manage,
                                                 settings_staging))
    print(green("Createsuperuser successful"))




