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

#ifndef INCLUDED_RWT_TOOLS_ZERO_PAD_IMPL_H
#define INCLUDED_RWT_TOOLS_ZERO_PAD_IMPL_H

#include <gnuradio/rwt_tools/zero_pad.h>

namespace gr {
  namespace rwt_tools {

    class zero_pad_impl : public zero_pad
    {
     private:
      std::vector<gr_complex> d_RampUp;
      std::vector<gr_complex> d_RampDown;
      uint32_t d_PacketSize;

     public:
      zero_pad_impl(uint32_t RampUp, uint32_t RampDown, uint32_t PacketSize);
      ~zero_pad_impl();

      // Where all the action really happens
      int work(
              int noutput_items,
              gr_vector_const_void_star &input_items,
              gr_vector_void_star &output_items
      );
    };

  } // namespace rwt_tools
} // namespace gr

#endif /* INCLUDED_RWT_TOOLS_ZERO_PAD_IMPL_H */

