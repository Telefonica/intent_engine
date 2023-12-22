import translator
import ib_object
import importer
import yamlParser
import os


if __name__ == "__main__":

    # cwd = os.getcwd()
    # os.chdir(cwd)
    data=yamlParser.yaml_to_data("input.yaml")
    # print(data)
    intent=ib_object.IB_object(data)
    print(intent)
    # ------- Intent translator -------
    