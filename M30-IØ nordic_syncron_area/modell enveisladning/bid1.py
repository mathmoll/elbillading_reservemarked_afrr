import math
def bid(total_energy, discharge, charge, i, min_bid, andel, max_bud, granularity=False):
    #calculate the optimal bid for each product
    market_rules = {    'FCR N': {'hours discharge': 1.25,
                                    'hours charge': 1.25,
                                    'LER discharge': 0.34,
                                    'LER charge': 0.34,
                                    'LER limit': 2,
                                  'direction': 1},
                        'FCR D up': {'hours discharge': 0.33,
                                    'hours charge': 0,
                                    'LER discharge': 0,
                                    'LER charge': 0.2,
                                    'LER limit': 2,
                                      'direction': 1},
                        'FCR D down': {'hours discharge': 0,
                                      'hours charge': 0.33,
                                      'LER discharge': 0.2,
                                      'LER charge': 0,
                                      'LER limit': 2,
                                      'direction': -1},
                        'FFR Profil': {'hours discharge': 0.01,
                                'hours charge': 0,
                                'LER discharge': 0,
                                'LER charge': 0,
                                'LER limit': 0,
                                'direction': 1},
                        'FFR Flex': {'hours discharge': 0,
                                'hours charge': 0.01,
                                'LER discharge': 0,
                                'LER charge': 0,
                                'LER limit': 0,
                                'direction': -1},
                        'aFRR up': {'hours discharge': 1,
                                    'hours charge': 0,
                                    'LER discharge': 0,
                                    'LER charge': 0,
                                    'LER limit': 0,
                                    'direction': 1},
                        'aFRR down': {'hours discharge': 0,
                                      'hours charge': 1,
                                      'LER discharge': 0,
                                      'LER charge': 0,
                                      'LER limit': 0,
                                      'direction': -1}}

    if total_energy < market_rules[i]['LER limit']:
        discharge_max_limit = discharge - (discharge * market_rules[i]['LER discharge'])
        charge_max_limit = charge - (charge * market_rules[i]['LER charge'])
    else:
        discharge_max_limit = discharge
        charge_max_limit = charge

    e_need_discharge = market_rules[i]['hours discharge'] * discharge_max_limit
    e_need_charge = market_rules[i]['hours charge'] * charge_max_limit
    energy_start_value = e_need_discharge + e_need_charge




    #loop thrugh all dates and calculate the optimal bid

    while energy_start_value > total_energy:
        #print(energy_start_value, total_energy)
        discharge_max_limit = discharge_max_limit - 0.01
        charge_max_limit = charge_max_limit - 0.01
        e_need_discharge = market_rules[i]['hours discharge'] * discharge_max_limit
        e_need_charge = market_rules[i]['hours charge'] * charge_max_limit
        energy_start_value = e_need_discharge + e_need_charge
        energy_start_value = round(energy_start_value, 2)

    e_need_charge = total_energy - e_need_charge

    #only three digits
    discharge_max_limit = round(discharge_max_limit, 2)
    charge_max_limit = round(charge_max_limit, 2)
    e_need_discharge = round(e_need_discharge, 3)
    e_need_charge = round(e_need_charge, 3)
    energy_start_value = round(energy_start_value, 3)

    #print(i, discharge_max_limit, charge_max_limit, e_need_discharge, e_need_charge, energy_start_value)

    #sikkerhetsmargin for å unngå at batteriet blir tomt
    discharge_max_limit = discharge_max_limit * andel
    charge_max_limit = charge_max_limit * andel

    def round_down(value, decimals=0):
        factor = 10 ** decimals
        return math.floor(value * factor) / factor

    def count_decimals(value):
        # Konverter tallet til en streng
        num_str = str(value)

        # Finn posisjonen til desimalpunktet
        if '.' in num_str:
            # Returner antall karakterer etter desimalpunktet
            return len(num_str.split('.')[1])
        else:
            # Ingen desimaler hvis det ikke er noen desimalpunkt
            return 0

    desired_decimals = count_decimals(min_bid)
    #print(desired_decimals)

    #rund ned til ingen desimaler
    if granularity == True:
        discharge_max_limit = round_down(discharge_max_limit, desired_decimals)
        charge_max_limit = round_down(charge_max_limit, desired_decimals)




    if charge_max_limit > max_bud:
        charge_max_limit = max_bud
        #print('Max bud', max_bud, 'charge_max_limit', charge_max_limit)
    else:
        charge_max_limit = charge_max_limit
        #print('charge_max_limit', charge_max_limit)

    #finner bud i riktig retning
    if market_rules[i]['direction'] == 1:
        #print(discharge_max_limit)
        if discharge_max_limit >= min_bid:
            return -discharge_max_limit
        else:
            return 0
    else:
        if charge_max_limit >= min_bid:
            return charge_max_limit
        else:
            #print('yoo')
            return 0



#bid = bid(4, 2, 1.32, 'aFRR down', 0.11, 1, granularity=True, max_bud = None)


