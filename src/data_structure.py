from src.tools import deep_getattr


class Structure:
    """Structures data into a single format."""
    
    structures = {}
    
    def __init__(self, item: any, structure_source: str = '') -> None:
        self.item: any = item
        self.structure_source_name: str = structure_source
        if structure_source not in self.structures:
            raise RuntimeError(f'Structure "{structure_source}" not found')
        self.structure_source: str = self.structures[structure_source]

    def format(self, fields: list) -> dict:
        result = []
        for field in fields:
            if field == 'source_name':
                result.append(self.structure_source_name)
                continue
            
            if not hasattr(self.structure_source, field):
                raise RuntimeError(f'Structure "{self.structure_source_name}" doesn\'t have attr "{field}"')
            
            result.append(deep_getattr(self.item, getattr(self.structure_source, field)))

        return result


def register_structure(name):
    """Decorator for register structurs."""
    
    def decorator(cls):
        if name in Structure.structures:
            raise RuntimeError(f'Can\'t register structure "{name}": name already exists')
        Structure.structures[name] = cls
    
    return decorator


@register_structure('data_Soruce_1')
class FirstStructureSource:
    id = 'id'
    ean_code = 'EAN'
    name = 'NAME'


@register_structure('data_Source_2')
class SecondStructureSource:
    id = 'id'
    ean_code = 'EAN'
    name = 'Description'


@register_structure('data_Source_3')
class ThridStructureSource:
    id = 'Id'
    ean_code = ['EANs', 0]
    name = 'name'
