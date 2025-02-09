/*
 * Copyright 2022 Free Software Foundation, Inc.
 *
 * This file is part of GNU Radio
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

/***********************************************************************************/
/* This file is automatically generated using bindtool and can be manually edited  */
/* The following lines can be configured to regenerate this file during cmake      */
/* If manual edits are made, the following tags should be modified accordingly.    */
/* BINDTOOL_GEN_AUTOMATIC(0)                                                       */
/* BINDTOOL_USE_PYGCCXML(0)                                                        */
/* BINDTOOL_HEADER_FILE(corr_est_ff.h)                                        */
/* BINDTOOL_HEADER_FILE_HASH(5d22d7ae2cf4dfccd868c95961d09611)                     */
/***********************************************************************************/

#include <pybind11/complex.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

#include <gnuradio/rwt_tools/corr_est_ff.h>
// pydoc.h is automatically generated in the build directory
#include <corr_est_ff_pydoc.h>

void bind_corr_est_ff(py::module& m)
{

    using corr_est_ff    = ::gr::rwt_tools::corr_est_ff;


    py::class_<corr_est_ff, gr::sync_block, gr::block, gr::basic_block,
        std::shared_ptr<corr_est_ff>>(m, "corr_est_ff", D(corr_est_ff))

        .def(py::init(&corr_est_ff::make),
           py::arg("symbols"),
           py::arg("sps"),
           py::arg("mark_delay"),
           py::arg("threshold") = 0.90000000000000002,
           py::arg("threshold_method") = 1,
           D(corr_est_ff,make)
        )
        




        
        .def("symbols",&corr_est_ff::symbols,       
            D(corr_est_ff,symbols)
        )


        
        .def("set_symbols",&corr_est_ff::set_symbols,       
            py::arg("symbols"),
            D(corr_est_ff,set_symbols)
        )


        
        .def("mark_delay",&corr_est_ff::mark_delay,       
            D(corr_est_ff,mark_delay)
        )


        
        .def("set_mark_delay",&corr_est_ff::set_mark_delay,       
            py::arg("mark_delay"),
            D(corr_est_ff,set_mark_delay)
        )


        
        .def("threshold",&corr_est_ff::threshold,       
            D(corr_est_ff,threshold)
        )


        
        .def("set_threshold",&corr_est_ff::set_threshold,       
            py::arg("threshold"),
            D(corr_est_ff,set_threshold)
        )

        ;




}








