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

#ifndef INCLUDED_RWT_TOOLS_API_H
#define INCLUDED_RWT_TOOLS_API_H

#include <gnuradio/attributes.h>

#ifdef gnuradio_rwt_tools_EXPORTS
#define RWT_TOOLS_API __GR_ATTR_EXPORT
#else
#define RWT_TOOLS_API __GR_ATTR_IMPORT
#endif

#endif /* INCLUDED_RWT_TOOLS_API_H */
