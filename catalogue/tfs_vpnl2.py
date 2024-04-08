import logging
from abstract_library import abstract_library

logger = logging.getLogger(__name__)

class tfs_vpnl2(abstract_library):
    """
    Abstract class created as 
    """
    def __init__(self):
        decision_tree={
            "vpnl2":"http_handler"
        }
        super().__init__(module_name="tfs_vpnl2",isILU=True,params={},decision_tree=decision_tree)
    
    def transaltor(self):
        pass
    
    def vpnl2_structure(self):
        pass

if __name__ == "__main__":
    a=tfs_vpnl2()
    print(a.get_decision_tree())
