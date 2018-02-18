# pinball_backglass
Web service to identify a pinball machine from a backglass image.

https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html#ec2-launch-instance

1. Choose an Amazon Machine Image (AMI)
* Ubuntu Server 16.04 LTS (HVM), SSD Volume Type - ami-79873901

2. Choose an Instance Type
* T2.micro

3. Configure Instance Details
* [defaults]

4. Add Storage
* [defaults]

5. Add Tags
* "instance_name" : "Pinball Backglass"

6. Configure Security Group
* SSH - My IP
* HTTP - Anywhere

Create a new key pair
* AWS_180218

Download Key Pair
* AWS_180218.pem


https://us-west-2.console.aws.amazon.com/ec2/v2/home?region=us-west-2#Instances:sort=instanceId

Select instance, Actions | Connect
* chmod 400 AWS_180218.pem
* Copy the Example ssh command into a bash command window

Flask
https://www.datasciencebytes.com/bytes/2015/02/24/running-a-flask-app-on-aws-ec2/

* sudo apt-get update
* sudo apt-get install apache2
* sudo apt-get install libapache2-mod-wsgi
* sudo apt install python-pip
* sudo pip install flask
* git clone http://github.com/Invader-Zim/pinball_backglass flaskapp
* sudo ln -sT ~/flaskapp /var/www/html/flaskapp


* nano /etc/apache2/sites-enabled/000-default.conf
'''
	# Add the following just after DocumentRoot /var/www/html
	WSGIDaemonProcess flaskapp threads=5
	WSGIScriptAlias / /var/www/html/flaskapp/flaskapp.wsgi

	<Directory flaskapp>
	    WSGIProcessGroup flaskapp
	    WSGIApplicationGroup %{GLOBAL}
	    Order deny,allow
	    Allow from all
	</Directory>
'''

* sudo apachectl restart


