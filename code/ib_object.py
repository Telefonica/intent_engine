from typing import List

class Context():
  
    def __init__(self,AttributeName,Attribute,Condition,ValueRange):
        self.__name=AttributeName
        self.__attribute=Attribute
        self.__condition=Condition
        self.__value_range=ValueRange
    def __str__(self):
        return f"Context(name={self.__name}, attribute={self.__attribute}, condition={self.__condition}, value_range={self.__value_range})"
    
    def get_keywords(self):
        keywords= []
        keywords.append(self.__name)
        keywords.append(self.__attribute)
        keywords.append(self.__condition)
        keywords.append(self.__value_range)
        return keywords
    
    def set_name(self, name):
        self.__name = name

    def set_attribute(self, attribute):
        self.__attribute = attribute

    def set_condition(self, condition):
        self.__condition = condition

    def set_value_range(self, value_range):
        self.__value_range = value_range

    def get_name(self):
        return self.__name

    def get_attribute(self):
        return self.__attribute

    def get_condition(self):
        return self.__condition

    def get_value_range(self):
        return self.__value_range

class Target():

    def __init__(self,AttributeName,Attribute,Condition,ValueRange,Context : Context):
        self.__name=AttributeName
        self.__attribute=Attribute
        self.__condition=Condition
        self.__value_range=ValueRange
        self.__context=Context
    def __str__(self):
        return f"Target(name={self.__name}, attribute={self.__attribute}, condition={self.__condition}, value_range={self.__value_range}, context={self.__context})"
    def get_keywords(self):
        keywords= []
        keywords.append(self.__name)
        keywords.append(self.__attribute)
        keywords.append(self.__condition)
        keywords.append(self.__value_range)
        if self.__context :
            keywords.append(self.__context.get_keywords())
        return keywords
    
    def set_name(self, name):
        self.__name = name

    def set_attribute(self, attribute):
        self.__attribute = attribute

    def set_condition(self, condition):
        self.__condition = condition

    def set_value_range(self, value_range):
        self.__value_range = value_range

    def set_context(self, context : Context):
        self.__context = context

    def get_name(self):
        return self.__name

    def get_attribute(self):
        return self.__attribute

    def get_condition(self):
        return self.__condition

    def get_value_range(self):
        return self.__value_range

    def get_context(self):
        return self.__context
    
class Expectation():

    def __init__(self, intent_type : str,target : List [Target], context : List[Context]):
        self.__target=target
        self.__context=context
        self.__intent_type=intent_type
    def __str__(self):
        context=[ctx.__str__() for ctx in self.__context]
        target=[trg.__str__() for trg in self.__target]
        return f"Expectation(intent_type={self.__intent_type}, target={target}, contexts={context})"
    def get_keywords(self):
        
        # print("context getkeywords expectations",flat_list)
        keywords= []
        keywords.append(self.__intent_type)

        target=[trg.get_keywords() for trg in self.__target]
        flat_list_trg = [x for xs in target for x in xs]
        for words in flat_list_trg:
            keywords.append(words)
        print("__target getkeywords expectations",keywords)
        context=[ctx.get_keywords() for ctx in self.__context]
        flat_list_ctx = [x for xs in context for x in xs]
        for words in flat_list_ctx:
            keywords.append(words)
        # print("flat_list getkeywords expectations",flat_list)
        return keywords
    
    def set_intent_type(self, intent_type):
        self.__intent_type = intent_type

    def set_target(self, target : Target):
        self.__target = target

    def set_context(self, context : Context):
        self.__context = context
    
    def get_intent_type(self):
        return self.__intent_type

    def get_target(self):
        return self.__target

    def get_context(self):
        return self.__context

class IB_object():
    def __init__(self, intent_dict: dict):

        intent=intent_dict["Intent"]
        self.__name=intent["AttributeName"]
        # Fixme context clase context/ lista de contexts
        self.__context = Context(**intent["Context"])
        self.__expectations: List[Expectation] = []
        for expectation_data in intent['Expectations']:
            # print("\n --expecs--",expectation_data)
            # context_data = expectation_data["Contexts"]
            context_data_list = expectation_data.get("Contexts", [])
            target_data_list = expectation_data["Target"]
            # print("\n --Context list-- ",context_data_list)
            if context_data_list and target_data_list:
                context_obj=[]
                for context_data in context_data_list:
                    # print("\n --Context-- ",context_data)
                    context_obj.append(Context(**context_data))
                # Fixme target lista de targets
                target_obj = []
                for target_data in target_data_list:
                    # print("\n --Context-- ",context_data)
                    target_obj.append(Target(**target_data))

                expectation_obj = Expectation(
                    intent_type=expectation_data.get('Type'),
                    target=target_obj,
                    context=context_obj
                )
                self.__expectations.append(expectation_obj)
    def __str__(self):
        expecs=[exp.__str__() for exp in self.__expectations]
        return f"IB_object(name={self.__name},context={self.__context},{expecs})"
    
    def get_keywords(self):
        expecs=[exp.get_keywords() for exp in self.__expectations]
        # print("expecs getkeywords ib_object",expecs)
        flat_list = [x for xs in expecs for x in xs]
        # print("flat_list getkeywords ib_object",flat_list)
        keywords= []
        keywords.append(self.__name)
        if self.__context:
            for words in self.__context.get_keywords():
                keywords.append(words)
        for words in flat_list:
                keywords.append(words)
        print("keywords: ",keywords)
        return keywords
    
    def set_name(self, name):
        self.__name = name

    def set_context(self, context):
        self.__context = context

    def set_expectations(self, expectations):
        self.__expectations = expectations
    
    def get_name(self):
        return self.__name

    def get_context(self):
        return self.__context

    def get_expectations(self):
        return self.__expectations