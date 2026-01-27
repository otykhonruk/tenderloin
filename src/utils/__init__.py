def display_dict(d):
    return {k: f'#list[{len(v)}]' if isinstance(v, list) else v
            for k, v in d.items()}
