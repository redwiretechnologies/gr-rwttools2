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
import threading

class stream_to_message(gr.sync_block):
    """
    docstring for block stream_to_message
    
    Test
    """
    def __init__(self, data_type, fixed_size, message_size, max_packet_buffer, min_packet_buffer, callback_fnc = lambda x: None):

        if data_type == 0:
            input_array = [np.uint8]
            self.data_array = np.array([], dtype=np.uint8)
        elif data_type == 1:
            input_array = [np.int16]
            self.data_array = np.array([], dtype=np.int16)
        elif data_type == 2:
            input_array = [np.float32]
            self.data_array = np.array([], dtype=np.float32)
        elif data_type == 3:
            input_array = [np.complex64]
            self.data_array = np.array([], dtype=np.complex64)
        else:
            print("[Stream to Message] Error: (Invalid Selection) Data type of the input message does not match the selected output type.")
            
        gr.sync_block.__init__(self,
            name="stream_to_message",
            in_sig=input_array,
            out_sig=None)
        
        self.callback = callback_fnc
        self.out_meta = pmt.make_dict()
        self.fixed_size = fixed_size
        self.message_size = message_size
        self.max_packet_buffer = max_packet_buffer
        self.min_packet_buffer = min_packet_buffer
        self.output_counter = 0
        self.tag_offset = 0
        self.sob_offset = 0
        self.sob_buffer = np.array([])
        self.eob_buffer = np.array([])

        self.packet_len = np.array([])
        self.packet_len_loc = np.array([])
        self.buffer_start_index = 0
        
        self.message_port_register_out(pmt.intern("message_out"))
        self.packet_present = False
        self.no_tags = False
        
        self.rx_time = 0

    def work(self, input_items, output_items):
        in0 = input_items[0]
        num_input_items = len(input_items[0])
        nread = self.nitems_read(0)

        #----- Fixed packet size -----#
        if self.fixed_size == 3:
            # Load the data into the buffer
            self.data_array = np.append(self.data_array, in0)
            
            while (self.data_array.size >= self.message_size):
                # Get tags within the specified range
                tags = self.get_tags_in_range(0, self.tag_offset, self.tag_offset + self.message_size)
                self.tag_offset += self.message_size
                for tag in tags:
                    #  Check for existing keys. Delete if existing.
                    if pmt.dict_has_key(self.out_meta, tag.key):
                        self.out_meta = pmt.dict_delete(self.out_meta, tag.key)
                        
                    #  Check if there are burst or packet_len tags
                    if ("sob" in pmt.symbol_to_string(tag.key)) or ("eob" in pmt.symbol_to_string(tag.key)) or ("packet_len"in pmt.symbol_to_string(tag.key)):
                        # We do not want to keep these tags when using fixed length
                        continue
                    else:
                        self.out_meta = pmt.dict_add(self.out_meta, tag.key, tag.value)
                        
                out_data = pmt.to_pmt(self.data_array[0:self.message_size])
                self.message_port_pub(pmt.to_pmt("message_out"), pmt.cons(self.out_meta, out_data))
                self.data_array = np.delete(self.data_array, range(0, self.message_size), None)
                self.out_data = pmt.make_dict()


        #----- Use packet_len tag to determine packet size -----#
        elif self.fixed_size == 2:
            # Load up the data buffer
            tags = self.get_tags_in_range(0, nread, nread+num_input_items)
            for tag in tags:
                ##  Check for "packet_len" tag
                if "packet_len" in pmt.symbol_to_string(tag.key):
                    self.packet_len = np.append(self.packet_len, pmt.to_python(tag.value))
                    self.packet_len_loc = np.append(self.packet_len_loc, tag.offset)
                else:
                    self.out_meta = pmt.dict_add(self.out_meta, tag.key, tag.value)        
            
            # If there are no tags, there are no packets. Dump the buffer.
            if self.packet_len.size == 0:
                self.data_array = np.delete(self.data_array, range(0, self.data_array.size), None)
                self.buffer_start_index = nread + num_input_items
            else:
                self.data_array = np.append(self.data_array, in0)
                used_packets = np.array([])
                for index in range(0, self.packet_len_loc.size):
                    if int(self.packet_len[index] + self.packet_len_loc[index]) <= (self.data_array.size + self.buffer_start_index):
                        buffer_offset = int(self.packet_len_loc[index]-self.buffer_start_index)
                        output_buffer = self.data_array[buffer_offset:buffer_offset+int(self.packet_len[index])]
                        out_data = pmt.to_pmt(output_buffer)
                        self.message_port_pub(pmt.to_pmt("message_out"), pmt.cons(self.out_meta, out_data))
                        used_packets = np.append(used_packets, index)
                        
                self.packet_len = np.delete(self.packet_len, used_packets, None)
                self.packet_len_loc = np.delete(self.packet_len_loc, used_packets, None)
                
                if self.packet_len.size > 0:
                    buffer_offset = int(self.packet_len_loc[0]-self.buffer_start_index)
                    self.data_array = np.delete(self.data_array, range(0, buffer_offset), None)
                    self.buffer_start_index = self.packet_len_loc[0]
                else:
                    self.data_array = np.delete(self.data_array, range(0, self.data_array.size), None)
                    self.buffer_start_index = nread + num_input_items
                
        #----- Use burst tags to determine packet size -----#
        elif self.fixed_size == 1:
            # Scan tags, put sob and eob into buffers and the rest into a dictionary
            tags = self.get_tags_in_range(0, nread, nread+num_input_items)
            for tag in tags:
                ##  Check if there is a start of burst tag and log its offset
                if "sob" in pmt.symbol_to_string(tag.key):
                    if self.sob_buffer.size > 0:
                        if tag.offset != self.sob_buffer[-1]:
                            self.sob_buffer = np.append(self.sob_buffer, tag.offset)
                    else:
                        self.sob_buffer = np.append(self.sob_buffer, tag.offset)
                
                ##  Check for end of burst tag
                elif "eob" in pmt.symbol_to_string(tag.key):
                    if self.eob_buffer.size > 0:
                        if tag.offset != self.eob_buffer[-1]:
                            self.eob_buffer = np.append(self.eob_buffer, tag.offset)
                    else:
                        self.eob_buffer = np.append(self.eob_buffer, tag.offset)
                        
                else:
                    self.out_meta = pmt.dict_add(self.out_meta, tag.key, tag.value)        
            
            # Create and send out PDUs based on the SOB/EOB pairs
            if self.packet_present == True:
                print("ONE!")
                # This does not currently handle bursts that overlap a full buffer
                if self.eob_buffer.size > 0:
                    print("TWO!")
                    self.data_array = np.append(self.data_array, in0[0:int(self.eob_buffer[0]+1)])
                    meta = pmt.make_dict()
                    #meta = pmt.dict_add(meta, pmt.string_to_symbol("packet_len"), pmt.to_pmt(self.eob_buffer[0] - self.temp_sob_index))
                    out_data = pmt.to_pmt(self.data_array)
                    self.message_port_pub(pmt.to_pmt("message_out"), pmt.cons(self.out_meta, out_data))
                    self.eob_buffer = np.delete(self.eob_buffer, 0)
                    self.packet_present = False
                    self.data_array = np.delete(self.data_array, range(0, self.data_array.size))
                else:
                    print("THREE!")
                    self.data_array = np.append(self.data_array, in0)
            
            while (self.sob_buffer.size > 0):
                print("FOUR!")
                if self.eob_buffer.size > 0:
                    out_data = pmt.to_pmt(in0[int(self.sob_buffer[0]-nread):int(self.eob_buffer[0]+1-nread)])
                    meta = pmt.make_dict()
                    #meta = pmt.dict_add(meta, pmt.string_to_symbol("packet_len"), pmt.to_pmt(self.eob_buffer[0] - self.sob_buffer[0]))
                    self.message_port_pub(pmt.to_pmt("message_out"), pmt.cons(self.out_meta, out_data))
                    self.sob_buffer = np.delete(self.sob_buffer, 0)
                    self.eob_buffer = np.delete(self.eob_buffer, 0)
                else:
                    # Changed the indexing so that we always use the first sob value
                    self.data_array = np.append(self.data_array, in0[int(self.sob_buffer[0])::])
                    self.temp_sob_index = self.sob_buffer[0]
                    self.sob_buffer = np.delete(self.sob_buffer, 0)
                    self.packet_present = True
            
            while (self.output_counter >= self.message_size):
                # Get tags within the specified range
                tags = self.get_tags_in_range(0, self.tag_offset, self.tag_offset + self.message_size)
                self.tag_offset = self.tag_offset + self.message_size
                for tag in tags:
                    #  Check for existing keys. Delete if existing.
                    if pmt.dict_has_key(self.out_meta, tag.key):
                        self.out_meta = pmt.dict_delete(self.out_meta, tag.key)
                        
                    #  Check if there is a start of burst tag and log its offset
                    if "sob" in pmt.symbol_to_string(tag.key):
                        self.sob_buffer = np.roll(self.sob_buffer, 1)
                        self.sob_buffer[0] = tag.offset
                    #  Check for end of burst tag
                    elif "eob" in pmt.symbol_to_string(tag.key):
                        self.eob_offset = tag.offset
                    else:
                        self.out_meta = pmt.dict_add(self.out_meta, tag.key, tag.value)
                        
                
                self.out_meta = pmt.dict_add(self.out_meta, pmt.string_to_symbol("packet_len"), pmt.to_pmt(self.message_size))
                self.message_port_pub(pmt.to_pmt("message_out"), pmt.cons(self.out_meta, out_data))
                self.data_array = np.delete(self.data_array, range(0, self.message_size), None)
                self.output_counter -= self.message_size
        
        
        #-----  Fixed size at correlation tags -----#
        else:
            # Scan tags
            tags = self.get_tags_in_window(0, 0, num_input_items)
            if self.packet_present:
                self.data_array = np.append(self.data_array, in0)
                # print("1 - %d" % len(self.data_array))

            for tag in tags:
                if "corr_start" in pmt.symbol_to_string(tag.key):
                    # print("2")
                    if not(self.packet_present):
                        # print("3")
                        self.data_array = np.append(self.data_array, in0[(tag.offset-nread)::])
                        self.packet_present = True
                        self.sob_offset = tag.offset

                    if (tag.offset - self.sob_offset) >= self.min_packet_buffer:
                        # print("4")
                        if (tag.offset - self.sob_offset) < self.max_packet_buffer:
                            # print("5")
                            #publish self.data_array[0:(tag.offset - self.sob_offset)]
                            meta = pmt.make_dict()
                            meta = pmt.dict_add(meta, pmt.string_to_symbol("packet_len"), pmt.to_pmt(tag.offset - self.sob_offset))
                            meta = pmt.dict_add(meta, pmt.string_to_symbol("tag_offset"), pmt.to_pmt(self.sob_offset))

                            out_data = pmt.to_pmt(self.data_array[0:(tag.offset - self.sob_offset)])
                            self.message_port_pub(pmt.to_pmt("message_out"), pmt.cons(meta, out_data))

                            self.data_array = np.delete(self.data_array, range(0, (tag.offset - self.sob_offset)))
                            self.sob_offset = tag.offset

                        else:
                            # print("6")
                            #publish self.data_array[0:self.max_packet_buffer]
                            meta = pmt.make_dict()
                            meta = pmt.dict_add(meta, pmt.string_to_symbol("packet_len"), pmt.to_pmt(self.max_packet_buffer))
                            meta = pmt.dict_add(meta, pmt.string_to_symbol("tag_offset"), pmt.to_pmt(self.sob_offset))

                            out_data = pmt.to_pmt(self.data_array[0:self.max_packet_buffer])
                            self.message_port_pub(pmt.to_pmt("message_out"), pmt.cons(meta, out_data))

                            self.data_array = np.delete(self.data_array, range(0, (tag.offset - self.sob_offset)))
                            self.sob_offset = tag.offset

            if len(self.data_array) >= self.max_packet_buffer:
                # print("7")
                #publish self.data_array[0:self.max_packet_buffer]
                meta = pmt.make_dict()
                meta = pmt.dict_add(meta, pmt.string_to_symbol("packet_len"), pmt.to_pmt(self.max_packet_buffer))
                meta = pmt.dict_add(meta, pmt.string_to_symbol("tag_offset"), pmt.to_pmt(self.sob_offset))

                out_data = pmt.to_pmt(self.data_array[0:self.max_packet_buffer])
                self.message_port_pub(pmt.to_pmt("message_out"), pmt.cons(meta, out_data))

                self.data_array = np.delete(self.data_array, range(0, len(self.data_array)))
                self.packet_present = False

                # print("7 - %d" % len(self.data_array))
        
        return len(in0)
