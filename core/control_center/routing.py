from utils.config import config
# core/control_center/routing.py

from typing import Callable, Dict

class Router:
    """
    A simple router for handling different commands and modules.
    """

    def __init__(self):
        # Define routes as a dictionary where keys are strings (route names) 
        # and values are functions (handlers) that take no arguments and return None
        self.routes: Dict[str, Callable[[], None]] = {}

    def add_route(self, path: str, handler: Callable[[], None]) -> None:
        """
        Add a new route to the router.
        
        Args:
            path (str): The route path (e.g., 'start', 'load').
            handler (Callable[[], None]): The function to handle this route, taking no arguments and returning None.
        """
        self.routes[path] = handler
        print(f"Route {path} added.")

    def resolve(self, path: str) -> None:
        """
        Resolve and execute the handler for a given route.
        
        Args:
            path (str): The route path to resolve (e.g., 'start').
        """
        handler = self.routes.get(path)
        if handler:
            print(f"Executing handler for {path}.")
            handler()  # Call the function associated with the route
        else:
            print(f"Route {path} not found.")