#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Red Wire Technologies.
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
from gnuradio import gr
import time
import pmt

class buffer_stream_burst(gr.sync_block):
    """
    sample_rate := sample rate of the receive chain
    buffer_time := Time in seconds to keep samples
    num_channels := Number of inputs to bufferf
    """
    def __init__(self, stream_sample_rate=1e6, buffer_time=1, num_channels=4):
        gr.sync_block.__init__(self,
            name="buffer_stream_burst",
            in_sig=[np.complex64]*num_channels,
            out_sig=None)
        
        self.message_port_register_out(pmt.intern("message_out"))


        self.num_samples = int(stream_sample_rate*buffer_time)
        self.num_channels = num_channels
        self.start_sample_index = -self.num_samples
        self.buffer = np.zeros((self.num_channels, self.num_samples), dtype=np.complex64)
        self.lock = False
        self.tic = 0
    
    def work(self, input_items, output_items):
        in0 = input_items[0]
        
        if len(input_items) != self.num_channels:
            raise AssertionError(f"Expected {self.num_channels} input streams. Recv {len(input_items)}")

        num_samples = len(in0)
        temp_buffer = np.copy(self.buffer)
        temp_buffer = np.roll(temp_buffer, -num_samples, axis=1)

        if time.time() - self.tic > 2: 
            self.tic = time.time()
            a = self.nitems_read(0)
            b = self.start_sample_index

        for i in range(self.num_channels):
            samp_length = len(input_items[i])
            if samp_length != num_samples:
                raise AssertionError(f"Inconsistent sample stream. Recv {samp_length}, " + \
                    f"Expected {num_samples}")
            temp_buffer[i, -num_samples:] = input_items[i]

        if self.lock:
            cnt = 5
            print("Locked")
            while cnt >= 0 and self.lock:
                time.sleep(0.00001)
            if not self.lock:
                self.buffer = temp_buffer
                self.start_sample_index += num_samples
        else:
            self.buffer = temp_buffer
            self.start_sample_index += num_samples
  
        return len(in0)

    def get_burst(self, offset, sample_len=800):
        if offset < self.start_sample_index:
            print("Warning: Asked for burst too far in past")
            return 
        elif offset > self.start_sample_index + self.num_samples - sample_len:
            cnt = 0
            #print("Warning: Asked for sample in near future...")
            while offset > self.start_sample_index + self.num_samples - sample_len and cnt <= 20:
                cnt += 1
                time.sleep(0.1)
            if cnt >= 20:
                print(f"Dropping Future: {offset}, {self.start_sample_index}, {offset - self.start_sample_index}")
                return

        self.lock = True
        rx_buffer = np.copy(self.buffer)
        start_sample_index = int(self.start_sample_index)
        self.lock = False

    
        start_idx = offset - start_sample_index
        stop_idx = start_idx + sample_len
        burst = rx_buffer[:, start_idx:stop_idx]

        out_data = pmt.to_pmt(burst)
        out_meta = pmt.make_dict()
        out_meta = pmt.dict_add(out_meta, pmt.string_to_symbol("tag_offset"), pmt.to_pmt(offset))
        out_meta = pmt.dict_add(out_meta, pmt.string_to_symbol("packet_len"), pmt.to_pmt(sample_len))
        self.message_port_pub(pmt.to_pmt("message_out"), pmt.cons(out_meta, out_data))
    
