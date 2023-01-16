import pymongo
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import logging
import sys
from constants.enum import OracleType
from os.path import join
from utils.converter import str_to_bool
import tensorflow as tf
from classes.tf_library import TFLibrary
from classes.tf_api import TFAPI
from classes.database import TorchDatabase, TFDatabase
import re
import copy
import os
import random

logging.basicConfig(level=logging.INFO)
myclient = pymongo.MongoClient("mongodb://localhost:27017/")


def read_txt(fname):
    with open(fname, "r") as fileReader:
        data = fileReader.read().splitlines()
    return data


def check_connection():
    client = MongoClient(
        "mongodb://localhost:27017/", serverSelectionTimeoutMS=10, connectTimeoutMS=300
    )

    try:
        info = client.server_info()

    except ServerSelectionTimeoutError:
        logging.info(
            "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
        )
        logging.info(
            "#### MongoDB Server is Down! I am trying initiating the server now. ####"
        )
        logging.info(
            "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
        )


def make_api_name_unique(api):
    api_split = api.split("tensorflow")
    new_api_name = "tensorflow" + api_split[-1]
    return new_api_name


def count_tensor_inputs(api, lib="Tensorflow"):
    tensor_holder = []
    integer_holder = []
    for arg in api.args:
        _arg = api.args[arg]

        if lib == "Tensorflow":
            if re.findall(r"(ArgType\.TF\_TENSOR\:)", repr(_arg.type)):
                tensor_holder.append(1)
            if re.findall(r"ArgType\.INT\:", repr(_arg.type)):
                integer_holder.append(1)
        else:
            if re.findall("r(ArgType\.TORCH\_TENSOR\:)", repr(_arg.type)):
                tensor_holder.append(1)
    return tensor_holder


if __name__ == "__main__":
    library = sys.argv[1]
    api_name = sys.argv[2]
    index = sys.argv[3]
    tool_name = sys.argv[4]
    output_dir = sys.argv[5]

    # output_dir = "/media/nimashiri/SSD/testing_results"
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    rules = [
        "MUTATE_PREEMPTIVES",
        "NEGATE_INT_TENSOR",
        "RANK_REDUCTION_EXPANSION",
        "EMPTY_TENSOR_TYPE1",
        "EMPTY_TENSOR_TYPE2",
        "EMPTY_LIST",
        "ZERO_TENSOR_TYPE1",
        "ZERO_TENSOR_TYPE2",
        "NAN_TENSOR",
        "NAN_TENSOR_WHOLE",
        "NON_SCALAR_INPUT",
        "SCALAR_INPUT",
        "LARGE_TENSOR_TYPE1",
        "LARGE_TENSOR_TYPE2",
        "LARGE_LIST_ELEMENT",
    ]

    if library == "tf":

        MyTF = TFLibrary(output_dir)
        TFDatabase.database_config("localhost", 27017, "TF")
        dimension_mismatch = True

        try:
            for k in range(5):
                # api = TFAPI(api_name)
                # old_api = copy.deepcopy(api)

                api_keywords = api_name.split(".")
                if api_keywords.count("tensorflow") > 1:
                    api_name = make_api_name_unique(api_name)

                api = TFAPI(api_name)
                for c1 in range(1000):

                    print(
                        "########################################################################################################################"
                    )
                    print(
                        "Running {0} on the current API under test: {1}/Index: {2}. Working on dimension mismatch, Iteration_L1 {3}, Iteration_L2 {4}".format(
                            tool_name, api_name, index, k, c1
                        )
                    )
                    print(
                        "########################################################################################################################"
                    )
                    api.new_mutate_tf()

                    MyTF.test_with_oracle(api, OracleType.CRASH)
                    api.api = api_name

                    MyTF.test_with_oracle(api, OracleType.CUDA)
                    api.api = api_name
        except Exception as e:
            print(e)

        try:

            for k in range(1):

                api_keywords = api_name.split(".")
                if api_keywords.count("tensorflow") > 1:
                    api_name = make_api_name_unique(api_name)

                for c2 in range(1000):
                    old_api = TFAPI(api_name)
                    for i, arg in enumerate(old_api.args):
                        for r in rules:
                            print(
                                "########################################################################################################################"
                            )
                            print(
                                "Running {0} on the current API under test: ###{1}###. Index: {2} Mutating the parameter ###{3}### using the rule ###{4}###, Iteration: {5}".format(
                                    tool_name, api_name, index, arg, r, c2
                                )
                            )
                            print(
                                "########################################################################################################################"
                            )
                            old_arg = copy.deepcopy(old_api.args[arg])
                            old_api.new_mutate_multiple(old_api.args[arg], r)
                            MyTF.test_with_oracle(old_api, OracleType.CRASH)
                            old_api.api = api_name
                            MyTF.test_with_oracle(old_api, OracleType.CUDA)
                            old_api.api = api_name
                            old_api.args[arg] = old_arg
        except Exception as e:
            pass
    else:
        from classes.torch_library import TorchLibrary
        from classes.torch_api import TorchAPI
        from classes.database import TorchDatabase

        TorchDatabase.database_config("localhost", 27017, "Torch-Unique")

        MyTorch = TorchLibrary(output_dir)

        try:
            for k in range(1):
                api = TorchAPI(api_name)
                for c1 in range(1000):

                    print(
                        "########################################################################################################################"
                    )
                    print(
                        "Running {0} on the current API under test: {1}/Index: {2}. Working on dimension mismatch, Iteration_L1 {3}, Iteration_L2 {4}".format(
                            tool_name, api_name, index, k, c1
                        )
                    )
                    print(
                        "########################################################################################################################"
                    )
                    api.new_mutate_torch()

                    MyTorch.test_with_oracle(api, OracleType.CRASH)
                    MyTorch.test_with_oracle(api, OracleType.CUDA)
        except Exception as e:
            print(e)

        try:

            for k in range(1):
                for c1 in range(1000):
                    api = TorchAPI(api_name)
                    num_arg = len(api.args)
                    num_Mutation = random.randint(1, num_arg + 1)
                    for _ in range(num_Mutation):
                        arg_name = random.choice(list(api.args.keys()))
                        arg = api.args[arg_name]
                        for r in rules:

                            print(
                                "########################################################################################################################"
                            )
                            print(
                                "Running {0} on the API under test: ###{1}###/{2}. Mutating the parameter ###{3}### using the rule ###{4}### Index1 {5} Index2 {6}".format(
                                    tool_name, api_name, index, arg_name, r, k, c1
                                )
                            )
                            print(
                                "########################################################################################################################"
                            )
                            # old_arg = copy.deepcopy(api.args[arg])
                            api.new_mutate_multiple(arg, r)
                            MyTorch.test_with_oracle(api, OracleType.CRASH)
                            MyTorch.test_with_oracle(api, OracleType.CUDA)
        except Exception as e:
            print(e)
