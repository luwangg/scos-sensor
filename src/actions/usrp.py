"""Maintains a persistent connection to the USRP.

Example usage:
    >>> from actions import usrp
    >>> usrp.connect(config.RADIO_ID)
    >>> usrp.is_available
    True
    >>> rx = usrp.radio
    >>> rx.sample_rate = 10e6
    >>> rx.frequency = 700e6
    >>> rx.gain = 30
    >>> samples = rx.acquire_samples(1000)
"""

import logging

import numpy as np


logger = logging.getLogger(__name__)


try:
    from gnuradio import uhd
    uhd_is_available = True
except ImportError:
    uhd_is_available = False


radio = None
is_available = False


def connect(usrp_serial):  # -> bool:
    if not uhd_is_available:
        logger.warning("gnuradio.uhd not available - disabling radio")
        return False

    try:
        radio_iface = RadioInterface(usrp_serial)
        global is_available
        global radio
        is_available = True
        radio = radio_iface
        return True
    except RuntimeError as err:
        logger.error(err)
        return False


class RadioInterface(object):
    def __init__(self, serial):
        search_criteria = uhd.device_addr_t()

        if serial:
            search_criteria['serial'] = serial

        available_devices = list(uhd.find_devices(search_criteria))
        ndevices_found = len(available_devices)

        if ndevices_found != 1:
            err = "Found {} devices that matches USRP identification\n"
            err += "information in sysinfo:\n"
            err += search_criteria.to_pp_string()
            err += "\nPlease add/correct identifying information."
            err = err.format(ndevices_found)

            for device in available_devices:
                err += "    {}\n".format(device.to_pp_string())

            raise RuntimeError(err)

        device = available_devices[0]
        logger.debug("Using the following USRP:")
        logger.debug(device.to_pp_string())

        stream_args = uhd.stream_args('fc32')
        self.usrp = uhd.usrp_source(device_addr=device,
                                    stream_args=stream_args)

        self.usrp.set_auto_dc_offset(True)

    @property
    def sample_rate(self):  # -> float:
        return self.usrp.get_samp_rate()

    @sample_rate.setter
    def sample_rate(self, rate):
        self.usrp.set_samp_rate(rate)
        fs_MHz = self.sample_rate / 1e6
        logger.debug("set USRP sample rate: {} MS/s".format(fs_MHz))

    @property
    def clock_rate(self):  # -> float:
        return self.usrp.get_clock_rate()

    @clock_rate.setter
    def clock_rate(self, rate):
        self.usrp.set_clock_rate(rate)
        clk_MHz = self.clock_rate / 1e6
        logger.debug("set USRP clock rate: {} MHz".format(clk_MHz))

    @property
    def frequency(self):  # -> float:
        return self.usrp.get_center_freq()

    @frequency.setter
    def frequency(self, freq):
        tune_request = uhd.tune_request(freq)
        tune_result = self.usrp.set_center_freq(tune_request)
        logger.debug(tune_result.to_pp_string())

    @property
    def gain(self):  # -> float:
        return self.usrp.get_gain()

    @gain.setter
    def gain(self, gain):
        self.usrp.set_gain(gain)
        logger.debug("set USRP gain: {} dB".format(self.usrp.get_gain()))

    def acquire_samples(self, n, nskip=1000):  # -> np.ndarray:
        """Aquire nskip+n samples and return the last n"""
        total_samples = nskip + n
        acquired_samples = self.usrp.finite_acquisition(total_samples)
        data = np.array(acquired_samples[nskip:])
        nreceived = len(data)
        if nreceived != n:
            err = "Requested {} samples, but received {}"
            raise RuntimeError(err.format(n, nreceived))

        return data
