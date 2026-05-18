import os
import json

from parser import parse_xml, build_children_map
from generators import (
    generate_config_xml,
    generate_meta_json,
    generate_delta,
    apply_delta
)

def write_json(path: str, data) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"[OK] {os.path.basename(path)}")

def main():
    base = os.path.dirname(os.path.abspath(__file__))

    model = parse_xml(os.path.join(base, "impulse_test_input.xml"))
    children_map = build_children_map(model)

    with open(os.path.join(base, "config.json"), encoding="utf-8") as f:
        config = json.load(f)

    with open(os.path.join(base, "patched_config.json"), encoding="utf-8") as f:
        patched = json.load(f)
    
    config_xml = generate_config_xml(model, children_map)
    with open(os.path.join(base, "config.xml"), "w", encoding="utf-8") as f:
        f.write(config_xml)
    print("[OK] config.xml")
    
    write_json(os.path.join(base, "meta.json"), generate_meta_json(model, children_map))

    delta = generate_delta(config, patched)

    write_json(os.path.join(base, "delta.json"), delta)

    result = apply_delta(config, delta)
    
    write_json(os.path.join(base, "res_patched_config.json"), result)

    if result == patched:
        print("\n[PASS] res_patched_config.json совпадает с patched_config.json")
    else:
        extra = set(result) - set(patched)
        missing = set(patched) - set(result)
        print(f"\n[WARNING] Расхождение: лишние ключи = {extra}, отсутствующие = {missing}")

if __name__ == "__main__":
    main()