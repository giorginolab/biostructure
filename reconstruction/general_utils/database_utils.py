import pymongo
import zlib, json, base64
import numpy as np
import os
from general_utils.download_utils import download_pdb
from general_utils.pdb_utils import get_chains_pdb
from general_utils.temp_utils import gen_dir, free_dir
from general_utils.workspace_utils import is_work_in_cluster
from pdb_to_mrc.pdb_2_mrc import pdb_to_mrc_chains
from process_graph.process_graph_utils import generate_graph
from process_mrc.generate import get_mrc_one
from networkx.readwrite import json_graph
from bson.json_util import dumps

ZIPJSON_KEY = 'base64(zip(o))'
database_name = "lcastillo_biostructures"
collection_name = "pdb_collection"
exists_mongo_db_var = None
valid_resolutions = [4, 6, 8, 10]


def json_zip(j):
  j = {
    ZIPJSON_KEY: base64.b64encode(
      zlib.compress(
        json.dumps(j).encode('utf-8')
      )
    ).decode('ascii')
  }

  return j


def json_unzip(j, insist=True):
  try:
    assert (j[ZIPJSON_KEY])
    assert (set(j.keys()) == {ZIPJSON_KEY})
  except:
    if insist:
      raise RuntimeError("JSON not in the expected format {" + str(ZIPJSON_KEY) + ": zipstring}")
    else:
      return j

  try:
    j = zlib.decompress(base64.b64decode(j[ZIPJSON_KEY]))
  except:
    raise RuntimeError("Could not decode/unzip the contents")

  try:
    j = json.loads(j)
  except:
    raise RuntimeError("Could interpret the unzipped contents")

  return j


def get_mongo_client():
  if is_work_in_cluster():
    client = pymongo.MongoClient(host="11.0.0.21",
                                 port=27017,
                                 username='lcastilloAdmin',
                                 password='LPtYJpA3',
                                 authSource='lcastillo_biostructures')
  else:
    client = pymongo.MongoClient()
  return client


def exists_mongo_db():
  # return False
  global exists_mongo_db_var
  if exists_mongo_db_var != None:
    return exists_mongo_db_var

  client = get_mongo_client()
  # Issue the serverStatus command and print the results
  try:
    client.server_info()
    exists_mongo_db_var = True
    return True
  except:
    exists_mongo_db_var = False
    return False


def get_graph_pdb_db(pdb_id, resolution):
  if resolution not in valid_resolutions:
    raise TypeError("Resolution is not valid, you can use: {0}".format(valid_resolutions))

  pdb_id = pdb_id.lower()
  if exists_mongo_db():
    client = get_mongo_client()
    db = client[database_name]
    col = db[collection_name]
    pdb_data = col.find_one({'pdbID': pdb_id}, no_cursor_timeout=True)
    if pdb_data != None:
      result_zip = pdb_data[str(resolution) + "A_G"]
      js_graph = json_unzip(result_zip)
      graph = json_graph.node_link_graph(js_graph)
      for j in graph.nodes():
        graph.nodes[j]["zd_descriptors"] = np.array(graph.nodes[j]["zd_descriptors"])
      return graph

    else:
      insert_pdb_information(col, pdb_id)
      return get_graph_pdb_db(pdb_id, resolution)

  else:
    path_dir = gen_dir()
    download_pdb(pdb_id, '{0}/{1}.pdb'.format(path_dir, pdb_id))
    chains = get_chains_pdb('{0}/{1}.pdb'.format(path_dir, pdb_id))
    graph = gen_graph_resolution_aux(chains, resolution, path_dir, pdb_id)
    free_dir(path_dir)
    return graph


def get_zd_pdb_db(pdb_id, resolution):
  if resolution not in valid_resolutions:
    raise TypeError("Resolution is not valid, you can use: {0}".format(valid_resolutions))

  pdb_id = pdb_id.lower()
  if exists_mongo_db():
    client = get_mongo_client()
    db = client[database_name]
    col = db[collection_name]
    pdb_data = col.find_one({'pdbID': pdb_id}, no_cursor_timeout=True)
    if pdb_data != None:
      result_zip = pdb_data[str(resolution) + "A_OZD"]
      js_zd = json_unzip(result_zip)
      list_js = json.loads(js_zd)
      final_result = np.array(list_js)
      return final_result

    else:
      insert_pdb_information(col, pdb_id)
      return get_zd_pdb_db(pdb_id, resolution)

  else:
    result = gen_zd_resolution_aux(resolution, pdb_id)
    return result


