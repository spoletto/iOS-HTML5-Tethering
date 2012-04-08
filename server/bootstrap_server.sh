# Install the essentials.
sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get install -y rcconf
sudo apt-get install -y build-essential
sudo apt-get install -y libssl-dev
sudo apt-get install -y git-core

# Install Node.
wget http://nodejs.org/dist/node-v0.6.13.tar.gz
tar xzf node-v0.6.13.tar.gz
cd node-v0.6.13
sudo ./configure --prefix=/usr
make
sudo make install

# Install npm.
cd ~
git clone http://github.com/isaacs/npm.git
cd npm
sudo make install

# Install the node modules we'll need.
cd ~
npm install websocket-server express