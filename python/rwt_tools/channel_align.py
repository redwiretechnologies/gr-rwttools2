#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 Red Wire Technologies.
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import numpy as np
import pmt
from gnuradio import gr
#import gnuradio.extras

class channel_align(gr.basic_block):
    """
    docstring for block channel_align
    """
    def __init__(self, NumChannels):
        gr.basic_block.__init__(self,
            name="channel_align",
            in_sig=[np.complex64],
            out_sig=[np.complex64])
        
        self.channel_align = np.array([], dtype=np.uint64)
        
    def forecast(self, noutput_items, ninput_items_required):
        #setup size of input_items[i] for work call
        for i in range(len(ninput_items_required)):
            ninput_items_required[i] = noutput_items
            
    def general_work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        num_input_items = len(in0)
        nread = self.nitems_read(0)
        
        tags = self.get_tags_in_range(0, nread, nread+num_input_items)
        
        for tag in tags:
            print(pmt.symbol_to_string(tag.key))
            if "channel_align" in pmt.symbol_to_string(tag.key):
                self.channel_align = np.append(self.channel_align, tag.offset)
        
        print(len(in0), len(out))
        
        out[:] = in0[0:len(out)]
        
        self.consume(0, len(out))
        
        return len(out)

