def prepare_id_in_dict_form(instances):
    return [ {'Id' : str(instance.id)} for instance in instances]

def prepare_id_in_array_form(instances):
    return [ str(instance.id) for instance in instances]