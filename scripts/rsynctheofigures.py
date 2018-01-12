"""
Rsync `figures` folders from local machine to Phantom.
"""

import os
import glob


if not os.environ.get('AZ_SNAKE'):
  raise KeyError('Environment variable AZ_SNAKE is not set')

source_dir = os.environ['AZ_SNAKE']
host = 'phantom.seas.gwu.edu'
dest_dir = '{}:/home/mesnardo/git/mesnardo/FlyingSnake2Cloud'.format(host)

wild_dir = os.path.join(source_dir, '**', 'figures')
figures_dirs = [os.path.relpath(folder, source_dir)
                for folder in glob.iglob(wild_dir, recursive=True)]

os.system('rsync -av -e ssh --relative {} {}'
          .format(' '.join(figures_dirs), dest_dir))
