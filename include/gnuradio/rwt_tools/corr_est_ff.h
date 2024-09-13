/* -*- c++ -*- */
/* 
 * Copyright 2019 Red Wire Technologies.
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

#ifndef INCLUDED_RWT_TOOLS_CORR_EST_FF_H
#define INCLUDED_RWT_TOOLS_CORR_EST_FF_H

#include <gnuradio/rwt_tools/api.h>
#include <gnuradio/sync_block.h>
#include <gnuradio/rwt_tools/common.h>

namespace gr {
  namespace rwt_tools {

    /*!
     * \brief <+description of block+>
     * \ingroup rwt_tools
     *
     */
    class RWT_TOOLS_API corr_est_ff : virtual public gr::sync_block
    {
     public:
      typedef std::shared_ptr<corr_est_ff> sptr;

    /*!
     * Make a block that correlates against the \p symbols vector
     * and outputs a phase and symbol timing estimate.
     *
     * \param symbols           Set of symbols to correlate against (e.g., a
     *                          sync word).
     * \param sps               Samples per symbol
     * \param mark_delay        tag marking delay in samples after the
     *                          corr_start tag
     * \param threshold         Threshold of correlator, relative to a 100%
     *                          correlation (1.0). Default is 0.9.
     * \param threshold_method  Method for computing threshold.
     *
     */
      static sptr make(const std::vector <float> & symbols,
                     float sps,
                     unsigned int mark_delay,
                     float threshold = 0.9,
                     int threshold_method = 1);


      virtual std::vector<float> symbols() const = 0;
      virtual void set_symbols(const std::vector<float>& symbols) = 0;

      virtual unsigned int mark_delay() const = 0;
      virtual void set_mark_delay(unsigned int mark_delay) = 0;

      virtual float threshold() const = 0;
      virtual void set_threshold(float threshold) = 0;
    };

  } // namespace rwt_tools
} // namespace gr

#endif /* INCLUDED_RWT_TOOLS_CORR_EST_FF_H */

