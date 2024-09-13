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

#ifndef INCLUDED_RWT_TOOLS_ZERO_PAD_H
#define INCLUDED_RWT_TOOLS_ZERO_PAD_H

#include <gnuradio/rwt_tools/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace rwt_tools {

    /*!
     * \brief <+description of block+>
     * \ingroup rwt_tools
     *
     */
    class RWT_TOOLS_API zero_pad : virtual public gr::sync_block
    {
     public:
      typedef std::shared_ptr<zero_pad> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of rwt_tools::zero_pad.
       *
       * To avoid accidental use of raw pointers, rwt_tools::zero_pad's
       * constructor is in a private implementation
       * class. rwt_tools::zero_pad::make is the public interface for
       * creating new instances.
       */
      static sptr make(uint32_t RampUp, uint32_t RampDown, uint32_t PacketSize);
    };

  } // namespace rwt_tools
} // namespace gr

#endif /* INCLUDED_RWT_TOOLS_ZERO_PAD_H */

