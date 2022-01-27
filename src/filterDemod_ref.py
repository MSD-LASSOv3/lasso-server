#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Filterdemod Ref
# GNU Radio version: 3.8.2.0

from gnuradio import analog
from gnuradio import blocks
import pmt
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation


class filterDemod_ref(gr.top_block):

    def __init__(self, cutoff_freq=80000, decimation=1, gain=1, samp_rate=2000000, save_file='', source_file='', trans_width=2000):
        gr.top_block.__init__(self, "Filterdemod Ref")

        ##################################################
        # Parameters
        ##################################################
        self.cutoff_freq = cutoff_freq
        self.decimation = decimation
        self.gain = gain
        self.samp_rate = samp_rate
        self.save_file = save_file
        self.source_file = source_file
        self.trans_width = trans_width

        ##################################################
        # Blocks
        ##################################################
        self.low_pass_filter_0_1 = filter.fir_filter_ccf(
            decimation,
            firdes.low_pass(
                gain,
                samp_rate,
                cutoff_freq,
                trans_width,
                firdes.WIN_HAMMING,
                6.76))
        self.blocks_wavfile_sink_0 = blocks.wavfile_sink(save_file, 1, samp_rate, 8)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, source_file, False, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=samp_rate,
        	audio_decimation=1,
        )



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_wfm_rcv_0, 0), (self.blocks_wavfile_sink_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.low_pass_filter_0_1, 0))
        self.connect((self.low_pass_filter_0_1, 0), (self.analog_wfm_rcv_0, 0))


    def get_cutoff_freq(self):
        return self.cutoff_freq

    def set_cutoff_freq(self, cutoff_freq):
        self.cutoff_freq = cutoff_freq
        self.low_pass_filter_0_1.set_taps(firdes.low_pass(self.gain, self.samp_rate, self.cutoff_freq, self.trans_width, firdes.WIN_HAMMING, 6.76))

    def get_decimation(self):
        return self.decimation

    def set_decimation(self, decimation):
        self.decimation = decimation

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.low_pass_filter_0_1.set_taps(firdes.low_pass(self.gain, self.samp_rate, self.cutoff_freq, self.trans_width, firdes.WIN_HAMMING, 6.76))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.low_pass_filter_0_1.set_taps(firdes.low_pass(self.gain, self.samp_rate, self.cutoff_freq, self.trans_width, firdes.WIN_HAMMING, 6.76))

    def get_save_file(self):
        return self.save_file

    def set_save_file(self, save_file):
        self.save_file = save_file
        self.blocks_wavfile_sink_0.open(self.save_file)

    def get_source_file(self):
        return self.source_file

    def set_source_file(self, source_file):
        self.source_file = source_file
        self.blocks_file_source_0.open(self.source_file, False)

    def get_trans_width(self):
        return self.trans_width

    def set_trans_width(self, trans_width):
        self.trans_width = trans_width
        self.low_pass_filter_0_1.set_taps(firdes.low_pass(self.gain, self.samp_rate, self.cutoff_freq, self.trans_width, firdes.WIN_HAMMING, 6.76))




def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--cutoff-freq", dest="cutoff_freq", type=intx, default=80000,
        help="Set cutoff_freq [default=%(default)r]")
    parser.add_argument(
        "--decimation", dest="decimation", type=intx, default=1,
        help="Set decimation [default=%(default)r]")
    parser.add_argument(
        "--gain", dest="gain", type=intx, default=1,
        help="Set gain [default=%(default)r]")
    parser.add_argument(
        "--samp-rate", dest="samp_rate", type=intx, default=2000000,
        help="Set samp_rate [default=%(default)r]")
    parser.add_argument(
        "--save-file", dest="save_file", type=str, default='',
        help="Set save_file [default=%(default)r]")
    parser.add_argument(
        "--source-file", dest="source_file", type=str, default='',
        help="Set source_file [default=%(default)r]")
    parser.add_argument(
        "--trans-width", dest="trans_width", type=intx, default=2000,
        help="Set trans_width [default=%(default)r]")
    return parser


def main(top_block_cls=filterDemod_ref, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(cutoff_freq=options.cutoff_freq, decimation=options.decimation, gain=options.gain, samp_rate=options.samp_rate, save_file=options.save_file, source_file=options.source_file, trans_width=options.trans_width)

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    tb.wait()


if __name__ == '__main__':
    main()
