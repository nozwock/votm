from votm.config._config import Access_Config


def cand_check(key):
    cand = [eval(i) for i in list(Access_Config().cand_config.keys())]
    ind = [i[0] for i in cand].index(key)
    return str(cand[ind])