def get_zd_chains_pdb_db(pdb_id, resolution):
  if resolution not in valid_resolutions:
    raise TypeError("Resolution is not valid, you can use: {0}".format(valid_resolutions))

  pdb_id = pdb_id.lower()
  if exists_mongo_db():
    client = get_mongo_client()
    db = client[database_name]
    col = db[collection_name]
    pdb_data = col.find_one({'pdbID': pdb_id}, no_cursor_timeout=True)
    if pdb_data != None:
      result_zip = pdb_data[str(resolution) + "A_G"]
      js_graph = json_unzip(result_zip)
      graph = json_graph.node_link_graph(js_graph)
      final_result = []
      for j in graph.nodes():
        final_result.append([pdb_data["chains"][j - 1], np.array(graph.nodes[j]["zd_descriptors"])])
      return final_result

    else:
      insert_pdb_information(col, pdb_id)
      return get_zd_chains_pdb_db(pdb_id, resolution)

  else:
    result = gen_zd_chain_resolution_aux(resolution, pdb_id)
    return result


def get_chain_to_number_chain(pdb_id, chain):
  pdb_id = pdb_id.lower()
  if exists_mongo_db():
    client = get_mongo_client()
    db = client[database_name]
    col = db[collection_name]
    pdb_data = col.find_one({'pdbID': pdb_id}, no_cursor_timeout=True)
    if pdb_data != None:
      return pdb_data["chains"].index(chain)+1


def get_zd_chain_pdb_db(pdb_id, chain, resolution):
  if resolution not in valid_resolutions:
    raise TypeError("Resolution is not valid, you can use: {0}".format(valid_resolutions))

  pdb_id = pdb_id.lower()
  if exists_mongo_db():
    client = get_mongo_client()
    db = client[database_name]
    col = db[collection_name]
    pdb_data = col.find_one({'pdbID': pdb_id}, no_cursor_timeout=True)
    if pdb_data != None:
      result_zip = pdb_data[str(resolution) + "A_G"]
      js_graph = json_unzip(result_zip)
      graph = json_graph.node_link_graph(js_graph)
      final_result = []
      for j in graph.nodes():
        final_result.append([pdb_data["chains"][j - 1], np.array(graph.nodes[j]["zd_descriptors"])])
      for k in final_result:
        if k[0] == chain:
          return k[1]

    else:
      insert_pdb_information(col, pdb_id)
      return get_zd_chains_pdb_db(pdb_id, resolution)

  else:
    result = gen_zd_chain_resolution_one_chain_aux(resolution, pdb_id, chain)
    return result


def get_chains_pdb_db(pdb_id):
  pdb_id = pdb_id.lower()
  if exists_mongo_db():
    client = get_mongo_client()
    db = client[database_name]
    col = db[collection_name]
    pdb_data = col.find_one({'pdbID': pdb_id}, no_cursor_timeout=True)
    if pdb_data != None:
      return pdb_data["chains"]

    else:
      insert_pdb_information(col, pdb_id)
      return get_chains_pdb_db(pdb_id)

  else:
    path_dir = gen_dir()
    download_pdb(pdb_id, '{0}/{1}.pdb'.format(path_dir, pdb_id))
    chains = get_chains_pdb('{0}/{1}.pdb'.format(path_dir, pdb_id))
    free_dir(path_dir)
    return chains


def insert_pdb_information(col, pdb_id):
  path_dir = gen_dir()
  download_pdb(pdb_id, '{0}/{1}.pdb'.format(path_dir, pdb_id))
  chains = get_chains_pdb('{0}/{1}.pdb'.format(path_dir, pdb_id))
  new_pdb = {}
  # new_pdb['pdbID'] = pdb_id
  new_pdb['chains'] = chains
  for i in [4, 6, 8, 10]:
    graph, father_ZD = gen_graph_resolution_aux(chains, i, path_dir, pdb_id, True)
    for j in graph.nodes():
      graph.nodes[j]["zd_descriptors"] = graph.nodes[j]["zd_descriptors"].tolist()
    g_json = json_graph.node_link_data(graph)
    new_pdb[str(i) + "A_G"] = json_zip(g_json)
    new_pdb[str(i) + "A_OZD"] = json_zip(json.dumps(father_ZD.tolist()))

  col.update_one(
    {"pdbID": pdb_id},
    {"$setOnInsert": new_pdb},
    True
  )

  free_dir(path_dir)


def gen_graph_resolution_aux(chains, resolution, path_dir, pdb_id, return_OZD=False):
  pdb_to_mrc_chains(return_OZD, False, resolution, '{0}/{1}.pdb'.format(path_dir, pdb_id), path_dir, chains,
                    len(chains))
  local_path = path_dir + "/" + pdb_id
  con_id_segment = 1
  segments = []
  for chain in chains:
    segments_graph_simulate, _ = get_mrc_one('{0}/{1}_{2}.mrc'.format(local_path, pdb_id, chain))
    segment = segments_graph_simulate[0]
    segment.id_segment = con_id_segment
    # segment.id_segment = chain
    segments.append(segment)
    con_id_segment += 1
  graph = generate_graph(segments, 100, 0, 6, 1)
  if return_OZD:
    father_ZD = get_mrc_one('{0}/{1}.mrc'.format(local_path, pdb_id))[1].zd_descriptors
    free_dir(local_path)
    return graph, father_ZD
  else:
    free_dir(local_path)
    return graph


