

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 16:59:04 2022

@author: christoph
"""

from bitboard import *
from movegen import *


class Move:
    def __init__(self, b, player_code, bb_from, bb_to):
        self.b = b
        self.player_code = player_code
        self.bb_from = bb_from
        self.bb_to = bb_to
        
    def simulate(self):
        pass