class AppAPI:
    """ Handles backend logic and exposes functions to JavaScript. """
    
    def greet(self, name: str) -> str:
        """ Example function: Returns a greeting message. """
        return f"Hello, {name}!"
