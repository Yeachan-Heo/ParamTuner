import numpy as np
# alias
nan = np.nan

class VariableHolder:
    def __init__(self, **kwargs):
        self.temp = None
        self.varnames = []
        self.add_variables(**kwargs)


    def add_variables(self, **kwargs):
        for name, value in kwargs.items():
            if not name in self.varnames:
                self.varnames.append(name)
            exec(f"self.{name} = {value}")

    def register_variable(self, variable_name, variable):
        self.add_variables(**{variable_name:variable})

    def set_value(self, variable_name: str, value: float):
        if variable_name in dir(self):
            exec(f"self.{variable_name} = {value}")
        else:
            raise ValueError(f"Unknown Variable {variable_name}")

    def get_value(self, variable_name):
        exec(f"self.temp = self.{variable_name}")
        return self.temp

    def __getitem__(self, item):
        return self.get_value(item)


