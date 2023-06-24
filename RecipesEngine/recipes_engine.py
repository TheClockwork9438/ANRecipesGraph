
import networkx as nx
import json

JSON_DATA_PATH = "data/recipes_graph.graphml"
GRAPH_PATH = "data/recipes.json"

class RecipesEngine():
    """
    Class Description: RecipesEngine
    """
    def __init__(self):
        
        self.recipesGraph = nx.Graph()
        
        pass
    
    def load_graph(self):
        self.recipesGraph = nx.read_graphml(GRAPH_PATH)      
        pass
    
    def create_graph_from_json(self):
        
        recipes = {}
        with open(JSON_DATA_PATH) as f:
            recipes = json.load(f)
        
        for recip_k, recip_data in recipes.items():
    
            recip_name = recip_data.get("nombre")
            self.recipesGraph.add_node(recip_name)
                
            ingredients = recip_data.get("ingredientes")
            for i in ingredients:
                ingredient_name = i.get("nombre")
                self.recipesGraph.add_node(ingredient_name)
                self.recipesGraph.add_edge(recip_name, ingredient_name)
                pass
            
            pass

            nx.write_graphml(self.recipesGraph, "data/recipes_graph.graphml")
        pass
    
    def suggest_recipes_from_ingredients(self, ingredients:list):
        
        pass
    
    def suggest_ingredient_substitute(self, ingredient, recipe_hint):
        
        pass
    
    def build_a_familly_weak_menu(self, available_recipes, hints):
        
        pass
    
    
    pass