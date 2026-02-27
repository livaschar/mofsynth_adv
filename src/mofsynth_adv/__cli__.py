import os
import argparse
from mofsynth_adv import __version__ as version


def _return_cli_parser():
    
    parser = argparse.ArgumentParser(
        prog='mofsynth_adv',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Access synthesizability from a directory containig ``.cif`` files.',
        epilog='''A command line utility based on the MOFSynth-Adv package.'''
        )

    parser.add_argument('--version', action='version', version=f'%(prog)s {version}')
        
    parser.add_argument('function', help='The function to be called. Choices: exec, verify, report')

    parser.add_argument('directory', help='The path to the directory containing all CIF files.')

    parser.add_argument(
        '--calc',
        dest='calc_choice',
        default='xtb',
        choices=['xtb', 'mace_off', 'mace_mp'],
        help='Energy evaluation backend: xtb (GFN2-xTB), mace_off, mace_mp. Default: xtb.'
    )

    parser.add_argument(
        '--opt',
        dest='opt_choice',
        default='lbfgs',
        choices=['fire', 'bfgs', 'lbfgs', 'sella'],
        help='Geometry optimizer controlling structural relaxation. Default: lbfgs.'
    )

    parser.add_argument(
        '--time',
        dest='time_limit',
        type=int,
        default=20,
        help='Fragmentation time limit in seconds. Default: 20.'
    )

    parser.add_argument(
        '--supercell',
        dest='supercell_limit',
        type=int,
        default=None,
        help='''\
        The maximum length for each edge of the unit cell in Angstroms.
        This limit is used to determine whether a supercell should be created based on the dimensions of the original unit cell.
        If not provided, the supercell creation will not be constrained by a specific limit. A limit helps with speed and convergence'''
    )

    return parser


def _transaction_summary(args):
    try:
        col_size, _ = os.get_terminal_size()
    except OSError:
        # Fallback for environments without a terminal
        col_size = 80  # Default column size

    gap = col_size // 6
    num_cifs = len([i for i in os.listdir(args.directory) if i.endswith('.cif')])

    
    print('\nTransaction Summary')
    print(col_size*"=")
    print('\nReading from directory:')
    print(f'  \033[1;31m{args.directory}\033[m')
    print(f'\nCalculate for:')
    print(f'  \033[1;31m{num_cifs}\033[m')
    print('\nExecuting the Function')
    print(f'  \033[1;31m{args.function}\033[m')
    print('\nCalculator - Optimizer')
    print(f'  \033[1;31m{args.calc_choice} - {args.opt_choice}\033[m')
    print('\nTimelimit')
    print(f'  \033[1;31m{args.time_limit}\033[m')
    if args.supercell_limit is not None:
        print('\nSupercell limit set to:')
        print(f'  \033[1;31m{args.supercell_limit}\033[m')
    print(col_size*"=")
