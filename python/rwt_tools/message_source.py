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
from gnuradio import gr
import pmt

class message_source(gr.sync_block):
    """
    docstring for block message_source
    """
    def __init__(self, vector, meta_name, meta_value):
        gr.sync_block.__init__(self,
            name="message_source",
            in_sig=None,
            out_sig=None)
        
        OutputMeta = pmt.make_dict()
        #OutputMeta = pmt.dict_add(OutputMeta, pmt.intern(meta_name), pmt.to_pmt(meta_value))
        #self.OutputMessage = pmt.cons(OutputMeta, pmt.to_pmt(numpy.array(vector, dtype=numpy.uint8)))
        OutputMeta = pmt.dict_add(OutputMeta, pmt.string_to_symbol(meta_name), pmt.from_uint64(meta_value))
        #OutputMeta = pmt.dict_add(OutputMeta, pmt.intern("direction"), pmt.intern("RX"))
        #OutputMeta = pmt.dict_add(OutputMeta, pmt.string_to_symbol("set_gpio_attr"), pmt.to_pmt(["FP0", "CTRL", 0x00, 0xff]))
        #OutputMeta = pmt.dict_add(OutputMeta, pmt.string_to_symbol("set_gpio_attr"), pmt.to_pmt(("FP0", "DDR", 0xff, 0xff)))
        #OutputMeta = pmt.dict_add(OutputMeta, pmt.string_to_symbol("set_gpio_attr"), pmt.to_pmt(("FP0", "OUT", 0x00, 0xff)))
        OutputData = pmt.make_vector(4, pmt.to_pmt(0))
        self.OutputMessage = pmt.cons(OutputMeta, OutputData)
        
        self.message_port_register_in(pmt.intern("trigger"))
        self.set_msg_handler(pmt.intern("trigger"), self.message_handler)
        self.message_port_register_out(pmt.intern("message_out"))
        

    def message_handler(self, msg):
        self.message_port_pub(pmt.to_pmt("message_out"), self.OutputMessage);

