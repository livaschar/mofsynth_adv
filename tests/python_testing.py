from mofsynth_adv.__utils__ import run_synthesis

directory = './data'
function='exec'
calc_choice='xtb'
opt_choice='lbfgs'
supercell_limit=25

run_synthesis(directory, function, calc_choice, opt_choice, supercell_limit)

function='report'
run_synthesis(directory, function, calc_choice, opt_choice, supercell_limit)