def gen_zd_chain_resolution_aux(resolution, pdb_id):
  path_dir = gen_dir()
  download_pdb(pdb_id, '{0}/{1}.pdb'.format(path_dir, pdb_id))
  chains = get_chains_pdb('{0}/{1}.pdb'.format(path_dir, pdb_id))

  pdb_to_mrc_chains(False, False, resolution, '{0}/{1}.pdb'.format(path_dir, pdb_id), path_dir, chains,
                    len(chains))
  local_path = path_dir + "/" + pdb_id
  result = []
  for chain in chains:
    segments_graph_simulate, _ = get_mrc_one('{0}/{1}_{2}.mrc'.format(local_path, pdb_id, chain))
    segment = segments_graph_simulate[0]
    result.append([chain, segment.zd_descriptors])

  free_dir(path_dir)
  return result


def gen_zd_chain_resolution_one_chain_aux(resolution, pdb_id, chain):
  path_dir = gen_dir()
  download_pdb(pdb_id, '{0}/{1}.pdb'.format(path_dir, pdb_id))
  chains = get_chains_pdb('{0}/{1}.pdb'.format(path_dir, pdb_id))

  pdb_to_mrc_chains(False, False, resolution, '{0}/{1}.pdb'.format(path_dir, pdb_id), path_dir, chains,
                    len(chains))
  local_path = path_dir + "/" + pdb_id
  result = []

  segments_graph_simulate, _ = get_mrc_one('{0}/{1}_{2}.mrc'.format(local_path, pdb_id, chain))
  segment = segments_graph_simulate[0]
  result.append([chain, segment.zd_descriptors])

  free_dir(path_dir)
  return result


def gen_zd_resolution_aux(resolution, pdb_id):
  path_dir = gen_dir()
  download_pdb(pdb_id, '{0}/{1}.pdb'.format(path_dir, pdb_id))
  pdb_to_mrc_chains(True, False, resolution, '{0}/{1}.pdb'.format(path_dir, pdb_id), path_dir)
  local_path = path_dir + "/" + pdb_id
  father_ZD = get_mrc_one('{0}/{1}.mrc'.format(local_path, pdb_id))[1].zd_descriptors
  free_dir(path_dir)
  return father_ZD


def get_all_archive_pdb():
  if exists_mongo_db():
    client = get_mongo_client()
    db = client[database_name]
    col = db[collection_name]
    pdbs_data = col.find(no_cursor_timeout=True)
    if pdbs_data.count() == 0:
      return []
    result = []
    for i in pdbs_data:
      result.append(i['pdbID'])
    return result

  else:
    return []


def clear_collection():
  if exists_mongo_db():
    client = get_mongo_client()
    db = client[database_name]
    col = db[collection_name]
    col.drop()


def save_collection(export_json_path):
  if os.path.exists(export_json_path):
    os.remove(export_json_path)

  if exists_mongo_db():
    client = get_mongo_client()
    db = client[database_name]
    col = db[collection_name]
    cursor = col.find({}, no_cursor_timeout=True)
    with open(export_json_path, 'w') as file:
      file.write('[')

      flag_1 = True
      for document in cursor:
        if not flag_1:
          file.write(',')
        else:
          flag_1 = False
        file.write(dumps(document))
      file.write(']')


def load_collection(json_path):
  if exists_mongo_db():
    client = get_mongo_client()
    db = client[database_name]
    col = db[collection_name]
    with open(json_path) as f:
      file_data = json.load(f)
      if isinstance(file_data, list):
        for add_pdb in file_data:
          add_pdb.pop("_id")
          col.update_one(
            {"pdbID": add_pdb["pdbID"]},
            {"$setOnInsert": add_pdb},
            True
          )
      else:
        file_data.pop("_id")
        col.update_one(
          {"pdbID": file_data["pdbID"]},
          {"$setOnInsert": file_data},
          True
        )


def memory_use():
  if exists_mongo_db():
    client = get_mongo_client()
    db = client[database_name]
    result = db.command("collstats", collection_name)
    final_size = result["totalIndexSize"] + result["storageSize"]
    return final_size / (1024 * 1024)
  return 0

# client = get_mongo_client()
# Issue the serverStatus command and print the results
# serverStatusResult = db.command("serverStatus")
# pprint(serverStatusResult)
# print(exists_mongo_db())
# print(exists_mongo_db())
# graph = get_graph_pdb_db('100d', 4)
# result = get_zd_chains_pdb_db('100d', '2')
# result2 = get_zd_pdb_db('100d', 4)
# print(result2)
#
#
# print(get_chains_pdb_db('100d'))
# print(get_all_archive_pdb())
