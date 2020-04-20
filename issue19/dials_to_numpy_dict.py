from __future__ import division, print_function
from dxtbx.model.experiment_list import ExperimentListFactory
from dials.array_family import flex
from libtbx import easy_pickle
import sys

# Specifiy experiment list and reflection table as arguments
expts_fn, refls_fn = sys.argv[1:3]

expts = ExperimentListFactory.from_json_file(expts_fn, check_format=False)
all_refls = flex.reflection_table.from_file(refls_fn)

# Save each reflection to numpy array in a dictionary
all_results = []
for expt_id, expt in enumerate(expts):
  results = {
  'refl_number': flex.size_t(),
  'pixel_value': flex.double(),
  'fast': flex.size_t(),
  'slow': flex.size_t(),
  'lab_x': flex.double(),
  'lab_y': flex.double(),
  'lab_z': flex.double(),
  'mask': flex.size_t(),
  }
  all_results.append(results)
  refls = all_refls.select(all_refls['id'] == expt_id)

  for i in range(len(refls)):
      panel = expt.detector[refls['panel'][i]]
      panel_fastmax, panel_slowmax = panel.get_image_size()
      x1, x2, y1, y2, z1, z2 = refls['bbox'][i]
      for f in range(max(x1,0), min(x2, panel_fastmax)):
          for s in range(max(y1, 0), min(y2, panel_slowmax)):
              x, y, z = panel.get_pixel_lab_coord((f,s))
              #print (i, refls['shoebox'][i].data[0,s-y1,f-x1], f, s, x, y, z, refls['shoebox'][i].mask[0,s-y1,f-x1])
              results['refl_number'].append(i)
              results['pixel_value'].append(refls['shoebox'][i].data[0,s-y1,f-x1])
              results['fast'].append(f)
              results['slow'].append(s)
              results['lab_x'].append(x)
              results['lab_y'].append(y)
              results['lab_z'].append(z)
              results['mask'].append(refls['shoebox'][i].mask[0,s-y1,f-x1])

for key in results:
  results[key] = results[key].as_numpy_array()

easy_pickle.dump('~/tmp/for_jamie.pickle', all_results)
