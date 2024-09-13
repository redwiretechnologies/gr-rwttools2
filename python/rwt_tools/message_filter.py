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



import numpy
from gnuradio import gr
import pmt

class message_filter(gr.sync_block):
    """
    docstring for block message_filter
    """
    def __init__(self, BlockVector):
        gr.sync_block.__init__(self,
            name="message_filter",
            in_sig=None,
            out_sig=None)
        self.BlockVector = BlockVector
        
        self.message_port_register_in(pmt.intern("message_in"))
        self.set_msg_handler(pmt.intern("message_in"), self.message_handler)
        self.message_port_register_out(pmt.intern("message_out"))

    def message_handler(self, msg):
        meta = pmt.car(msg)
        data = pmt.to_python(pmt.cdr(msg))
        print(" [Message Filter] Data vector of length: %d" % data.size)
        
        if self.BlockVector == True:
            data = numpy.array([])
            
        else:
            data = pmt.to_python(pmt.cdr(msg))

        self.message_port_pub(pmt.to_pmt("message_out"), pmt.cons(meta, pmt.to_pmt(data)))
