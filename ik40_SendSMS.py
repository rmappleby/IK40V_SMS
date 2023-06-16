#!/usr/bin/env python3
"""
<Program Name>
    ik40_SendSMS.py
<Author>
    Richard Appleby 
<Purpose>
    Provides a command line interface to an Alcatel Linkkey IK40V 4G mobile broadband dongle, allowing
    the sending of SMS messages without needing to navigate its web interface.
<Usage>
    ik40_SendSMS <mobileNumber> <SMS message text>
"""

# Needed to make HTML requests
import requests
# Needed to generate a timestamp for sending SMS message
import datetime
# Needed to sleep for a delay
import time
# Needed for argument handling
import sys


# The webservices URL on the Alcatel IK40 4G dongle
URL = "http://ik40.home/jrd/webapi"

JSON_CHECKREQUEST = { 
    "jsonrpc":"2.0",
    "method":"GetSendSMSResult",
    "params":{},
    "id":"6.7"
}

# Headers required to authenticate with JSON rpc (assessed by trial and error)
HEADERS = {
    "Host": "ik40.home",
    "Origin": "http://ik40.home",
    "Referer": "http://ik40.home/default.html"
}


def main():
    # Check arguments 'Number of arguments:', len(sys.argv), 'arguments.'
    if len(sys.argv) < 3:
        print("Not enough arguments:", sys.argv[0], "mobileNumber> <SMS message text>")
        quit(1)

    # Concatenate everything after the 1st argument into a single string
    # This will collapse multiple contiguous instances of whitespace
    allargs = ' '.join(str(e) for e in sys.argv[2:])

    # Generate a timestamp in the format "2023-06-14 22:15:01"
    timeNow = datetime.datetime.now()
    dateTime = timeNow.strftime("%Y-%m-%d %H:%M:%S")

    JSON_SENDREQUEST = {
        "jsonrpc":"2.0",
        "method":"SendSMS",
        "params":{
            "SMSId":-1,
            "SMSContent":allargs,
            "PhoneNumber":[sys.argv[1]],
            "SMSTime":dateTime},
        "id":"6.6"
        }

    # Tell the modem that we want to send an SMS message ...
    r = requests.post(URL, json=JSON_SENDREQUEST, headers=HEADERS)

    # If there is an "error" attribute, we're in trouble...
    if hasattr(r.json(), "error") :
        # Print the error attribute and quit...
        print("SendSMS Error:", r.json() )
        quit()

    # For some reason, this doesn't seem to actually cause the message
    # to be sent. It seems to be necessary to check the sent status of the
    # message, using GetSendSMSResult, before the message is actually 
    # transmitted.
    # Note also, calling the GetSendSMSResult too soon after the SendSMS 
    # action sometimes seems to prevent message transmission too, so
    # pause here for 1 second...
    time.sleep(1)

    # Loop around waiting for a settled status for the SMS send operation
    # Possible values:
    # SMS_SEND_STATUS_NONE = 0;         // none
    # SMS_SEND_STATUS_SENDING = 1;      // sending
    # SMS_SEND_STATUS_SUCCESS = 2;      // success
    # SMS_SEND_STATUS_FAIL_SENDING = 3; // failstill sending last message
    # SMS_SEND_STATUS_FULL = 4;         // fail with Memory full
    # SMS_SEND_STATUS_FAILED = 5;       // fail

    while True:
        # Check the status of the message send operation ...
        r = requests.post(URL, json=JSON_CHECKREQUEST, headers=HEADERS)

        # If there is an "error" attribute we're in trouble...
        if hasattr(r.json(), "error") :
            # Print the error attribute and quit...
            print("GetSendSMSResult Error:", r.json() )
            quit()

        if r.json().get("result", {}).get("SendStatus") == 2:
            # SMS sent 
            print("SMS sucessfully sent")
            quit()

        if r.json().get("result", {}).get("SendStatus") > 2:
            # SMS failed to send 
            print("SMS failed to send")
            print("GetSendSMSResult Error:", r.json() )
            quit()

        time.sleep(0.5)
    quit()

if __name__ == "__main__":
  main()
