# Path Forward for Development #

*Note: this portion of documentation is designed for the continued work on this codebase by Eastern Nazarene College during the summer research program. Please disregard this document if you are not part of the ENC Department of Engineering development team*

There are several facets of the data acquisition platform that require continued development. In no particular order, the following are additional tasks to accomplish and features to implement:

* Setup InfluxDB on the new development and production servers
* Refactor the script to follow standard object oriented practices for python
* Refactor the script to create a simple API for deployment
    * Wrap Influx code into a child of a new more general database object
    * Create object for the whole script which takes inputs representing the intervals
    * Wrap ADS1115 code into a child of a new more general ADC object
* Look into SSL certificates for the servers
* Add code to process the ADC values and convert them to voltage
* Refactor code to follow best practices for real-time capabilities
* Attempt to connect multiple ADC units to have more sensors available on each platform
* Run performance testing on platform and server
* Convert script to systemd service (daemon)

