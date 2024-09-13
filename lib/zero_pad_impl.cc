/* -*- c++ -*- */
/* 
 * Copyright 2019, 2020 Red Wire Technologies.
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

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "zero_pad_impl.h"

namespace gr {
  namespace rwt_tools {

    zero_pad::sptr
    zero_pad::make(uint32_t RampUp, uint32_t RampDown, uint32_t PacketSize)
    {
      return gnuradio::get_initial_sptr
        (new zero_pad_impl(RampUp, RampDown, PacketSize));
    }


    /*
     * The private constructor
     */
    zero_pad_impl::zero_pad_impl(uint32_t RampUp, uint32_t RampDown, uint32_t PacketSize)
      : gr::sync_block("zero_pad",
              gr::io_signature::make(1, 1, PacketSize*sizeof(gr_complex)),
              gr::io_signature::make(1, 1, (PacketSize+RampUp+RampDown)*sizeof(gr_complex))),
              d_PacketSize(PacketSize)
    {
        d_RampUp.resize(RampUp);
        std::fill(d_RampUp.begin(), d_RampUp.end(), 0);
        d_RampDown.resize(RampDown);
        std::fill(d_RampDown.begin(), d_RampDown.end(), 0);
    }

    /*
     * Our virtual destructor.
     */
    zero_pad_impl::~zero_pad_impl()
    {
    }

    int
    zero_pad_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
      const gr_complex *in = (const gr_complex *) input_items[0];
      gr_complex *out = (gr_complex *) output_items[0];
      
      for(int k=0; k<noutput_items; k++){
          std::copy(d_RampUp.begin(), d_RampUp.end(), out);
          out += d_RampUp.size();
          std::copy(&in[k*d_PacketSize], &in[(k+1)*d_PacketSize], out);
          out += d_PacketSize;
          std::copy(d_RampDown.begin(), d_RampDown.end(), out);
          out += d_RampDown.size();
      }
          
      return noutput_items;
    }

  } /* namespace rwt_tools */
} /* namespace gr */

