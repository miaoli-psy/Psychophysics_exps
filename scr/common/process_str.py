import ast


def str_to_list(string: str) -> list:
    """
    convert list-like str to list
    :param string: "[(0, 100), (105, 10) ...]"
    :return: list of tuples
    """
    return ast.literal_eval(string)


def raw_resp_to_int(raw_resp):
    """
    # convert response to int
    ('xxx   224rfff  ')) # -->224
    :param raw_resp: float or str collect from keyboard response
    :return: int response
    """
    if isinstance(raw_resp, float):
        return int(raw_resp)
    # apply to rows with str
    if isinstance(raw_resp, str):
        if not raw_resp:
            return None
        res_s = ""
        for c in filter(str.isdigit, raw_resp):
            res_s += c
        if res_s == "":
            return None
        else:
            return int(res_s)
