class Building:
    def __init__(self,resarea=0,height=0,elev=0,cat=0):
        """Initialize a building instance"""
        self.resarea = resarea # Double: Building residential area sqft
        self.height = height # Double: Building height ft
        self.elev = elev # Double: Base elevation from sea level ft
        self.cat = cat # Int: Category of building
    def damage_rate(self,h):
        """Takes in inundation depth h and returns the damage rate"""
        if self.height > 0:
            if h <= self.elev:
                return 0
            elif (h-self.elev) > self.height:
                return 1
            else:
                return (h-self.elev)/self.height
        else:
            return 0
    def damage_estim(self,h):
        """Takes in inundation depth h and returns a damage loss"""
        value = 0
        if self.cat in ['A0','A1','A2','A3','A4','A5','A6','A7','A8','A9',
                       'S0','S1']:
            # RES1 Single Family Dwelling
            value = 182492+91246
        elif self.cat in ['B1','B2','B3','B9','S2']:
            # RES3A Duplex
            value = 186630+93315
        elif self.cat in ['C0','C3','S3']:
            # RES3B Triplex / Quads
            value = 282573+141287
        elif self.cat in ['C1','C2','C4','C5','C6','C7','C8','C9','CM',
                          'D0','D1','D2','D3','D4','D5','D6','D7','D8','D9',
                         'HB','HH','HR','HS','H1','H2','H3','H4','H5','H6',
                         'H7','H8','H9','L1','L2','L3','L8','L9','R0','R1',
                         'R2','R3','R4','R5','R6','R7','R8','R9','RR','RH',
                         'S4','S5','S9']:
            # Multi-dwellings
            if self.resarea > 0:
                estim_unit = int(self.resarea/866) # Average unit size in NY is 866 sqft
                if estim_unit<9:
                    value = 873207+436604
                elif estim_unit<19:
                    value = 1546338+773169
                elif estim_unit<49:
                    value = 3714867+1857433
                else:
                    value = 18707261+9353631
            else:
                value = 0
        elif self.cat in ['P2','N1','N2','N3','N4','N9']:
            # RES4 Temporary Lodging
            value = 11991508+5995754
        elif self.cat in ['H8']:
            # RES5 Institutional Dormitory
            value = 7019251+3509626
        elif self.cat in ['I6']:
            # RES6 Nursing Home
            value = 8067754+4033877
        elif self.cat in ['K1','K2','K4','K5','K9','RK']:
            # COM1 Retail Trade
            value = 571211+571211+41339
        elif self.cat in ['K3','K6','K8']:
            # COM2 Wholesale Trade
            value = 1466010+1466010+127395
        elif self.cat in ['RB','O1','O2','O3','O4','O5','O6','O7','O8','O9']:
            # COM4 Professional/Technical Services
            value = 11381918+11381918
        elif self.cat in ['K7']:
            # COM5 Banks
            value = 2370537+2370537
        elif self.cat in ['I1','I4']:
            # COM6 Hospital
            value = 81553944+122330915
        elif self.cat in ['I2','I3','I5','I7','I9']:
            # COM7 Medical Office/Clinic
            value = 4904708+7357062
        elif self.cat in ['Q1','Q2','Q3','Q4','Q5','Q6','Q7','Q8','Q9','P3',
                         'P4','P5','P6','P7','P8','P9','RT']:
            # COM8 Entertainment & Recreation
            value = 2260999 +2260999
        elif self.cat in ['P1','J1','J2','J3','J4','J5','J6','J7','J8','J9']:
            # COM9 Theaters
            value = 6015389+6015389
        elif self.cat in ['G0','G1','G2','G3','G4','G5','G6','G7','G8','G9','GU','GW','RG','RP','Z2']:
            # COM10 Parking
            value = 180913+90457
        elif self.cat in ['F1','F2','F8','E1','E2','E3','E4','E7','E9','RW','RS']:
            # IND1 Heavy
            value = 1677769+2516654+585357
        elif self.cat in ['F4','F5','F9']:
            # IND2 Light
            value = 4095922+6143882+422805
        elif self.cat in ['M1','M2','M3','M4','M9']:
            # REL1 Churches and Other Non-profit
            value = 1982996+1982996
        elif self.cat in ['RA','Y3','Y4','Y5','Y6','Y7','Y8','Y9']:
            # GOV1 General Services
            value = 18290701+18290701
        elif self.cat in ['Y1','Y2']:
            # GOV2 Emergency Response
            value = 2874692+4312038
        elif self.cat in ['W1']:
            # EDU1 Grade Schools
            value = 7797433+7797433
        elif self.cat in ['W2','W3','W4','W5','W6','W7','W8','W9']:
            # EDU2 Colleges/Universities
            value = 27175914+40763870
        loss = value*self.damage_rate(h)
        return loss

class Region:
    def __init__(self,buildings):
        # Takes in a dictionary of building instances and generate a region
        self.buildings = buildings
    def loss_estim(self,h):
        # Takes in height of flood, height of proposed levee height, current year, and interest i
        cumu_loss = 0

        for index in self.buildings:
            building = self.buildings[index]
            loss = building.damage_estim(h)
            cumu_loss += loss
        return cumu_loss

def build_seawall(h,initial=False):
    length_AK = 0.5
    length_VN = 1.82
    length_ER = 1.36
    length_JB = 1.73 # km Aertz Bay-Closed
    length = length_AK+length_VN+length_ER+length_JB
    unitCost_AK = (1.9+2.18)/2/30 # billion/km*ft
    unitCost_VN = (2.37+3.53)/2/30 # billion/km*ft
    unitCost_ER = (1.9+2.18)/2/30 # billion/km*ft
    unitCost_JB = (2.37+3.53)/2/30 # billion/km*ft
    if initial:
        fixed_cost = 9.5 # billion
        cost = ((unitCost_AK*length_AK+unitCost_VN*length_VN+unitCost_ER*length_ER+unitCost_JB*length_JB)*h+fixed_cost)*10**9
    else:
        fixed_cost = (11.6+(16.6-11.6)/2)-9.5 # billion
        cost = ((unitCost_AK*length_AK+unitCost_VN*length_VN+unitCost_ER*length_ER+unitCost_JB*length_JB)*h+fixed_cost)*10**9
    return cost
