# This file is part of MOFSynth-ADV.
# Copyright (C) 2026 Charalampos G. Livas

# MOFSynth-ADV is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""
MOFSynth-ADV is a Python package for synthesizability evaluation, with
emphasis on reticular chemistry.
"""

__author__ = 'Charalampos G. Livas'
__version__ = "1.0.0"
__copyright__ = "Copyright (c) 2026 Charalampos G. Livas"
__license__ = 'GPL-3.0-only'

from mofsynth_adv.core import MOF, Linkers
from mofsynth_adv.workflow import SynthesizabilityWorkflow, run_synthesis

__all__ = ["MOF", "Linkers", "SynthesizabilityWorkflow", "run_synthesis"]
