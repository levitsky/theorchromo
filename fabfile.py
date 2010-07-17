# It it a modified version of Gareth Rushgrove's django via fabric deployment
# script. The directory structure has been slightly changed.
# Also several fixed were made for compatibility with Fabric v.0.9.1

from fabric.api import *

# Globals
env.project_name = 'theorchromo_online'

# Environments
def target_server():
    "Use the production server"
    env.hosts = ['76.10.212.149']
    env.project_path = '/home/bezalel/theorchromo_online'
    env.user = 'bezalel'
    env.virtualhost_path = "/"

# Tasks
def test():
    "Run the test suite and bail out if it fails"
    local("cd %(project_name)s; python manage.py test" % env)

def setup():
    """
    Setup a fresh virtualenv as well as a few useful directories, then run
    a full deployment
    """
    require('hosts', provided_by=[target_server])
    require('project_path')
    sudo('aptitude install -y python-setuptools')
    sudo('easy_install pip')
    sudo('pip install virtualenv')
    sudo('aptitude install -y apache2')
    sudo('aptitude install -y libapache2-mod-wsgi')

    # We want rid of the defult apache config
    sudo('cd /etc/apache2/sites-available/; a2dissite default;')
    run('mkdir -p %(project_path)s; cd %(project_path)s; virtualenv .;' % env)
    run(('cd %(project_path)s; mkdir releases; '+ 
        'mkdir shared; mkdir packages;') % env)
    deploy()

def deploy():
    """
    Deploy the latest version of the site to the servers, install any
    required third party modules, install the virtual host and 
    then restart the webserver
    """
    require('hosts', provided_by=[target_server])
    require('project_path')
    import time
    env.release = time.strftime('%Y%m%d%H%M%S')
    upload_tar_from_hg()
    install_requirements()
    install_site()
    symlink_current_release()
    migrate()
    restart_webserver()

def deploy_version(version):
    "Specify a specific version to be made live"
    require('hosts', provided_by=[target_server])
    require('project_path')
    env.version = version
    run(('cd %(project_path)s; rm releases/previous; '+
        'mv releases/current releases/previous;') % env)
    run('cd %(project_path)s; ln -s %(version)s releases/current' % env)
    restart_webserver()

def rollback():
    """
    Limited rollback capability. Simple loads the previously current
    version of the code. Rolling back again will swap between the two.
    """
    require('hosts', provided_by=[target_server])
    require('project_path')
    run('cd %(project_path)s; mv releases/current releases/_previous;' % env)
    run('cd %(project_path)s; mv releases/previous releases/current;' % env)
    run('cd %(project_path)s; mv releases/_previous releases/previous;' % env)
    restart_webserver()    

# Helpers. These are called by other functions rather than directly
def upload_tar_from_hg():
    require('release', provided_by=[deploy, setup])
    "Create an archive from the current Hg defalut branch and upload it"
    local('hg archive -p theorchromo_online -t tgz %(release)s.tar.gz' % env)
    run('mkdir %(project_path)s/releases/%(release)s' % env)
    put('%(release)s.tar.gz', '%(project_path)s/packages/' % env)
    run(('cd %(project_path)s/releases/%(release)s '+
        '&& tar zxf ../../packages/%(release)s.tar.gz --strip 1') % env)
    local('rm %(release)s.tar.gz' % env)

def install_site():
    "Add the virtualhost file to apache"
    require('release', provided_by=[deploy, setup])
    sudo(('cd %(project_path)s/releases/%(release)s; '+
         'cp %(project_name)s%(virtualhost_path)s%(project_name)s '+
         '/etc/apache2/sites-available/') % env)
    sudo('cd /etc/apache2/sites-available/; a2ensite %(project_name)s' % env) 

def install_requirements():
    "Install the required packages from the requirements file using pip"
    require('release', provided_by=[deploy, setup])
    run(('cd %(project_path)s; pip install -E . '+
        '-r ./releases/%(release)s/requirements.txt') % env)

def symlink_current_release():
    "Symlink our current release"
    require('release', provided_by=[deploy, setup])
    run(('cd %(project_path)s; rm releases/previous; '
        'mv releases/current releases/previous;' % env)
    run('cd %(project_path)s; ln -s %(release)s releases/current' % env)

def migrate():
    "Update the database"
    require('project_name')
    run('cd %(project_path)s/releases/current/%(project_name)s; '+
        '../../../bin/python manage.py syncdb --noinput')

def restart_webserver():
    "Restart the web server"
    sudo('/etc/init.d/apache2 restart')
