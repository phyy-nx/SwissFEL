from xfel.ui import load_cached_settings
from xfel.ui.db.xfel_db import xfel_db_application
import sys
trial_number = int(sys.argv[1])

params = load_cached_settings()
db = xfel_db_application(params)

trial = db.get_trial(trial_number=trial_number)
for tag in trial.tags:
  if 'sample' not in tag.name: continue
  fn = "trial" + str(trial.trial) + "_" + tag.name.replace(" ", "_")
  timestamps, cells = db.get_stats(trial=trial, tags=[tag])()
  for ts, cell in zip(timestamps, cells):
    print("%13.10f %13.10f %13.10f %.1f %.1f %.1f %s %s_%s"%(
      cell.cell_a,cell.cell_b,cell.cell_c,cell.cell_alpha,cell.cell_beta,cell.cell_gamma,
      "".join(cell.lookup_symbol.split()), fn, ts))

