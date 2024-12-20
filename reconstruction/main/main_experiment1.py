import sys
import pathlib

sys.path.append(str(pathlib.Path(__file__).parent.absolute()) + "/../")

import general_utils

from general_utils.workspace_utils import is_work_in_cluster
from general_utils.temp_utils import clean_work_dir
from csv_modules.csv_combine import combine_files_exp_1

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--number_exe', help='foo help')
args = parser.parse_args()

if args.number_exe is None:
  raise ("Can not run")

folder_work = "data_experiment_1_v2_exe_{}".format(args.number_exe)


def experiment_1():
  from experiment.experiment_1 import do_parallel_test_a
  if is_work_in_cluster():
    local_path = "/work/lcastillo"
  else:
    local_path = "/home/lcastillo98/Documents/git_projects/biostructure/reconstruction"

  print("Start")
  do_parallel_test_a("{0}/{1}".format(local_path, folder_work),
                     "result.csv",
                     [4, 6, 8, 10],
                     range_incompleteness=[10.0, 15.0],
                     percentage_data_set=10,
                     can_experiments_to_do=5,
                     file_checkpoint='check_expe_1.pkl',
                     add_to_ignore_files=False,
                     error_file="error_log_expe_1_exe_{}.txt".format(args.number_exe))
  print("Finish")


def union_test():
  if is_work_in_cluster():
    local_path = "/work/lcastillo/{0}".format(folder_work)
  else:
    local_path = "/home/lcastillo98/Documents/git_projects/biostructure/reconstruction/{0}".format(folder_work)

  combine_files_exp_1('salida_exper1_v2_{}.csv'.format(args.number_exe), local_path)


if __name__ == '__main__':
  if is_work_in_cluster():
    general_utils.temp_utils.global_temp_dir = "/work/lcastillo/temp_exp_1_exe_{}".format(args.number_exe)
  else:
    general_utils.temp_utils.global_temp_dir = None
  clean_work_dir()
  experiment_1()
  # result = get_similar_pdb("6LFS")
  # union_test()
