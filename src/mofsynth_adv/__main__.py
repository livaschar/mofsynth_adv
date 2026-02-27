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

from mofsynth_adv.__cli__ import _transaction_summary, _return_cli_parser
from mofsynth_adv.workflow import run_synthesis

def main():
    

    args = _return_cli_parser().parse_args()
    _transaction_summary(args)

    #inp = input('\nIs this ok[y/N]: ')
    print('\n')
    inp='y'
    if inp.upper() == 'Y':
        print(f'\033[1;31m-------------------\033[m')
        run_synthesis(
            args.directory,
            args.function,
            args.calc_choice,
            args.opt_choice,
            args.time_limit,
            args.supercell_limit
            )
    else:
        print('Operation aborted.')

if __name__ == '__main__':
    main()