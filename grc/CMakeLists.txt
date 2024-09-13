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


install(FILES
    rwt_tools_channel_align.block.yml
    rwt_tools_message_filter.block.yml
    rwt_tools_message_router.block.yml
    rwt_tools_message_source.block.yml
    rwt_tools_message_to_stream.block.yml
    rwt_tools_ook_preamble_correlator.block.yml
    rwt_tools_stream_to_message.block.yml
    rwt_tools_corr_est_ff.block.yml
    rwt_tools_tx_burst_tagger_cc.block.yml
    rwt_tools_zero_pad.block.yml
    rwt_tools_buffer_stream_burst.block.yml
    DESTINATION share/gnuradio/grc/blocks
)
