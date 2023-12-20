from typing import List

class Context():
  
    def __init__(self,AttributeName,Attribute,Condition,ValueRange):
        self.__name=AttributeName
        self.__attribute=Attribute
        self.__condition=Condition
        self.__value_range=ValueRange
    def __str__(self):
        return f"Context(name={self.__name}, attribute={self.__attribute}, condition={self.__condition}, value_range={self.__value_range})"
    
class Target():

    def __init__(self,AttributeName,Attribute,Condition,ValueRange,Context : Context):
        self.__name=AttributeName
        self.__attribute=Attribute
        self.__condition=Condition
        self.__value_range=ValueRange
        self.__context=Context
    def __str__(self):
        return f"Target(name={self.__name}, attribute={self.__attribute}, condition={self.__condition}, value_range={self.__value_range}, context={self.__context})"

class Expectation():

    def __init__(self, intent_type : str,target : Target, context : Context):
        self.__target=target
        self.__context=context
        self.__intent_type=intent_type
    def __str__(self):
        return f"Expectation(intent_type={self.__intent_type}, target={self.__target}, context={self.__context})"

class IB_object():
    def __init__(self, intent_dict: dict):

        intent=intent_dict["Intent"]
        self.__name=intent["AttributeName"]
        self.__context = intent["Context"]
        self.__expectations: List[Expectation] = []
        for expectation_data in intent['Expectations']:
            print("\n",expectation_data)
            context_data = expectation_data["Contexts"]
            target_data = expectation_data["Target"]
            if context_data and target_data:
                print("\n Context",context_data)
                context_obj = Context(**context_data)
                target_obj = Target(**target_data)
                expectation_obj = Expectation(
                    intent_type=expectation_data.get('intent_type'),
                    target=target_obj,
                    context=context_obj
                )
                self.__expectations.append(expectation_obj)
    def __str__(self):
        expecs=[exp.__str__() for exp in self.__expectations]
        return f"IB_object(context={self.__context},{expecs})"