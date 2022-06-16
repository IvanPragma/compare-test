import json
import xmltodict
from lxml import etree
from lxml import objectify


def register_data_format(cls):
    """Decorator for register data formats."""
    
    if cls.name in DataFormatHandler.formats:
        raise RuntimeError(f'Can\'t register data format "{cls.name}": name already exists')
    DataFormatHandler.formats[cls.name] = cls
    
    return cls


class DataFormatHandler:
    """Base for all data formats classes."""

    formats = {}

    def __init__(self, path: str) -> None:
        self.path: str = path
        
    def from_python(self, data: any) -> str:
        return str(data)
    
    def to_python(self, data: str) -> str:
        return str(data)
    
    def read(self) -> any:
        with open(self.path, 'r', encoding='utf-8') as f:
            return self.to_python(f.read())
        
    def write(self, data: any) -> None:
        with open(self.path, 'w', encoding='utf-8') as f:
            f.write(self.from_python(data))


@register_data_format
class JSONFormat(DataFormatHandler):
    name = 'json'
    extensions = ['json']
    
    def from_python(self, data: any) -> str:
        return json.dumps(data, indent=4)

    def to_python(self, data: str) -> any:
        return json.loads(data, strict=False)


@register_data_format
class XMLFormat(DataFormatHandler):
    name = 'xml'
    extensions = ['xml']
    
    def from_python(self, data: any) -> str:
        return ET.dump(data)

    def to_python(self, data: str) -> any:
        res = xmltodict.parse(data)
        if 'SHOP' in res:
            res = res['SHOP']['SHOPITEM']
        elif 'Stock' in res:
            res = res['Stock']['Product']
        return res
        result = {}
        data = data.encode('utf-8')
        parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
        for item in etree.fromstring(data, parser=parser):
            result[item.name] = item.text

        return result

    
class DataEngine:
    """Abstraction for data-engines classes"""

    @staticmethod
    def get_dfh(path: str) -> DataFormatHandler:
        """Get data format handler.

        Depending on the file extension,
        it will return the desired DataFormatHandler.
        """

        extension = path.split('.')[-1]
        data_format = None

        for data_format_handler in DataFormatHandler.formats.values():
            if extension in data_format_handler.extensions:
                data_format = data_format_handler
                break
            
        return data_format(path)

    @staticmethod
    def read(path: str) -> any:
        dfh = DataEngine.get_dfh(path)
        return dfh.read()

    @staticmethod
    def write(path: str, data: any) -> None:
        dfh = DataEngine.get_dfh(path)
        return dfh.write(data)
