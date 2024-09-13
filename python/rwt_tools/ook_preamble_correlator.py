#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2019 Red Wire Technologies.
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


from gnuradio import gr,blocks,digital,analog
from gnuradio import rwt_tools

class ook_preamble_correlator(gr.hier_block2):
    """
    docstring for block ook_preamble_correlator
    """
    def __init__(self, sampleRate=1e6, symbolRate=10e3, preamble=[1,0,1,0,1,0,1,0], threshold = 0.9):
        gr.hier_block2.__init__(self,
            "ook_preamble_correlator",
            gr.io_signature(1, 1, gr.sizeof_float),  # Input signature
            gr.io_signature(2, 2, gr.sizeof_float)) # Output signature
        
        ##################################################
        # Variables
        ##################################################
        self.symbolRate = symbolRate
        self.sampleRate = sampleRate
        self.sps = sampleRate/symbolRate
        self.preamble = preamble
        self.threshold = threshold

        ##################################################
        # Blocks
        ##################################################
        self.rebuild_modulation()
        self.flt = rwt_tools.corr_est_ff(self.taps, self.sps, 0, self.threshold, digital.THRESHOLD_ABSOLUTE)

        ##################################################
        # Connections
        ##################################################

        # Connect Input
        self.connect(self, (self.flt,0))
        
        # Connect Output
        self.connect((self.flt,0), (self,0))
        self.connect((self.flt,1), (self,1))

    def set_preamble(self,preamble):
        self.preamble = preamble
        self.rebuild_modulation()
        self.flt.set_symbols(self.taps)
    
    def set_symbolRate(self,symbolRate):
        self.symbolRate = symbolRate
        self.rebuild_modulation()
        self.flt.set_sps(self.sps)
        self.flt.set_symbols(self.taps)
        
    def set_sampleRate(self,sampleRate):
        self.sampleRate = sampleRate
        self.rebuild_modulation()
        self.flt.set_symbols(self.taps)
        self.flt.set_sps(self.sps)
        
    def set_threshold(self,threshhold):
        self.threshhold = threshhold
        self.flt.set_threshold(self.threshold)
        
    def rebuild_modulation(self):
        self.sps = self.sampleRate/self.symbolRate
        print ("self.sps " + str(self.sps))
        vsource = blocks.vector_source_b(self.preamble, False, 1, [])      
        chunks_to_symbols = digital.chunks_to_symbols_bf([-1,1], 1)
        repeat = blocks.repeat(gr.sizeof_float*1, int(self.sps))
        vsink = blocks.vector_sink_f()

        tbtaps = gr.top_block()
        tbtaps.connect((vsource, 0),(chunks_to_symbols, 0),(repeat, 0),(vsink, 0))
        tbtaps.run();
        
        self.taps = list(vsink.data())
        #print(self.taps)
        self.taps.reverse()
        self.taps = list(map(lambda x: x.conjugate(), self.taps))

a = ook_preamble_correlator();
