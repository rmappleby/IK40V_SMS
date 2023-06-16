# IK40V_SMS
A command line interface to send SMS messages via the Alcatel Linkkey IK40V USB 4G dongle

The Alcatel IK40V is a USB-powered 4G cellular modem. It's a category 4 device, capable of up to 150Mbps downloads and 50Mbps uploads. This makes it useful as a mobile broadband connection, which is what I use it for, in conjunction with an OpenWRT-based router.

![ik40v](./ik40.jpg)

It connects to the router via RNDIS, which is essentially a virtual ethernet network run over the USB hardware interface. The IK40V defines the 192.168.1.1/24 network, taking the 192.168.1.1 address for itself, and issuing the router with an IP address in that network. The router can then send network traffic over the mobile network by routing packets through 192.168.1.1.

In addition, the modem implements a webserver, which allows the modem status to be examined and the configuration altered. Those webpages function by invoking a series of webservices provided by the modem, and include services to manipulate SMS messages; sending, receiving, storing and deleting SMS messages.

![sms](./sms.jpg)

This is especially interesting to me, as the mobile ISP contract I have provides me with unlimited inclusive SMS messages, opening up the possibility of using the modem and those "free" SMS messages to create a notification service for my home automation system. 

My plan was to build a simple command line application that would accept a telephone number and a message, and use the SMS functionality of the IK40V to send the message as an SMS message to the nominated telephone number. I could them trivially integrate that command line application into my home automation system using NodeRed.

This is that command line application. It takes a single telephone number as the first argument, and concatenates all subsequent arguments together into the message. This application doesn't carry out any validation checks on the phone number or message text. I leave that as an exercise for the interested reader :)

Tested / running on Python 3.10.6 on Ubuntu 22.04 LTS

## License

[MIT](./LICENSE)
