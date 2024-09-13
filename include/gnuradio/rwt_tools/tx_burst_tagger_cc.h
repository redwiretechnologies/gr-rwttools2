/* -*- c++ -*- */
/* 
 * Copyright 2019, 2021 Red Wire Technologies.
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

#ifndef INCLUDED_RWT_TOOLS_TX_BURST_TAGGER_CC_H
#define INCLUDED_RWT_TOOLS_TX_BURST_TAGGER_CC_H

#include <gnuradio/rwt_tools/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace rwt_tools {

    /*!
     * \brief <+description of block+>
     * \ingroup rwt_tools
     *
     */
    class RWT_TOOLS_API tx_burst_tagger_cc : virtual public gr::sync_block
    {
     public:
      typedef std::shared_ptr<tx_burst_tagger_cc> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of rwt_tools::tx_burst_tagger_cc.
       *
       * To avoid accidental use of raw pointers, rwt_tools::tx_burst_tagger_cc's
       * constructor is in a private implementation
       * class. rwt_tools::tx_burst_tagger_cc::make is the public interface for
       * creating new instances.
       */
      static sptr make(int16_t add_length, uint16_t multiplier);
    };

  } // namespace rwt_tools
} // namespace gr

#endif /* INCLUDED_RWT_TOOLS_TX_BURST_TAGGER_CC_H */

