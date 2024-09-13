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



import numpy as np
import pmt
from gnuradio import gr

class message_to_stream(gr.sync_block):
    """
    This block takes a message as an input and outputs a stream. This version of the block assumes a fixed output buffer size.
    """
    def __init__(self, data_type, custom_meta):
        
        if data_type == 0:
            output_array = [np.uint8]
            self.data_buffer = np.array([], dtype=np.uint8)
            self.data_max = 32768
        elif data_type == 1:
            output_array = [np.int16]
            self.data_buffer = np.array([], dtype=np.int16)
            self.data_max = 16384
        elif data_type == 2:
            output_array = [np.float32]
            self.data_buffer = np.array([], dtype=np.float32)
            self.data_max = 8192
        elif data_type == 3:
            output_array = [np.complex64]
            self.data_buffer = np.array([], dtype=np.complex64)
            self.data_max = 4096
        else:
            print("[Message to Stream] Error: (Invalid Selection) Data type of the input message does not match the selected output type.")
            
        gr.sync_block.__init__(self,
            name="message_to_stream",
            in_sig=None,
            out_sig=output_array)
        
        self.message_flag = False
        self.tx_time_available = False
        self.rx_time_available = False
        self.custom_tag_available = False
        self.custom_meta = custom_meta
        
        self.message_port_register_in(pmt.intern("message_in"))
        self.set_msg_handler(pmt.intern("message_in"), self.message_handler)

    def message_handler(self, msg):
        data = pmt.to_python(pmt.cdr(msg))
        meta = pmt.car(msg)
        
        # Convert custom metadata to tags
        if pmt.dict_has_key(meta, pmt.intern(self.custom_meta)) == True:
            self.custom_tag_available = True
            self.custom_tag = pmt.dict_ref(meta, pmt.intern(self.custom_meta), pmt.from_uint64(0))
        # Convert time metadata to tags
        if pmt.dict_has_key(meta, pmt.intern("tx_time")) == True:
            self.tx_time_available = True
            self.time_tag = pmt.dict_ref(meta, pmt.intern("tx_time"), pmt.make_tuple(pmt.from_uint64(0), pmt.from_double(0)))
        if pmt.dict_has_key(meta, pmt.intern("rx_time")) == True:
            self.rx_time_available = True
            self.time_tag = pmt.dict_ref(meta, pmt.intern("rx_time"), pmt.make_tuple(pmt.from_uint64(0), pmt.from_double(0)))
            
        # Convert message size metadata to packet_len tag
        self.length_tag = data.size
        
        self.data_buffer = np.append(self.data_buffer, data)
        self.message_flag = True

    def work(self, input_items, output_items):
        out = output_items[0]

        #  TODO: Add a mechanism for when we receive another message before the first one has been fully sent into the stream
        
        if self.message_flag == False:
            return 0
        else:
            if self.data_buffer.size <= out.size:
                key = pmt.string_to_symbol("packet_len")
                value = pmt.to_pmt(self.length_tag)
                self.add_item_tag(0, self.nitems_written(0), key, value, pmt.string_to_symbol("Message to Stream"))
                
                if self.tx_time_available == True:
                    key = pmt.string_to_symbol("tx_time")
                    value = self.time_tag
                    self.add_item_tag(0, self.nitems_written(0), key, value, pmt.string_to_symbol("Message to Stream"))
                    self.tx_time_available = False
                
                if self.rx_time_available == True:
                    key = pmt.string_to_symbol("rx_time")
                    value = self.time_tag
                    self.add_item_tag(0, self.nitems_written(0), key, value, pmt.string_to_symbol("Message to Stream"))
                    self.rx_time_available = False
                
                if self.custom_tag_available == True:
                    key = pmt.string_to_symbol(self.custom_meta)
                    value = self.custom_tag
                    self.add_item_tag(0, self.nitems_written(0), key, value, pmt.string_to_symbol("Message to Stream"))
                    self.custom_tag_available = False
                
                out[0:self.data_buffer.size] = self.data_buffer
                self.message_flag = False
                temp_size = self.data_buffer.size
                self.data_buffer = np.delete(self.data_buffer, range(0, self.data_buffer.size))
                
                return temp_size

            else:
                out[0::] = self.data_buffer[0:out.size]
                self.data_buffer = np.delete(self.data_buffer, range(0, out.size))
                
                key = pmt.string_to_symbol("packet_len")
                value = self.length_tag
                self.add_item_tag(0, self.nitems_written(0), key, value, pmt.string_to_symbol("Message to Stream"))
                
                if self.tx_time_available == True:
                    key = pmt.string_to_symbol("tx_time")
                    value = self.time_tag
                    self.add_item_tag(0, self.nitems_written(0), key, value, pmt.string_to_symbol("Message to Stream"))
                    self.tx_time_available = False
                
                if self.rx_time_available == True:
                    key = pmt.string_to_symbol("rx_time")
                    value = self.time_tag
                    self.add_item_tag(0, self.nitems_written(0), key, value, pmt.string_to_symbol("Message to Stream"))
                    self.rx_time_available = False
                
                return out.size
