# -*- coding: utf-8 -*-
"""
This module contains the class for the BB84 protocol and main() to run it
"""

from parties import Sender
from parties import Receiver
from parties import Adversary
from channels import QuantumChannel
from channels import ClassicalChannel
from enum import Enum
from showbb84 import DisplayStyle
from showbb84 import Show

def main():
    alice = Sender(name='Alice')
    bob = Receiver(name='Bob')
    eve = Adversary()
    qu_chan = QuantumChannel(0)
    cl_chan = ClassicalChannel()
    

    qkd_run = BB84(alice, bob, eve, 10, qu_chan, cl_chan, verbose=True)
    show = Show(qkd_run, display_style=DisplayStyle.CONSOLE)

    qkd_run.initialise()
    
    qkd_run.send_key_as_photons()
    
    
    qkd_run.sift_keys()
    qkd_run.estimate_error()

    return


class BB84(object):
    """
    BB84 protocol

    Parameters
    ----------
    sender: Sender
        aka Alice

    reciever: Reciever
        aka Bob

    adversary: Adversary
        aka Eve

    init_key_len: int
        Initial length of the random bit array generated by the sender
        which will become the shared secret key

    qu_chan: QuantumChannel
        Quantum channel used to share photons between sender and reciever

    cl_chan: ClassicalChannel
        Classical channel used to share messages between sender and reciever
    """

    def __init__(self, sender, reciever, adversary, init_key_len,
                 qu_chan, cl_chan, verbose=False):
        self.sender = sender
        self.reciever = reciever
        self.adversary = adversary
        self.qu_chan = qu_chan
        self.cl_chan = cl_chan
        self.n = init_key_len
        self.verbose = verbose

    def initialise(self):
        """
        Initialise QKD

        Generate random key for sender and random bases for sender and reciever
        """
        self.sender.generate_initial_key(self.n)
        self.sender.generate_sending_bases(self.n)
        self.reciever.generate_receiving_bases(self.n)
        
        self.sender.qu_chan = self.qu_chan
        self.reciever.qu_chan = self.qu_chan
        self.sender.cl_chan = self.cl_chan
        self.reciever.cl_chan = self.cl_chan
        
        self.show_initialise()


    def send_key_as_photons(self):
        """
        * generate photons from sender's key and bases
        * send them through the quantum channel to reciever
        * generate reciever's initial key by measuring photons
        """
        
        
        self.show_send_key_as_photons()

    def sift_keys(self):
        """
        Communicate over classical channel to establish which photons
        reciever measured in correct basis and remove incorrect or missing
        bits from both sender's and reciever's keys
        """
        self.show_sift_keys()

    def estimate_error(self):
        """
        Communicate subset of key over classical channel to estimate error
        and remove shared bits
        """
        self.show_estimate_error()
    
    
    def show_initialise(self):
        if not self.verbose:
            return
        self.sender.print_state()
        self.reciever.print_state()
        return
    
    def show_send_key_as_photons(self):
        pass
    
    def show_sift_keys(self):
        pass
    
    def show_estimate_error(self):
        pass


class BB84Stage(Enum):
    INITIALISE = 1
    SEND_PHOTONS = 2
    SIFT_KEYS = 3
    ESTIMATE_ERROR = 4


if __name__ == '__main__':
    main()
