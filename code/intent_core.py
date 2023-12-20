import translator
import ib_object
import importer
import yamlParser

if __name__ == "__main__":

    data=yamlParser.yaml_to_data("input.yaml")
    print(data)
    intent=ib_object.IB_object(data)
    print(intent)