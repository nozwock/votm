"""
Copyright (C) 2019 Sagar Kumar

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or 
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

"""
*Version 1.0.8 changes:
!> Dialog to use custom name for the merged database.
!> Dialog to choose the database from which the merge file is to be created.
!> Fixed merged db's datatypes.
"""

import os

__author__ = 'Sagar Kumar'
__version__ = '1.0.8'

ENV_KEY = 'BASE_VCON_CONFIG'
SECRET_KEY = 'SEC_VCON_KEY'

__up = lambda i: os.path.dirname(i)
__path = __up(__up(__up(os.path.abspath(__file__))))

with open(os.path.join(__path, "LICENSE"), 'r') as f:
    __license__ = f.read()
