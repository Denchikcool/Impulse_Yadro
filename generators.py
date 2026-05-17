def generate_config_xml(model: dict, children_map: dict) -> str:
    raise NotImplementedError

def generate_meta_json(model: dict, children_map: dict) -> list:
    raise NotImplementedError

def generate_delta(config: dict, patched: dict) -> dict:
    raise NotImplementedError

def apply_delta(config: dict, delta: dict) -> dict:
    raise NotImplementedError