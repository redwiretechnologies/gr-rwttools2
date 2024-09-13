/* -*- c++ -*- */
/* 
 * Copyright 2019, 2021 Red Wire Technologies
 * 
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

#ifndef INCLUDED_RWT_TOOLS_TX_BURST_TAGGER_CC_IMPL_H
#define INCLUDED_RWT_TOOLS_TX_BURST_TAGGER_CC_IMPL_H

#include <gnuradio/rwt_tools/tx_burst_tagger_cc.h>

namespace gr {
  namespace rwt_tools {

    class tx_burst_tagger_cc_impl : public tx_burst_tagger_cc
    {
     private:
      int16_t d_add_length;
      uint16_t d_multiplier;
      uint64_t d_next_sob_pos;
      uint64_t d_next_eob_pos;
      size_t d_itemsize;
      uint64_t d_packet_len;

     public:
      tx_burst_tagger_cc_impl(int16_t add_length, uint16_t multiplier);
      ~tx_burst_tagger_cc_impl();

      // Where all the action really happens
      int work(int noutput_items,
         gr_vector_const_void_star &input_items,
         gr_vector_void_star &output_items);
    };

  } // namespace rwt_tools
} // namespace gr

#endif /* INCLUDED_RWT_TOOLS_TX_BURST_TAGGER_CC_IMPL_H */

