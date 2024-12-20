import os
import shutil
import random
from ast import literal_eval
import numpy as np
import pandas as pd
from csv_modules.csv_writer import write_in_file
from general_utils.download_utils import download_pdb
from math import ceil

from general_utils.pdb_utils import get_chains_pdb, get_cube_pdb, move_pdb_center, \
  get_all_pdb_work
from general_utils.temp_utils import gen_dir, free_dir


def get_parallel_can_chains_chunk(pdb_name, dir_path):
  from general_utils.pdb_utils import get_chains_pdb

  download_pdb(pdb_name, '{0}/{1}.pdb'.format(dir_path, pdb_name))
  chains = get_chains_pdb('{0}/{1}.pdb'.format(dir_path, pdb_name))
  move_pdb_center('{0}/{1}.pdb'.format(dir_path, pdb_name))
  cube_dimensions = get_cube_pdb('{0}/{1}.pdb'.format(dir_path, pdb_name))
  result = [pdb_name, len(chains), cube_dimensions]
  os.remove('{0}/{1}.pdb'.format(dir_path, pdb_name))
  return result


def pdb_percentage(percentage, executor=None, min_can_chains=0):
  headers_csv = ['Pdb', 'Can Chains', 'Cube dimension']

  # List know can chains pdb
  know_can_chains_pdb_path = os.path.dirname(__file__) + '/../files/pdb_can_chains.csv'

  if os.path.exists(know_can_chains_pdb_path):
    pd_data_frame = pd.read_csv(know_can_chains_pdb_path,
                                converters={"Cube dimension": literal_eval})
    can_chains_list_name = pd_data_frame["Pdb"].tolist()
  else:
    can_chains_list_name = []

  # Process
  all_names = get_all_pdb_work()  # 169315
  # all_names = all_names[:3]
  all_names = np.setdiff1d(np.array(all_names), np.array(can_chains_list_name))
  all_names = all_names.tolist()

  # Add chains
  dirpath = gen_dir()

  flag_error = False

  if executor is not None:
    parallel_jobs = []
    for i in all_names:
      parallel_jobs.append([executor.submit(get_parallel_can_chains_chunk, i, dirpath)])

    for f in parallel_jobs:
      try:
        list_append = f[0].result()
        data_write = [list_append]
        write_in_file(know_can_chains_pdb_path, headers_csv, data_write)
      except Exception as e:
        flag_error = True
  else:
    for i in all_names:
      list_append = get_parallel_can_chains_chunk(i, dirpath)
      data_write = [list_append]
      write_in_file(know_can_chains_pdb_path, headers_csv, data_write)

  free_dir(dirpath)

  if flag_error:
    raise NameError('Error in download pdbs')

  # Gen data use
  pd_data_frame = pd.read_csv(know_can_chains_pdb_path,
                              converters={"Cube dimension": literal_eval})
  can_chains_list = pd_data_frame.values.tolist()
  can_chains_list_dic = {value[0]: value[1] for value in can_chains_list}
  can_chains_list = []
  for i in get_all_pdb_work():
    can_chains_list.append([i, can_chains_list_dic[i]])

  # Dic with can chains to pdbs
  dic_chains = {}
  for i in can_chains_list:
    can = i[1]
    pdb_name = i[0]

    if can in dic_chains:
      dic_chains[can].append(pdb_name)

    else:
      dic_chains[can] = [pdb_name]

  # Gen result
  result = []
  percentage_value = percentage / 100

  for i in dic_chains.keys():
    if i >= min_can_chains:
      real_can_add = ceil(len(dic_chains[i]) * percentage_value)
      random.shuffle(dic_chains[i])
      result += dic_chains[i][:real_can_add]

  return result


def remove_get_dirs(path, add_to_ignore_files=False, can_csv=1):
  result = []
  complete_path = os.path.abspath(path)
  list_dirs = os.listdir(complete_path)

  evil_pdb_path = os.path.dirname(__file__) + '/../files/pdb_no_work.txt'
  f_evil_pdb = open(evil_pdb_path, 'a+')

  for dir_name in list_dirs:
    check_path = '{0}/{1}'.format(complete_path, dir_name)
    files_dir = os.listdir(check_path)

    flag = True
    for i in files_dir:
      if i.find(".") == -1:
        flag = False
        break
      if not i.split('.')[1] == 'csv':
        flag = False
        break

    if len(files_dir) == can_csv and flag:
      result.append(dir_name)

    else:
      if add_to_ignore_files:
        all_pdb = True
        for i in files_dir:
          if i.find(".") == -1:
            all_pdb = False
            break
          if i.split('.')[1] != 'pdb':
            all_pdb = False
            break

        if all_pdb:
          f_evil_pdb.write(dir_name + '\n')

      shutil.rmtree(check_path)

  f_evil_pdb.close()
  return result
