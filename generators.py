import xml.etree.ElementTree as ET
from xml.dom import minidom

def build_xml_element(class_name: str, model: dict, children_map: dict) -> ET.Element:
    elem = ET.Element(class_name)
    cls = model["classes"][class_name]

    for attr in cls["attributes"]:
        sub = ET.SubElement(elem, attr["name"])
        sub.text = attr["type"]
    
    for child_name, _ in children_map.get(class_name, []):
        elem.append(build_xml_element(child_name, model, children_map))
    
    return elem

def generate_config_xml(model: dict, children_map: dict) -> str:
    root_class = next(name for name, info in model["classes"].items() if info["isRoot"])
    root_elem = build_xml_element(root_class, model, children_map)

    def expand_empty(elem: ET.Element) -> None:
        if elem.text is None and len(elem) == 0:
            elem.text = ""
        
        for child in elem:
            expand_empty(child)
    
    expand_empty(root_elem)

    raw = ET.tostring(root_elem, encoding="unicode")
    dom = minidom.parseString(raw)
    pretty = dom.toprettyxml(indent="   ")
    lines = [l for l in pretty.splitlines() if l.strip() and not l.startswith("<?xml")]

    return "\n".join(lines) + "\n"

def parse_multiplicity(mult: str) -> tuple[str, str]:
    if ".." in mult:
        parts = mult.split("..")
        return parts[0], parts[1]
    return mult, mult

def generate_meta_json(model: dict, children_map: dict) -> list:
    classes = model["classes"]
    aggregations = model["aggregations"]

    mult_map: dict = {}

    for agg in aggregations:
        mult_map[agg["source"]] = parse_multiplicity(agg["sourceMultiplicity"])

    seen: list = []

    for agg in aggregations:
        if agg["source"] not in seen:
            seen.append(agg["source"])
    for name in classes:
        if classes[name]["isRoot"] and name not in seen:
            seen.append(name)
    
    result: list = []

    for name in seen:
        cls = classes[name]
        entry: dict = {
            "class": name,
            "documentation": cls["documentation"],
            "isRoot": cls["isRoot"]
        }

        if not cls["isRoot"]:
            mn, mx = mult_map.get(name, ("0", "1"))
            entry["max"] = mx
            entry["min"] = mn
        
        params = [{"name": a["name"], "type": a["type"]} for a in cls["attributes"]]

        for child_name, _ in children_map.get(name, []):
            params.append({"name": child_name, "type": "class"})
        
        entry["parameters"] = params
        result.append(entry)
    
    return result

def generate_delta(config: dict, patched: dict) -> dict:
    raise NotImplementedError

def apply_delta(config: dict, delta: dict) -> dict:
    raise NotImplementedError