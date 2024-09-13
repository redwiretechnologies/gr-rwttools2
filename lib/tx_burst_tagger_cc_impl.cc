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

//TODO:  Check on: "d_next_sob_pos += d_packet_len;" (line 87 and 91). Why is this still necessary? The block does not work without it.

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "tx_burst_tagger_cc_impl.h"
#include <typeinfo>
#include <inttypes.h>

namespace gr {
  namespace rwt_tools {

    tx_burst_tagger_cc::sptr
    tx_burst_tagger_cc::make(int16_t add_length, uint16_t multiplier)
    {
      return gnuradio::get_initial_sptr(new tx_burst_tagger_cc_impl(add_length, multiplier));
    }


    /*
     * The private constructor
     */
    tx_burst_tagger_cc_impl::tx_burst_tagger_cc_impl(int16_t add_length, uint16_t multiplier)
            : gr::sync_block("tx_burst_tagger_cc",
                             gr::io_signature::make(1, 1, sizeof(gr_complex)),
                             gr::io_signature::make(1, 1, sizeof(gr_complex))),
                             d_add_length(add_length),
                             d_multiplier(multiplier),
                             d_next_sob_pos(0),
                             d_next_eob_pos(0),
                             d_itemsize(sizeof(gr_complex)),
                             d_packet_len(911)
        {}

    /*
     * Our virtual destructor.
     */
    tx_burst_tagger_cc_impl::~tx_burst_tagger_cc_impl()
    {
    }

    int
    tx_burst_tagger_cc_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
            const gr_complex *in = (const gr_complex *) input_items[0];
            gr_complex *out = (gr_complex *) output_items[0];
            
            std::vector<tag_t> tags;
            
            get_tags_in_range(tags, 0, nitems_read(0), nitems_read(0)+noutput_items);
            for(size_t i=0; i<tags.size(); i++){
                if(pmt::eqv( tags[i].key , pmt::intern("packet_len"))){       
                    d_next_sob_pos = (uint64_t) tags[i].offset;
                    d_packet_len = (pmt::to_uint64(tags[i].value) + d_add_length)*d_multiplier;
                    d_next_eob_pos = d_next_sob_pos + d_packet_len-1;
                } 
            }
            
            memcpy(out, in, noutput_items * d_itemsize);
            
            while(d_next_sob_pos < nitems_written(0) + noutput_items){
                add_item_tag(0, d_next_sob_pos, pmt::string_to_symbol("tx_sob"), pmt::PMT_T, pmt::string_to_symbol("Burst Tagger"));
                d_next_sob_pos += d_packet_len;
            }
            while(d_next_eob_pos < nitems_written(0) + noutput_items){
                add_item_tag(0, d_next_eob_pos, pmt::string_to_symbol("tx_eob"), pmt::PMT_T, pmt::string_to_symbol("Burst Tagger"));
                d_next_eob_pos += d_packet_len;
            }
            
            // Tell runtime system how many output items we produced.
            return noutput_items;
        }

  } /* namespace rwt_tools */
} /* namespace gr */

