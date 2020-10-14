from votm.config import Config


def cand_check(key):
    cand = [eval(i) for i in list(Config().load("candidate").keys())]
    ind = [i[0] for i in cand].index(key)
    return str(cand[ind])
