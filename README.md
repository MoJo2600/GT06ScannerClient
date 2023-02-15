# GT06ScannerClient for GPSD

The GT06ScannerClient was written to be run on a mobile computer to update a system compatible with the GT06 protocol. Specifically, this client targets the open source Traccar platform and was developed based on this codebase.

This fork was created to utilize [GPSD](https://gpsd.gitlab.io/gpsd/) as the lone provider for GPS information. The original code is locking the GPS device and so only this program can use the information. By utilizing GPSD, multiple services on
your device can use GPS information. I want to use this script alongside an [OpenautoPro](https://bluewavestudio.io/shop/openauto-pro-car-head-unit-solution/) installation which uses itself GPSD for GPS data. I additionally removed the GUI part of this script as it should only run as
a daemon script to push information to traccar. This also removed the pygame requirements.

## Prerequisites

The GT06ScannerClient relies on the following prerequisites:

* Python version 3.4 or greater
* Git
* pip for installation of Python modules
* A mobile internet connection for communication with the server
* for the server, you will need to know the
  * hostname/ip address of the host server
  * port for GT06 communication
* A GPS receiver attached to the computer and configured to be used by GPSD

## Installation

* In the installation directory run

```bash
cd /opt
git clone https://github.com/mojo2600/GT06ScannerClient.git
cd GT06ScannerClient
```

* You can create a virtual environment to run the application (This step is optional).

```bash
python3 -m venv venv
source venv/bin/activate
```

* Install the prerequisite Python modules

```bash
pip install -r requirements.txt
```

## Configuration

* Edit the config.xml file to point to the correct server and device information.
* In this installation, you can use your favorite editor.  However, for this example we will be using Windows Notepad.
* Open the file for editing.

```bash
notepad config.xml
```

* The following settings should be as follows:
  * /ScannerSettings/ScannerIDNumber - Scanner identifier number (This is usually the IMEI)
  * /ScannerSettings/GT06ClientSettings/Hostname - Hostname or IP address of the GPS tracking server
  * /ScannerSettings/GT06ClientSettings/Port - The port number for the service running the GT06 protocol on the host server
  * /ScannerSettings/GT06ClientSettings/UpdateDelay - The delay (in seconds) to wait between GPS scanner updates to the server

## Running the application

* To run the application, you will have to do the following steps, based on your installation.
* Change into the directory containing the GT06ScannerClient script:

```bash
cd GT06ScannerClient
```

* If you installed the Python module dependencies in a virtual environment (after following the optional venv step), you will need to ensure that you source the virtual environment.

```bash
source venv/bin/activate
```

* Run the client application

```bash
python runClient.py
```

## Stopping the application

* To stop the application, type Ctrl-C
* If you sourced a virtual environment, you can deactivate the virtual environment by entering the following command:

```bash
deactivate
```

## Setup Systemd daemon

* You have to install the code for this in the /opt directory or you'll have to update the path in the service script
* Copy the daemon script to the systemd folder
* Reload the configuration
* Enable the service

```bash
cp systemd/gpstracker.service /etc/systemd/system
systemctl daemon-reload
systemctl enable gpstracker
systemctl start gpstracker
```

* You can check the status of the daemon

```bash
systemctl status gpstracker
journalctl -fu gpstracker
```