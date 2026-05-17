import os
import json

from parser import parse_xml, build_children_map
from generators import (
    generate_config_xml,
    generate_meta_json,
    generate_delta,
    apply_delta
)

def main():
    base = os.path.dirname(os.path.abspath(__file__))

    xml_path = os.path.join(base, "impulse_test_input.xml")
    config_path = os.path.join(base, "config.json")
    patched_path = os.path.join(base, "patched_config.json")

    model = parse_xml(xml_path)
    children_map = build_children_map(model)

    with open(config_path, encoding="utf-8") as f:
        config = json.load(f)
    
    with open(patched_path, encoding="utf-8") as f:
        patched = json.load(f)
    
    config_xml = generate_config_xml(model, children_map)
    with open(os.path.join(base, "config.xml"), "w", encoding="utf-8") as f:
        f.write(config_xml)

    meta = generate_meta_json(model, children_map)
    with open(os.path.join(base, "meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=4)
    
    delta = generate_delta(config, patched)
    with open(os.path.join(base, "delta.json"), "w", encoding="utf-8") as f:
        json.dump(delta, f, ensure_ascii=False, indent=4)

    result = apply_delta(config, delta)
    with open(os.path.join(base, "res_patched_config.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()