import os

import xml.etree.ElementTree as ET
import logging

from extra_test_information import extra_javafile_information
from spc.SPCsManager import load_configs
from util.FileManager import list_dir, join_path, get_model_configs_report_path
import pandas as pd

from util.TestingCoverageManager import statement_coverage_of_variants

system_name = "BankAccountTP"
buggy_systems_folder = "/home/whn/Desktop/Email-FH-JML/4wise-Email-FH-JML-2BUG-Full"
#buggy_systems_folder = "/home/whn/Desktop/BankAccountTP/4wise-BankAccountTP-1BUG-Full"
#Test_data = "/home/whn/Desktop/Test_data"
original_production_src_path = "/home/whn/Desktop/OriginalSystem/Email-FH-JML/4wise-Email-FH-JML-Original/4wise-Email-FH-JML/variants"

num_of_bugs = 0
filtering_coverage_rate = 0.1
mutated_projects = list_dir(buggy_systems_folder)
production_dir = list_dir(original_production_src_path)
print(production_dir)
for mutated_project_name in mutated_projects:    #for each bug version
    num_of_bugs += 1
    mutated_project_dir = join_path(buggy_systems_folder, mutated_project_name)

    #get config.report.csv
    config_report_path = get_model_configs_report_path(mutated_project_dir)
    variants_testing_coverage = statement_coverage_of_variants(mutated_project_dir)  # 被测试变异项目的覆盖率，返回的为一个数组
    feature_names, variant_names, passed_configs, failed_configs, failed_variant_names = load_configs(config_report_path,
                                                                                variants_testing_coverage,
                                                                                filtering_coverage_rate)

    tt = True
    #for each production
    sps_funs = {}

    for config in failed_variant_names:
        out = []
        print(type(config), config)
        # test data
        current_original_production_path = join_path(original_production_src_path, config)
        current_original_production_src_path = join_path(current_original_production_path, "test/EmailSystem")
        # failed coverage xml
        current_coverage_dir_path = join_path(mutated_project_dir, "variants")
        current_coverage_dir2_path = join_path(current_coverage_dir_path, config)
        current_coverage_dir3_path = join_path(current_coverage_dir2_path, "coverage")
        current_coverage_file_path = join_path(current_coverage_dir3_path, "failed")
        current_coverage_file_list = list_dir(current_coverage_file_path)   #each coverage file
        failed_test_no = {}


        first_test = True

        for cf in current_coverage_file_list:
            s_cf = cf.split(".")
            no = s_cf[2]#.split("test")[1]
            #test_class_name = s_cf[1]
            failed_test_no[s_cf[1]] = no
            test_file = s_cf[1] + ".java"
            file_path = join_path(current_original_production_src_path, test_file)
            #extra_no_test_information

            variable_set = {}  # bianliang
            method_invocation_set = {}
            funs = []
            variable_set, method_invocation_set, funs = extra_javafile_information(file_path, no, variable_set, method_invocation_set, funs)
            print("funs:", config, funs)

            test_ver_set_hash = {}
            # for tv in test_ver_set:
            #     tv_tem = tv.split('-')
            #     if tv_tem[0] == "assertFalse" or tv_tem[0] == "assertTrue":
            #         test_ver_set_hash[tv_tem[1].split('.')[1]] = tv_tem[0]

            for fun in method_invocation_set.keys():
                sps_method = method_invocation_set.get(fun)
                if method_invocation_set.get(fun) not in sps_funs.keys():
                    sps_funs[sps_method] = 1
                    #first_test = False
                else:
                    #if first_test:
                    sps_funs[sps_method] = sps_funs[sps_method] + 1
            class_method_tem = {}

            for class_and_value in method_invocation_set.values():
                ttemp = class_and_value.split('.')
                method_tem = []
                if ttemp[0] in class_method_tem.keys():
                    method_tem = class_method_tem.get(ttemp[0])
                method_tem.append(ttemp[1])
                class_method_tem[ttemp[0]] = method_tem


            # print("current result is:", class_creat, array_creat, variable_set, method_invocation_set, test_ver_set)
            # print("*******************************************")
            # file_path = join_path(current_test_path, s_cf[1] + ".csv")
            # test_csv_df = pd.read_csv(file_path)
            # #get bug test
            # if len(no) >= 2 and no[0] == '0':
            #     no = no[1:]
            # series = test_csv_df.loc[int(no)]   #Series
            # sf = series["fun"].split(".")
            # test_class_name = sf[0]
            # test_fun_name = sf[1]

            # #read coverage file
            coverage_file = join_path(current_coverage_file_path, cf)
            # if os.path.isfile(coverage_file):
            #     data[variant] = []

            # read
            # try:
            #     tree = ET.parse(coverage_file)
            #     root = tree.getroot()
            #     project = root.find("project")
            #     package = project.find("package")
            #     files = package.find("file")
            #     #lines = files.find("line")
            #     #for package in project:
            #     #print("ddddd", files.attrib.items())
            #     for cl_tem in class_method_tem.keys():
            #         for key1, value1 in files.attrib.items():
            #             tem = value1.split('.')[0]
            #             #print("tem:", tem)
            #
            #             if tem == cl_tem:
            #                 #print("current:", key1, value1)
            #                 methods_tem = list(test_ver_set_hash.keys())[0]
            #                 #print("methods_tem", methods_tem)
            #                 start = False
            #                 for line in files:
            #                     if line.tag == "line":
            #                         if line.attrib.get("signature") != None:
            #                             hn = line.attrib.get("signature").split('(')
            #                             if len(hn) > 0 and hn[0] in methods_tem:
            #                                 # print(hn[0], type(line.attrib), line.attrib.get("count"),
            #                                 #       type(line.attrib.get("count")))
            #                                 start = True
            #                                 out.append(hn[0])
            #                             else:
            #                                 start = False
            #
            #                         if line.attrib.get("truecount") == 1 and start:
            #                             out.append(line.attrib.get("num"))
            #                         if line.attrib.get("count") == "1" and start:
            #                             out.append(line.attrib.get("num"))
            #                         # for key, value in line.attrib.items():
            #                         #     # print("key", key)
            #                         #     # print("value", value)
            #                         #     hn = value.split('(')
            #                         #     if key == "signature" and len(hn) > 0 and hn[0] in methods_tem:
            #                         #         print(key, hn[0], type(line.attrib))
            #                         #         start = True
            #                         #     if key == "truecount" and start:
            #                         #         if value == "1":
            #                         #             out.append()
            #                                 #search the sps stataments
            #                                 #ver_type = test_ver_set_hash.get(hn[0])
            #                                 #if ver_type == ""
            #
            #                             #pass
            #                 break
            #
            #
            #         # id = line.get('num') + line.get('count') + line.get('type')
            #         # print("id :", line)
            #         #for line in file:
            #             #id = line.get('num') + line.get('count') + line.get('type')
            #             #print("id :", line)
            #             #pass
            # except:
            #     logging.info("Exception when parsing %s", coverage_file)



        # key_failed_test_no = list(failed_test_no.keys())
        # for file in key_failed_test_no:
        #     file_path = join_path(current_test_path, file + ".csv")
        #     test_csv = pd.read_csv(file_path)
        #     print(test_csv)

        # print("out", config, out)
        print("----------------------------------------------")
        print("----------------------------------------------")

    lis = sorted(sps_funs.items(), key=lambda x: x[1], reverse=True)
    print(mutated_project_name, lis)
    # for each_sfun in sps_funs.keys():
    #     class_and_fun = each_sfun.split(".")




