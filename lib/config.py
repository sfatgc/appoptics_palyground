import yaml
def load_config_file(asFileName):
    with open(asFileName, "r") as oFile:
        return yaml.load(oFile)
