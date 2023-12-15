import math
import os

import numpy as np
import pandas as pd

from dsEvfusion import fusion, softmax, mul_evd_fusion
from extra_test_information import extra_javafile_information
from get_fail_coverage_information import get_each_failed_test_coverage_inf
from methods.mutual_information import su_calculation
from util.FileManager import join_path, list_dir
import json



def get_Evidence1(variants_list, product_with_roles, config_report_csv, variants_list_path, times):
    each_x_number = {}
    each_x_pass = {}
    each_x_fail = {}
    product_len = 0
    pass_pro = 0
    fail_pro = 0
    sps_funs_keys = []
    funstion_role_csv = []
    result_list = []

    for product in variants_list:
        product_name = join_path(variants_list_path, product)

        src_path = join_path(product_name, "src")
        src_files_and_dir = list_dir(src_path)
        for fd in src_files_and_dir:
            fd_path = join_path(src_path, fd)
            if os.path.isfile(fd_path):
                fd_name = fd.split(".")[0]
                if fd_name not in sps_funs_keys:
                    sps_funs_keys.append(fd_name)
            elif os.path.isdir(fd_path):
                fd_files = list_dir(fd_path)
                for fdf in fd_files:
                    fdf_path = join_path(fd_path, fdf)
                    if os.path.isfile(fdf_path):
                        fd_name = fdf.split(".")[0]
                        if fd_name not in sps_funs_keys:
                            sps_funs_keys.append(fd_name)

        each_role_funs = []
        mata_file_path = join_path(product_name, "roles.meta")
        mata_file = open(mata_file_path, 'r')
        product_len = product_len + 1
        try:
            all_the_text = mata_file.read()
            metaData = json.loads(all_the_text)
            productRoles = metaData.get("roles")
            ll = list(productRoles.keys())
            if times == 0:
                role_with_feature = {}
                for role in ll:
                    role_with_feature[role] = list(productRoles.get(role).values())
                product_with_roles[product] = role_with_feature
            tem = config_report_csv.loc[config_report_csv['Product\Feature'] == str(product), '__TEST_OUTPUT__'].iloc[0]
            for i in range(0, len(ll)):
                each_role_funs.append(ll[i])
                if ll[i] in each_x_number:
                    each_x_number[ll[i]] = each_x_number[ll[i]] + 1
                else:
                    each_x_number[ll[i]] = 1
                if ll[i] in each_x_pass and tem == "__PASSED__":
                    each_x_pass[ll[i]] = each_x_pass[ll[i]] + 1
                elif ll[i] not in each_x_pass and tem == "__PASSED__":
                    each_x_pass[ll[i]] = 1
                if ll[i] in each_x_fail and tem == "__FAILED__":
                    each_x_fail[ll[i]] = each_x_fail[ll[i]] + 1
                elif ll[i] not in each_x_fail and tem == "__FAILED__":
                    each_x_fail[ll[i]] = 1
            funstion_role_csv.append(each_role_funs)

            if tem in each_x_number:
                each_x_number[tem] = each_x_number[tem] + 1
            else:
                each_x_number[tem] = 1
            if tem == "__PASSED__":
                pass_pro = pass_pro + 1
                result_list.append(1)
            else:
                fail_pro = fail_pro + 1
                result_list.append(0)
        finally:
            mata_file.close()

    pass_pro = pass_pro / product_len
    fail_pro = fail_pro / product_len

    each_x_pro = {}
    each_x_front_pass = {}
    each_x_front_fail = {}

    each_x_rear_pass = {}
    each_x_rear_fail = {}

    for key, value in each_x_number.items():
        if key != "__PASSED__" and key != "__FAILED__":
            each_x_pro[key] = value / product_len
            if key in each_x_pass:
                each_x_front_pass[key] = each_x_pass[key] / value
                each_x_rear_pass[key] = (each_x_front_pass[key] * each_x_pro[key]) / pass_pro
            if key in each_x_fail:
                each_x_front_fail[key] = (each_x_fail[key] / value)
                each_x_rear_fail[key] = 0.5 * ((each_x_front_fail[key] * each_x_pro[key]) / fail_pro) + 0.5 * \
                                        each_x_front_fail[key]
            else:
                each_x_fail[key] = 0

    first_fun_value_front = list(each_x_front_fail.values())[0]
    for key, value in each_x_front_fail.items():
        if value >= 0.6:
            if key not in sps_funs_keys:
                sps_funs_keys.append(key)
    return sps_funs_keys, result_list, funstion_role_csv, product_len, each_x_rear_fail

