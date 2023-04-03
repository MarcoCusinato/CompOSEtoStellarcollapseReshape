def periodic_table(index):
    """
    Returns the name and mass number of the particle with the given index.
    Many of the particles are not used in CCSN simulations, but are included
    for completeness. 
    """
    periodic_table = {
        0: {'name': "e", 'A': 0},         # electron
        1: {'name': "muon", 'A': 0},      # muon
        10: {'name': "n", 'A': 1},        # neutron
        11: {'name': "p", 'A': 1},        # proton
        20: {'name': "delM", 'A': 0},     # Delta-minus
        21: {'name': "Del0", 'A': 0},     # Delta-zero
        22: {'name': "DelP", 'A': 0},     # Delta-plus
        23: {'name': "DelPP", 'A': 0},    # Delta-double-plus
        100: {'name': "lambda", 'A': 0},  # lambda baryon
        110: {'name': "sigmaM", 'A': 0},  # sigma-minus
        111: {'name': "sigma0", 'A': 0},  # sigma-zero
        112: {'name': "sigmaP", 'A': 0},  # sigma-plus
        120: {'name': "xiM", 'A': 0},     # xi-minus
        121: {'name': "xi0", 'A': 0},     # xi-zero
        200: {'name': "omega", 'A': 0},   # omega
        210: {'name': "sigma", 'A': 0},   # sigma
        220: {'name': "eta", 'A': 0},     # eta
        230: {'name': "etap", 'A': 0},    # eta'
        300: {'name': "rhoM", 'A': 0},    # rho-minus
        301: {'name': "rho0", 'A': 0},    # rho-zero
        302: {'name': "rhoP", 'A': 0},    # rho-plus
        310: {'name': "delM", 'A': 0},    # delta-minus
        311: {'name': "del0", 'A': 0},    # delta-zero
        312: {'name': "delP", 'A': 0},    # delta-plus
        320: {'name': "piM", 'A': 0},     # pi-minus
        321: {'name': "pi0", 'A': 0},     # pi-zero
        322: {'name': "piP", 'A': 0},     # pi-plus
        400: {'name': "phi", 'A': 0},     # phi
        420: {'name': "kM", 'A': 0},      # k-minus
        421: {'name': "k0", 'A': 0},      # k-zero
        422: {'name': "kbar0", 'A': 0},   # k-bar-zero
        423: {'name': "kP", 'A': 0},      # k-plus
        424: {'name': "kth", 'A': 0},     # thermal-kaon
        425: {'name': "KMcond", 'A': 0},  # K-minus-condensated
        500: {'name': "up", 'A': 0},      # up quark
        501: {'name': "down", 'A': 0},    # down quark
        502: {'name': "strange", 'A': 0}, # strange quark
        2001: {'name': "d", 'A': 2, 'Z': 1},      # deuterium
        3001: {'name': "t", 'A': 3, 'Z': 1},      # tritium
        4002: {'name': "a", 'A': 4, 'Z': 2},      # alpha
        3002: {'name': "3he", 'A': 3, 'Z': 2},    # helium-3
        4003: {'name': "4li", 'A': 4, 'Z': 3},    # lithium-4
    }
    return periodic_table[index]
    
