/* -*- c++ -*- */
/* 
 * Copyright 2020 Red Wire Technologies.
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
/*
 * Copyright 2015 Free Software Foundation, Inc.
 *
 * This file is part of GNU Radio
 *
 * GNU Radio is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * GNU Radio is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with GNU Radio; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifndef INCLUDED_RWT_TOOLS_CORR_EST_FF_IMPL_H
#define INCLUDED_RWT_TOOLS_CORR_EST_FF_IMPL_H

#include <gnuradio/rwt_tools/corr_est_ff.h>
#include <gnuradio/filter/fft_filter.h>

using namespace gr::filter;

namespace gr {
  namespace rwt_tools {

    class corr_est_ff_impl : public corr_est_ff
    {
     private:
      pmt::pmt_t d_src_id;
      std::vector<float> d_symbols;
      float d_sps;
      unsigned int d_mark_delay, d_stashed_mark_delay;
      float d_thresh, d_stashed_threshold;
      kernel::fft_filter_fff* d_filter;

      float* d_corr;
      float* d_corr_mag;

      float d_scale;
      float d_pfa; // probability of false alarm

      int d_threshold_method;

      void _set_mark_delay(unsigned int mark_delay);
      void _set_threshold(float threshold);

     public:
      corr_est_ff_impl(const std::vector<float>& symbols, float sps, unsigned int mark_delay, float threshold = 0.9,
                     int threshold_method = 1);
      ~corr_est_ff_impl();
       
      std::vector<float> symbols() const;
      void set_symbols(const std::vector<float>& symbols);

      unsigned int mark_delay() const;
      void set_mark_delay(unsigned int mark_delay);

      float threshold() const;
      void set_threshold(float threshold);
      // Where all the action really happens
      int work(
              int noutput_items,
              gr_vector_const_void_star &input_items,
              gr_vector_void_star &output_items
      );
    };

  } // namespace rwt_tools
} // namespace gr

#endif /* INCLUDED_RWT_TOOLS_CORR_EST_FF_IMPL_H */

