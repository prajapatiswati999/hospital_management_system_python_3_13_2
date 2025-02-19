class BaseModelMeta(type): 
    """Metaclass for models to ensure consistent behavior.""" 
    def __new__(cls, name, bases, dct): 
        if 'save' not in dct: 
            raise TypeError(f"Class {name} must implement save method") 
        return super().__new__(cls, name, bases, dct) 
# Example usage 
class BaseModel(metaclass=BaseModelMeta): 
    def save(self): 
        raise NotImplementedError("Save method must be implemented.")