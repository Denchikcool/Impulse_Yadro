import xml.etree.ElementTree as ET

def parse_xml(path: str) -> dict:
    tree = ET.parse(path)
    root = tree.getroot()

    classes: dict = {}
    aggregations: list = []

    for child in root:
        tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag

        if tag == "Class":
            name = child.attrib["name"]
            is_root = child.attrib.get("isRoot", "false").lower() == "true"
            doc = child.attrib.get("documentation", "")
            attrs = []
            for attr in child:
                attr_tag = attr.tag.split("}")[-1] if "}" in attr.tag else attr.tag
                
                if attr_tag == "Attribute":
                    attrs.append({
                        "name": attr.attrib["name"],
                        "type": attr.attrib["type"]
                    })
            
            classes[name] = {"isRoot": is_root, "documentation": doc, "attributes": attrs}
        
        elif tag == "Aggregation":
            aggregations.append({
                "source": child.attrib["source"],
                "target": child.attrib["target"],
                "sourceMultiplicity": child.attrib.get("sourceMultiplicity", "1"),
                "targetMultiplicity": child.attrib.get("targetMultiplicity", "1")
            })
    
    return {"classes": classes, "aggregations": aggregations}

def build_children_map(model: dict) -> dict:
    children_map: dict = {}

    for agg in model["aggregations"]:
        parent = agg["target"]
        child = agg["source"]
        mult = agg["sourceMultiplicity"]
        children_map.setdefault(parent, []).append((child, mult))
    
    return children_map