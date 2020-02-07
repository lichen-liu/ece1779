def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    From: https://stackoverflow.com/questions/12523586/python-format-size-application-converting-b-to-kb-mb-gb-tb
    """
    step_unit = 1024.0

    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < step_unit:
            return "%3.1f %s" % (num, x)
        num /= step_unit