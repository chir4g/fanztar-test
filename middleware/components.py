import json
import os
from uuid import uuid4




class JsonMiddleware:
    """Manipulates the underlying JSON resource for components."""
    @staticmethod
    def get_all_unique_part_names(CODE_2_PRICE_PART : list[dict]) -> set:
        """Get all unique part names
        OS is a part and (Android OS or iOS OS) are two different components of same part "OS"
        """
        parts = set(component_details[1].split(" ")[-1] for _, component_details in CODE_2_PRICE_PART.items())
        return parts

    @staticmethod
    def get_part_name(component_name: str) -> str:
        return component_name.split(" ")[-1]

class ComponentMiddleware:
    """Middleware class for Component Handlings
    For ex : OS is a part and (Android OS or iOS OS) are two different components of same part "OS"
    ...
    Attributes
    ----------
    Class Attributes:
    CODE_2_PRICE_PART : dict<order_id:str, total:0, parts:list[]>
        Loads Json as static variable(class-level resource)
    ALL_PART_NAMES : set<str>
        Loads part-names from the CODE_2_PRICE_PART names

    Instance Attributes:
    all_parts_count : dict<str:int>
        Keeps count of each unique part

    ----------

    Methods
    ----------
    add_component_name(self, component_name : str)
        Adds component_name to component_details.

    add_component_price(self, component_price : float)
        Adds component_price to component_details.

    add_to_component_details(self, component_id : str)
        Adds to component_details based on component_id.

    set_details(self, component_ids : list[str])
        Sets component_details for component_ids.

    """
    CODE_2_PRICE_PART = json.loads(open(os.path.join("resources", "constants", "CODE_2_PRICE-PART.json")).read())
    ALL_PART_NAMES = JsonMiddleware.get_all_unique_part_names(CODE_2_PRICE_PART= CODE_2_PRICE_PART)

    def __init__(self) -> None:
        self.all_parts_count = {part_name : 0 for part_name in ComponentMiddleware.ALL_PART_NAMES}
        self.failure = None
        self.component_details = {
            "order_id" : uuid4(),
            "total" : 0,
            "parts" : []
        }


    def add_component_name(self, component_name : str) -> None:
        """Adds component name to component_details"""
        self.component_details["parts"].append(component_name)

    def add_component_price(self, component_price : float) -> None:
        "Adds component price to component_details"
        self.component_details["total"] += component_price

    def add_to_component_details(self, component_id : str) -> dict:
        """Adds to component_details based on component_id"""
        component_details =  ComponentMiddleware.CODE_2_PRICE_PART.get(component_id, None)
        if component_details:
            component_price, component_name = component_details
            part_name = JsonMiddleware.get_part_name(component_name)
            self.all_parts_count[part_name] += 1
            part_count = self.all_parts_count[part_name]
            

            if part_count > 1:
                self.failure = {"reason" : f"part : {part_name}({part_count}) has more than 1 asked component, please check" \
                    f" and make sure you have only one component for each of the following parts : {', '.join(ComponentMiddleware.ALL_PART_NAMES)}"}
            
            else:
                self.add_component_name(component_name)
                self.add_component_price(component_price)

        else:
            self.failure = f"Component-Id : {component_id} not found."

        return self.component_details


    def set_details(self, component_ids : list[str]) -> None:
        """Sets details based on component_ids"""

        #Design is kept in a way that only till the component_id satisfy the constraints, the computation is done.
        #Once any issue is found, the loop breaks saving rest of computer.
        for component_id in component_ids:
            self.add_to_component_details(component_id)
            if self.failure:
                break

        

