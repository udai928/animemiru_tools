# coning:utf-8

import yaml
import sys

def load_config(env):
    if(env == "prod"):
        CONFIG_DIR = "../config/"
    else:
        CONFIG_DIR = "/Users/kuzuyayuudai/GoogleDrive/development/Animemiru/animemiru_tools/config/"
    f = open(CONFIG_DIR + "config.yaml",'r')
    configs = yaml.load(f)
    f.close()
    return configs[env]
