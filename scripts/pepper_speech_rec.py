#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Use ALSpeechRecognition Module"""

import qi
import argparse
import sys
import time
import threading

class PepperSpeechRec():

    def __init__(self, session):
        self.asr_service = session.service("ALSpeechRecognition")
        self.mem_service = session.service("ALMemory")

        self._lastheard = ""
        self._listenlock = True

        self.threads = []

        pT = threading.Thread(target=self.printMem)
        self.threads.append(pT)
        pT.start()

        vocabulary = ["yes", "no", "please"]
        self.listen(vocabulary, 20)

    def printMem(self):

        print "Started printmem thread"

        old = self._lastheard

        while(self._listenlock == True):
            while(self._lastheard == ""):
                self._lastheard = self.mem_service.getData("WordRecognized")

            if(old!= self._lastheard):
                print self._lastheard
            old = self._lastheard

    def listen(self, vocabulary, timeout):

        self.asr_service.pause(True)
        self.asr_service.setLanguage("English")

        # Example: Adds "yes", "no" and "please" to the vocabulary (without wordspotting)
        self.asr_service.setVocabulary(vocabulary, False)

        self.asr_service.pause(False)

        # Start the speech recognition engine with user Test_ASR
        self._listenlock = True
        self.asr_service.subscribe("Test_ASR")
        print 'Speech recognition engine started'
        time.sleep(timeout)
        self.asr_service.unsubscribe("Test_ASR")

        self._listenlock = False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    p = PepperSpeechRec(session)
