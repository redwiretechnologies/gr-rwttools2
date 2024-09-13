#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2019, 2020 Red Wire Technologies.
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
import pmt
from gnuradio import gr

class message_router(gr.sync_block):
    """
    docstring for block message_router
    """
    def __init__(self, RouterKey, NumOutputs, ZeroIndexed):
        gr.sync_block.__init__(self,
            name="message_router",
            in_sig=None,
            out_sig=None)
        
        self.NumOutputs = NumOutputs
        self.RouterKey = RouterKey
        self.ZeroIndexed = ZeroIndexed
        
        self.message_port_register_in(pmt.intern("message_in"))
        self.set_msg_handler(pmt.intern("message_in"), self.message_handler)
        for index in range(0, NumOutputs):
            eval('self.message_port_register_out(pmt.intern("out%d"))' % index)


    def message_handler(self, msg):
        data = pmt.cdr(msg)
        meta = pmt.car(msg)
        
        OutputPortNum = pmt.to_python(pmt.dict_ref(meta, pmt.intern(self.RouterKey), pmt.from_uint64(0)))
        if(self.ZeroIndexed != True):
            OutputPortNum -= 1
        OutputPort = "out%d" % OutputPortNum
        
        self.message_port_pub(pmt.to_pmt(OutputPort), pmt.cons(meta, data))
