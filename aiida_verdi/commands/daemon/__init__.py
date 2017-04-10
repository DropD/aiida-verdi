# -*- coding: utf-8 -*-
"""
Assembling the verdi daemon cli
"""
from aiida_verdi.commands.daemon.daemon import daemon
from aiida_verdi.commands.daemon.start import start
from aiida_verdi.commands.daemon.stop import stop
from aiida_verdi.commands.daemon.status import status
from aiida_verdi.commands.daemon.logshow import logshow
from aiida_verdi.commands.daemon.restart import restart


daemon.add_command(start)
daemon.add_command(stop)
daemon.add_command(status)
daemon.add_command(logshow)
daemon.add_command(restart)


__all__ = ['daemon']
