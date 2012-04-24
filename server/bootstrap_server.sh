# Install the essentials.
sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get install -y rcconf
sudo apt-get install -y build-essential
sudo apt-get install -y libssl-dev
sudo apt-get install -y git-core

# Install Node.
cd ~
wget http://nodejs.org/dist/node-v0.6.13.tar.gz
tar xzf node-v0.6.13.tar.gz
cd node-v0.6.13
sudo ./configure --prefix=/usr
make
sudo make install
cd ~
sudo rm -rf node-v0.6.13
sudo rm node-v0.6.13.tar.gz

# Install npm.
cd ~
git clone http://github.com/isaacs/npm.git
cd npm
sudo make install
cd ~
sudo rm -rf npm

# Install the node modules we'll need.
cd ~
npm install websocket-server express

# Install easy_install
sudo apt-get install python-setuptools

# Install Tornado
sudo easy_install tornado

# Install Scapy
cd ~
wget http://www.secdev.org/projects/scapy/files/scapy-2.1.0.tar.gz
tar xzf scapy-2.1.0.tar.gz
cd scapy-2.1.0
sudo python setup.py install
cd ~
sudo rm -rf scapy-2.1.0
sudo rm scapy-2.1.0.tar.gz

# Clone the repo
cd ~
git clone git://github.com/spoletto/iOS-HTML5-Tethering.git