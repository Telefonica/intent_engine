# © 2024 Telefónica Innovación Digital

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import List
import logging
logger = logging.getLogger(__name__)
class Context():
  
    def __init__(self,Attribute,Condition,ValueRange,AttributeName=""):
        self.__name=AttributeName
        self.__attribute=Attribute
        self.__condition=Condition
        self.__value_range=ValueRange
    def __str__(self):
        return f"Context(name={self.__name}, attribute={self.__attribute}, condition={self.__condition}, value_range={self.__value_range})"
    
    def get_dict(self):
        return {
            "AttributeName":self.__name,
            "Attribute":self.__attribute,
            "Condition":self.__condition,
            "ValueRange":self.__value_range
        }
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

    def __init__(self,AttributeName,Attribute,Condition,ValueRange,Contexts : List[Context]=None):
        self.__name=AttributeName
        self.__attribute=Attribute
        self.__condition=Condition
        self.__value_range=ValueRange
        if Contexts:
            self.__context : List[Context]=[Context(**ctx) for ctx in Contexts]
        else: self.__context = None
    def __str__(self):
        if self.__context:
            ctx=[cx.__str__() for cx in self.__context]
            return f"Target(name={self.__name}, attribute={self.__attribute}, condition={self.__condition}, value_range={self.__value_range}, context={ctx})"
        return f"Target(name={self.__name}, attribute={self.__attribute}, condition={self.__condition}, value_range={self.__value_range})"
    
    def get_dict(self):
        return {
            "AttributeName":self.__name,
            "Attribute":self.__attribute,
            "Condition":self.__condition,
            "ValueRange":self.__value_range
        }

    def get_keywords(self):
        keywords= []
        keywords.append(self.__name)
        keywords.append(self.__attribute)
        keywords.append(self.__condition)
        keywords.append(self.__value_range)
        if self.__context :
            for ctx in self.__context:
                keywords.append(ctx.get_keywords())
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

class Object_expectation():
    def __init__(self, Type : str,Instance : str, Contexts : List[Context]):
        self.__type=Type
        self.__instance=Instance
        if Contexts:
            self.__context : List[Context]=[Context(**ctx) for ctx in Contexts]
        else: self.__context = None
    def __str__(self):
        context=[ctx.__str__() for ctx in self.__context]
        return f"Expectation(type={self.__type},instance={self.__instance}, contexts={context})"
    def get_dict(self):
        return {
            "Type":self.__type,
            "Instance":self.__instance,
            "Contexts":[ctx.get_dict() for ctx in self.__context]
        }
    def get_keywords(self):
        # print("context getkeywords expectations",flat_list)
        keywords= []
        keywords.append(self.__type)
        keywords.append(self.__instance)
        context=[ctx.get_keywords() for ctx in self.__context]
        flat_list_ctx = [x for xs in context for x in xs]
        for words in flat_list_ctx:
            keywords.append(words)
        return keywords

    def get_type(self):
        return self.__type
    def set_type(self,otype : str):
        self.__type=otype
    def get_contexts(self):
        return self.__context
    def set_contexts(self,context:Context):
        self.__context=context

class Expectation():

    def __init__(self, verb : str,Targets : List [Target], obj : Object_expectation ,context : List[Context] = None):
    
        if Targets:
            self.__target : List[Target]=Targets
        else:
            self.__target=None
            logger.warning("Intent expectation needs a Target!")
        self.__context=context
        self.__verb=verb
        self.__object=obj
    def __str__(self):
        target=[trg.__str__() for trg in self.__target]
        if self.__context:
            context=[ctx.__str__() for ctx in self.__context]
            return f"Expectation(verb={self.__verb}, target={target},object={self.__object},contexts={context})"
        return f"Expectation(verb={self.__verb},target={target},object={self.__object})"
    def get_dict(self):
        if self.__target:
            return {
                "Verb":self.__verb,
                "Object":self.__object.get_dict(),
                "Contexts":[ctx.get_dict() for ctx in self.__context],
                "Targets":[trg.get_dict() for trg in self.__target]
            }
        return {
                "Verb":self.__verb,
                "Object":self.__object.get_dict(),
                "Contexts":[ctx.get_dict() for ctx in self.__context]
            }
    def get_keywords(self):
        
        # print("context getkeywords expectations",flat_list)
        keywords= []
        keywords.append(self.__verb)
        for words in self.__object.get_keywords():
            keywords.append(words)
        target=[trg.get_keywords() for trg in self.__target]
        flat_list_trg = [x for xs in target for x in xs]
        for words in flat_list_trg:
            keywords.append(words)
        # logger.debug("__target getkeywords expectations %s",keywords)
        context=[ctx.get_keywords() for ctx in self.__context]
        flat_list_ctx = [x for xs in context for x in xs]
        for words in flat_list_ctx:
            keywords.append(words)
        # print("flat_list getkeywords expectations",flat_list)
        return keywords
    
    def set_verb(self, verb):
        self.__verb = verb

    def set_target(self, target : Target):
        self.__target = target

    def set_context(self, context : Context):
        self.__context = context

    def set_object(self, obj : Object_expectation):
        self.__object = obj
    
    def get_object(self):
        return self.__object
    
    def get_verb(self):
        return self.__verb

    def get_target(self):
        return self.__target

    def get_context(self):
        return self.__context

class IB_object():
    def __init__(self, intent_dict: dict = {}):
        self.__expectations: List[Expectation] = []
        self.__context:Context
        self.__name : str
        if not intent_dict:
            return
        intent=intent_dict["Intent"]
        self.__name=intent["AttributeName"]
        # Intent context
        self.__context = Context(**intent["Context"])
        # Intent Expectations
        for expectation_data in intent['Expectations']:
            # print("\n --expecs--",expectation_data)
            # Travers expectations in one intent
            target_data_list=[]
            target_obj = []
            context_obj=[]
            object_data={}
            context_data_list=[]
            # Expectations contexts
            if "Contexts" in expectation_data:
                context_data_list = expectation_data["Contexts"]
                if context_data_list:
                    for context_data in context_data_list:
                        # print("\n --Context-- ",context_data)
                        context_obj.append(Context(**context_data))
            # Expectations targets
            if "Targets" in expectation_data :
                target_data_list = expectation_data["Targets"]
                for target_data in target_data_list:
                    # print("\n --Targets-- ",target_data)
                    target_obj.append(Target(**target_data))

            # Expectation Objects
            object_data = expectation_data["Object"]
            # print("\n --Context list-- ",context_data_list)
            print("\n --object_data-- ",object_data)
            if object_data:
                expectation_obj = Expectation(
                    verb=expectation_data.get('Verb'),
                    Targets=target_obj,
                    context=context_obj,
                    obj=Object_expectation(**object_data)
                )
                # Intent expectation
                self.__expectations.append(expectation_obj)
                # print("\n --expectation_obj-- ",expectation_obj)
            else:
                print("Error.No expectation object.")
            
    def __str__(self):
        expecs=[exp.__str__() for exp in self.__expectations]
        return f"IB_object(name={self.__name},context={self.__context},{expecs})"
    
    def get_dict(self):
        return {
                "Expectations":[exp.get_dict() for exp in self.__expectations],
                "Context":self.__context.get_dict(),
            }
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
        # logger.debug("keywords: %s",keywords)
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