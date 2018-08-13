def nested_lookup(key,dictionary):
    return list(_nested_lookup(key,dictionary))


def _nested_lookup(key,dictionary):
    for k,v in dictionary.items():
        if k==key:
            yield v

        elif isinstance(v,dict):
            for result in _nested_lookup(key,v):
                yield result
        
        elif isinstance(v,list):
            for d in v:
                for result in _nested_lookup(key,d)
                    yield result
