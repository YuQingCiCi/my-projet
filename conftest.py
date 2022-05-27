import osfrom json_handler import json_get, jsonFile_getfrom utility import attr_dictdef merge_dicts(d1, d2):    '''合并两个dict对象,如果子节点也是dict,同样会被合并'''    common_keys = set(d1.keys()) & set(d2.keys())    for k in common_keys:        if isinstance(d1[k], dict) and isinstance(d2[k], dict):            d2[k] = merge_dicts(d1[k], d2[k])    d1.update(d2)    return d1def get_input_data(self):    all_test_data = self.get_testdata()    json_path_for_input = "$..input_values"    return json_get(all_test_data, json_path_for_input) or all_test_datadef get_test_data(test_data_path, test_case_name):    expr_with_test_case = "$..%s" % test_case_name    test_data = jsonFile_get(test_data_path, expr_with_test_case)    return test_datadef get_all_data(test_data_path):    expr_with_test_case = "$"    test_data = jsonFile_get(test_data_path, expr_with_test_case)    return test_datadef pytest_generate_tests(metafunc):    # generate each test cases with keywords and data driven pattern    test_module_path = metafunc.module.__file__    function_name = metafunc.function.__name__    test_data_path = test_module_path.replace("test_cases", "test_data").replace(".py", ".json")    # 若不存在相同目录层级的json文件，则找test_data目录下的该同名文件    if not os.path.exists(test_data_path):        child_path = test_module_path.split('/', -1)[-1].replace(".py", ".json")        test_data_path = test_module_path.split("test_cases")[0] + "test_data/" + child_path    all_data = get_all_data(test_data_path)    if all_data:        default_data = [d for d in all_data if "test_" not in d]        for item in default_data:            # only set data for per class once            if not hasattr(metafunc.cls, item):                setattr(metafunc.cls, item, attr_dict(all_data[item]) if all_data[item] else None)    test_data = get_test_data(test_data_path, function_name)    if test_data:        test_data = [attr_dict(d) for d in test_data]        metafunc.parametrize("data", test_data)