def get_Evidence2(folder_path, mutated_project_name, variants_list_path):
    config_csv = join_path(folder_path, "config.report.csv")
    config_report_csv = pd.read_csv(config_csv)
    fail_productions = config_report_csv.loc[
        config_report_csv['__TEST_OUTPUT__'] == "__FAILED__", 'Product\Feature'].tolist()

    sps_funs_in_test_file = {}
    total_number = 0
    for production in fail_productions:
        failed_production_path = join_path(variants_list_path, production)
        failed_coverage_path = join_path(failed_production_path, "coverage/failed")
        current_coverage_file_list = list_dir(failed_coverage_path)
        current_original_production_src_path = join_path(failed_production_path, "test/EmailSystem")

        test_src_files = {}
        for cf in current_coverage_file_list:
            s_cf = cf.split(".")
            no = s_cf[-3]
            tem_s_cf = s_cf[0: -3]
            src_file_path = ""
            for st in tem_s_cf:
                src_file_path = src_file_path + "." + str(st)
            if src_file_path not in test_src_files:
                test_src_files[src_file_path] = []
                test_src_files[src_file_path].append(no)
            else:
                test_src_files[src_file_path].append(no)

        for kk, vv in test_src_files.items():
            unit_test_file_path = join_path(failed_production_path, "test")
            sp_path = kk.split(".")
            if len(sp_path) > 1:
                for mm in range(len(sp_path) - 1):
                    unit_test_file_path = join_path(unit_test_file_path, sp_path[mm])
            test_file = sp_path[-1] + ".java"
            file_path = join_path(unit_test_file_path, test_file)
            variable_set, method_invocation_set, funs = extra_javafile_information(file_path, vv, mutated_project_name)
            for each_unit_test_information in funs:
                for ff, value in each_unit_test_information.items():
                    if ff not in sps_funs_in_test_file:
                        total_number += 1
                        sps_funs_in_test_file[ff] = value
                    else:
                        sps_funs_in_test_file[ff] = sps_funs_in_test_file[ff] + value
    return sps_funs_in_test_file, total_number, fail_productions

def uncertain_inference(buggy_systems_folder):
    mutated_projects = list_dir(buggy_systems_folder)
    type_0 = 0
    type_1 = 0
    times = 0
    product_with_roles = {}
    print("***********************************************")
    print("Start calculating the suspiciousness of suspicious blocks and generating suspicious statements!")
    for mutated_project_name in mutated_projects:
        folder_path = join_path(buggy_systems_folder, mutated_project_name)
        config_csv = join_path(folder_path, "config.report.csv")
        config_report_csv = pd.read_csv(config_csv)
        variants_list_path = join_path(folder_path, "variants")
        variants_list = list_dir(variants_list_path)
        sps_funs_keys, result_list, funstion_role_csv, product_len, each_x_rear_fail = get_Evidence1(variants_list, product_with_roles, config_report_csv, variants_list_path, times)

        sps_funs_in_test_file, total_number, fail_productions = get_Evidence2(folder_path, mutated_project_name, variants_list_path)

        classfication_results = {}
        for key, value in each_x_rear_fail.items():
            classfication_results[key] = value
        classfication_results = sorted(classfication_results.items(), key=lambda x: x[1], reverse=True)          #higher value indicates the spc function
        sps_funs = dict(classfication_results)
        for key, value in sps_funs.items():
            if value >= 0.5:
                if key not in sps_funs_keys:
                    sps_funs_keys.append(key)

        for ff, value in sps_funs_in_test_file.items():
            sps_funs_in_test_file[ff] = 1 / total_number

        sps_funs_keys_set = set(sps_funs_keys)
        sps_funs_in_test_file_set = set(sps_funs_in_test_file.keys())
        sps_funs_keys_set_intersection = list(sps_funs_keys_set.union(sps_funs_in_test_file_set))

        arr_sps_funs_keys = []
        arr_sps_funs_in_test_file = []

        su_list = []
        for ff in sps_funs_keys_set_intersection:
            if ff in sps_funs_in_test_file:
                arr_sps_funs_in_test_file.append(sps_funs_in_test_file[ff])
            else:
                arr_sps_funs_in_test_file.append(0)
            if ff in each_x_rear_fail:
                arr_sps_funs_keys.append(each_x_rear_fail[ff])
            else:
                arr_sps_funs_keys.append(0)

            each_fun_su_list = []
            for pi in range(product_len):
                if ff in funstion_role_csv[pi]:
                    each_fun_su_list.append(1)
                else:
                    each_fun_su_list.append(0)
            su_list.append(su_calculation(each_fun_su_list, result_list))

        arr_sps_funs_keys = softmax(arr_sps_funs_keys)

        #Multi-source evidence fusion based on the Dempster Synthesis Rule
        type_fusion, fusion_result = fusion(arr_sps_funs_keys, arr_sps_funs_in_test_file, su_list)

        sps_funs_keys_new = []

        if type_fusion == 0:
            for i in range(0, len(fusion_result)):
                if fusion_result[i] > 0:
                    sps_funs_keys_new.append([sps_funs_keys_set_intersection[i], fusion_result[i]])
            type_0 += 1
        else:
            type_1 += 1
            for i in range(0, len(fusion_result)):
                if fusion_result[i] > 0:
                    sps_funs_keys_new.append([sps_funs_keys_set_intersection[i], fusion_result[i]])
        siling_data = {}
        for production in fail_productions:
            failed_production_path = join_path(variants_list_path, production)
            failed_coverage_path = join_path(failed_production_path, "coverage/failed")
            data = get_each_failed_test_coverage_inf(failed_coverage_path, sps_funs_keys_new, production, product_with_roles)
            if len(list(data.keys())) != 0:
                siling_data[production] = data
        siling_data = json.dumps(siling_data)
        print(mutated_project_name, "is finished!")
        times += 1
        siling_file_path = join_path(folder_path, "slicing_10.log")
        nf = open(siling_file_path, "w")
        try:
            nf.write(siling_data)
        finally:
            nf.close()
    print("***********************************************")