from neuron import h
import  random
from neuron import h, crxd as rxd
somaR = 11.0  # soma radius
dendR = 4  # dendrite radius
dendL = 300.0
dendL1 = 300.0
dendL2 = 300.0
dendL3 = 300.0# dendrite length
axonR = 2
axonL = 100
doff = dendL + somaR

class Cell:
    def __init__(self, x, y, z, num):
        self.x = x
        self.y = y
        self.z = z
        self.Excitatory = 0
        self.soma = h.Section(name='soma', cell=self)
        self.soma.pt3dclear()
        self.soma.pt3dadd(x, y, z + somaR, 2.0 * somaR)
        self.soma.pt3dadd(x, y, z - somaR, 2.0 * somaR)

        self.dend = h.Section(name='dend', cell=self)
        self.dend.pt3dclear()
        self.dend.pt3dadd(x, y, z - somaR, 2.0 * dendR)
        self.dend.pt3dadd(x, y, z - somaR - dendL, 2.0 * dendR)
        self.dend.nseg = 10
        self.dend.connect(self.soma(1))

        self.axon = h.Section(name='axon', cell=self)
        self.axon.pt3dclear()
        self.axon.pt3dadd(x, y, z + axonR, 2.0 * axonR)
        self.axon.pt3dadd(x, y, z + axonR + axonL, 2.0 * axonR)
        self.axon.connect(self.soma, 0, 1)

        self.all = [self.soma, self.dend]
        self.somaV = h.Vector()
        self.somaV.record(self.soma(0.5)._ref_v)

        self.dendV = h.Vector()
        self.dendV.record(self.dend(0.5)._ref_v)
        self.axonV = h.Vector()
        self.axonV.record(self.axon(0.5)._ref_v)




        self._spike_detector = h.NetCon(self.soma(0.5)._ref_v, None, sec=self.soma)
        self.spike_times = h.Vector()
        self._spike_detector.record(self.spike_times)
        
        self._ncs = []
        self.synlistexI = []
        self.synlistexE = []
        #self.count=0
        self.number=num
        self.cells={}

        self.dend1 = h.Section(name='dend1', cell=self)
        self.dend1.pt3dclear()
        self.dend1.pt3dadd(x, y, z - somaR, 2.0 * dendR)
        self.dend1.pt3dadd(x, y, z - somaR - dendL1, 2.0 * dendR)
        self.dend1.nseg = 10
        self.dend1.connect(self.soma(0))

        self.dend2 = h.Section(name='dend2', cell=self)
        self.dend2.pt3dclear()
        self.dend2.pt3dadd(x, y, z - somaR, 2.0 * dendR)
        self.dend2.pt3dadd(x, y, z - somaR - dendL2, 2.0 * dendR)
        self.dend2.nseg = 10
        self.dend2.connect(self.soma(0.5))

        self.dend3 = h.Section(name='dend3', cell=self)
        self.dend3.pt3dclear()
        self.dend3.pt3dadd(x, y, z - somaR, 2.0 * dendR)
        self.dend3.pt3dadd(x, y, z - somaR - dendL3, 2.0 * dendR)
        self.dend3.nseg = 10
        self.dend3.connect(self.soma(1))

        self.dend4 = h.Section(name='dend4', cell=self)
        self.dend4.pt3dclear()
        self.dend4.pt3dadd(x, y, z - somaR, 2.0 * dendR)
        self.dend4.pt3dadd(x, y, z - somaR - dendL, 2.0 * dendR)
        self.dend4.nseg = 10
        self.dend4.connect(self.soma(0.8))

        self.dendV1 = h.Vector().record(self.dend1(0.5)._ref_v)
        self.dendV2 = h.Vector().record(self.dend2(0.5)._ref_v)
        self.dendV3 = h.Vector().record(self.dend3(0.5)._ref_v)
        self.dendV4 = h.Vector().record(self.dend4(0.5)._ref_v)

        self.dends=[self.dend1, self.dend,self.dend2, self.dend3, self.dend4]
        '''
                for d in self.dends:
            synE = h.AMPA(d(0.5))
            synE.tau = 1
            synE.e = 30
            self.synlistex.append(synE)
        '''
        for d in self.dends:
            synI = h.GABAA(d(0.5))
            synI.tau = 0.3
            synI.e = -50
            self.synlistexI.append(synI)
            synE = h.AMPA(d(0.5))
            synE.tau = 1
            synE.e = 50
            self.synlistexE.append(synE)
            self.synlistexNMDA=[]
            synE = h.NMDA1(d(0.5))
            self.synlistexNMDA.append(synE)


        self._set_position(x, y, z)
        self.syns = []
        self.netcons = []

        # everything below here in this method is NEW

        #self.nmda1 = h.Vector().record(self.synlistexNMDA[0]._ref_i)
        #self.nmda2 = h.Vector().record(self.synlistexNMDA[1]._ref_i)
        #self.nmda3 = h.Vector().record(self.synlistexNMDA[2]._ref_i)
        #self.nmda4 = h.Vector().record(self.synlistexNMDA[3]._ref_i)
        #self.nmda5 = h.Vector().record(self.synlistexNMDA[4]._ref_i)

        #self.data=[self.nmda1,
        #            self.nmda2,
        #            self.nmda3,
        #            self.nmda4,
        #            self.nmda5]

    def _set_position(self, x, y, z):
        for sec in self.all:
            for i in range(sec.n3d()):
                sec.pt3dchange(i,
                               x - self.x + sec.x3d(i),
                               y - self.y + sec.y3d(i),
                               z - self.z + sec.z3d(i),
                               sec.diam3d(i))
        self.x, self.y, self.z = x, y, z

    def connect_cells(self, target, type, w, d):
        if(type==1):
            j = random.randint(0,len(target.dends)-1)
            synE = h.AMPA(target.dends[j](0.8))
            synE.tau = 1
            synE.e = 50
            #self.synlistexE.append(synE)
            nc = h.NetCon(self.axon(0.9)._ref_v, synE, sec=self.axon)
            nc.weight[0] = random.gauss(w, w/3 )
            nc.delay = random.gauss(d, 1/4)
            #target._ncs.append(nc)
            self._ncs.append(nc)
            target.syns.append(synE)
            #target.count += 1
            #target.cells[self.number] = self.id


        elif(type==-1):
            #for sec in self.dends:
            j = random.randint(0, len(target.dends)-1)
            synI = h.GABAA(target.dends[j](0.8))
            synI.tau = 0.3
            synI.e = -30
            #self.synlistexI.append(synI)
            nc = h.NetCon(self.axon(0.9)._ref_v, synI, sec=self.axon)
            nc.weight[0] = random.gauss(w, w / 3)
            nc.delay =  random.gauss(d, 1/4)
            self._ncs.append(nc)
            target.syns.append(synI)
            #target.count += 1
            #target.cells[self.number] = self.id


        elif (type == 0):
            j = random.randint(0, len(target.dends)-1)
            synE = h.NMDA1(target.dends[j](0.8))
            #self.synlistexNMDA.append(synE)
            nc = h.NetCon(self.axon(0.9)._ref_v, synE, sec=self.axon)
            nc.weight[0] = random.gauss(w, w / 3)
            nc.delay = random.gauss(d, 1/4)
            self._ncs.append(nc)
            target.syns.append(synE)


        

class Bask23(Cell):
    def __init__(self, x, y, z, num):
        super().__init__(x , y, z, num)
        self.id = 1
        self.Excitatory = -1
        self.name = 'superficial interneurons basket'

        # ---------------soma----------------
        for mechanism_s in ['extracellular', 'Nafin', 'kdrin', 'IKsin', 'hin', 'kapin', 'canin', 'kctin', 'cadynin',
                            'pas']:
            self.soma.insert(mechanism_s)

        self.soma(0.5).Nafin.gnafbar = 0.5
        self.soma(0.5).kdrin.gkdrbar = 0.001
        self.soma(0.5).IKsin.gKsbar = 0.000725 * 0.1
        self.soma(0.5).hin.gbar = 0.00001
        self.soma(0.5).kapin.gkabar = 0.0032 * 15
        self.soma(0.5).canin.gcalbar = 0.0003
        self.soma(0.5).kctin.gkcbar = 0.0001
        self.soma(0.5).pas.g = 0.0002
        self.soma(0.5).pas.e = -70
        self.soma.Ra = 100
        #self.soma(0.5).nap.gnapbar = 0.018

        #self.v1 = h.Vector().record(self.soma(0.5)._ref_ina_Nafin)
        # self.v2 = h.Vector().record(self.soma(0.5)._ref_ina_nap)
        #self.v3 = h.Vector().record(self.soma(0.5)._ref_ik_kdrin)
        #self.v4 = h.Vector().record(self.soma(0.5)._ref_ik_IKsin)
        # self.v5 = h.Vector().record(self.soma(0.5)._ref_ik_kc_fast)
        # self.v6 = h.Vector().record(self.soma(0.5)._ref_ik_km)
        # self.v7 = h.Vector().record(self.soma(0.5)._ref_ik_k2)
        # self.v8 = h.Vector().record(self.soma(0.5)._ref_ik_kahp_slower)
        # self.v9 = h.Vector().record(self.soma(0.5)._ref_ica_cal)

        # ---------------dend----------------
        for mechanism_d in ['Nafin', 'kdrin', 'kapin', 'pas', 'nap']:
            self.dend.insert(mechanism_d)
            self.dend1.insert(mechanism_d)
            self.dend2.insert(mechanism_d)
            self.dend3.insert(mechanism_d)
            self.dend4.insert(mechanism_d)

            # print(mechanism_d)

        # self.dend(0.5).naf2.gbar =   0.2
        self.dend(0.5).Nafin.gnafbar = 0.00018 * 10
        self.dend(0.5).kdrin.gkdrbar = 0.018
        self.dend(0.5).kapin.gkabar = 0.000032 * 15 * 10
        self.dend(0.5).nap.gnapbar = 0.000018
        self.dend(0.5).pas.g = 1 / 100
        self.dend(0.5).pas.e = -73
        self.dend.Ra = 150

        self.dend1(0.5).Nafin.gnafbar = 0.00018 * 10
        self.dend1(0.5).kdrin.gkdrbar = 0.018 * 0.5
        self.dend1(0.5).kapin.gkabar = 0.000032 * 15 * 10
        self.dend1(0.5).pas.g = 1 / 100
        self.dend1(0.5).pas.e = -73
        self.dend1.Ra = 150
        self.dend1(0.5).nap.gnapbar = 0.000018

        self.dend2(0.5).Nafin.gnafbar = 0.00018 * 10
        self.dend2(0.5).kdrin.gkdrbar = 0.018 * 0.5
        self.dend2(0.5).kapin.gkabar = 0.000032 * 15 * 10
        self.dend2(0.5).pas.g = 1 / 100
        self.dend2(0.5).pas.e = -73
        self.dend2.Ra = 150
        self.dend2(0.5).nap.gnapbar = 0.000018

        self.dend3(0.5).Nafin.gnafbar = 0.00018 * 10
        self.dend3(0.5).kdrin.gkdrbar = 0.018 * 0.5
        self.dend3(0.5).kapin.gkabar = 0.000032 * 15 * 10
        self.dend3(0.5).pas.g = 1 / 100
        self.dend3(0.5).pas.e = -73
        self.dend3.Ra = 150
        self.dend3(0.5).nap.gnapbar = 0.000018

        self.dend4(0.5).Nafin.gnafbar = 0.00018 * 10
        self.dend4(0.5).kdrin.gkdrbar = 0.018 * 0.5
        self.dend4(0.5).kapin.gkabar = 0.000032 * 15 * 10
        self.dend4(0.5).pas.g = 1 / 100
        self.dend4(0.5).pas.e = -73
        self.dend4.Ra = 150
        self.dend4(0.5).nap.gnapbar = 0.000018

        self.vd1 = h.Vector().record(self.dend(0.5)._ref_ina_Nafin)
        # self.vd2 = h.Vector().record(self.dend(0.5)._ref_ina_napf_spinstell)
        self.vd3 = h.Vector().record(self.dend(0.5)._ref_ik_kdrin)
        self.vd4 = h.Vector().record(self.dend(0.5)._ref_ik_kapin)

        # ---------------axon----------------
        for mechanism_a in ['Nafin', 'kdrin', 'pas']:
            self.axon.insert(mechanism_a)
            # print(mechanism_a)

        self.axon(0.5).Nafin.gnafbar = 0.5
        self.axon(0.5).kdrin.gkdrbar = 0.001
        self.axon(0.5).pas.g = 0.0002
        self.axon(0.5).pas.e = -73
        self.axon.Ra = 100
        self.axon.cm = 1.2

        for sec in self.all:
            sec.cm = 1.2
           # sec.cm = 0.9
            sec.ena = 50.
            sec.ek = -90
           # ek = -100.
            #e = -65.
            #ena = 50.
            #vca = 125.
        '''

        self.n_km = h.Vector().record(self.dend(0.5).km._ref_n)
        self.h_cat = h.Vector().record(self.dend(0.5).cat._ref_h)
        self.h_k2 = h.Vector().record(self.dend(0.5).k2._ref_h)
        self.h_ka = h.Vector().record(self.dend(0.5).ka._ref_h)
        #self.h_naf2 = h.Vector().record(self.dend(0.5).naf2._ref_h)
        self.m_ar = h.Vector().record(self.dend(0.5).ar._ref_m)
        self.m_cal = h.Vector().record(self.dend(0.5).cal._ref_m)
        self.m_cat = h.Vector().record(self.dend(0.5).cat._ref_m)
        self.m_k2 = h.Vector().record(self.dend(0.5).k2._ref_m)
        self.m_kahp_slower = h.Vector().record(self.dend(0.5).kahp_slower._ref_m)
        self.m_ka = h.Vector().record(self.dend(0.5).ka._ref_m)
        self.m_kc_fast = h.Vector().record(self.dend(0.5).kc_fast._ref_m)
        self.m_kdr_fs = h.Vector().record(self.dend(0.5).kdr_fs._ref_m)
        #self.m_naf2 = h.Vector().record(self.dend(0.5).naf2._ref_m)
        self.m_nap = h.Vector().record(self.dend(0.5).nap._ref_m)

        #self.nmh_list_dend =[self.n_km, self.h_cat, self.h_k2, self.h_ka, self.h_naf2, self.m_ar, self.m_cal, 
        #                    self.m_cat, self.m_k2, self.m_kahp_slower, self.m_ka, self.m_kc_fast, self.m_kdr_fs, self.m_naf2, self.m_nap ]

        self.m_k2_axon = h.Vector().record(self.axon(0.5).k2._ref_m)
        self.m_ka_axon = h.Vector().record(self.axon(0.5).ka._ref_m)
        self.m_kdr_fs_axon = h.Vector().record(self.axon(0.5).kdr_fs._ref_m)
        self.m_naf2_axon = h.Vector().record(self.axon(0.5).naf2._ref_m)
        self.h_k2_axon = h.Vector().record(self.axon(0.5).k2._ref_h)
        self.h_ka_axon = h.Vector().record(self.axon(0.5).ka._ref_h)
        self.h_naf2_axon = h.Vector().record(self.axon(0.5).naf2._ref_h)

        self.nmh_list_axon = [self.m_k2_axon, self.m_ka_axon, self.m_kdr_fs_axon, self.m_naf2_axon, self.h_k2_axon, self.h_ka_axon,self.h_naf2_axon]
        '''
        self.k_vec = h.Vector().record(self.soma(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.soma(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.soma(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.soma(0.5)._ref_ki)
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_vext[0])

        self.cyt = rxd.Region(self.all, name='cyt', nrn_region='i', dx=1.0,
                               geometry=rxd.FractionalVolume(0.9, surface_fraction=1.0))
        self.na = rxd.Species([self.cyt], name='na', charge=1, d=1.0, initial=10)
        self.k = rxd.Species([self.cyt], name='k', charge=1, d=1.0, initial=148)
        self.k_i = self.k[self.cyt]

        self.ca = rxd.Species([self.cyt], d=0.08, name='ca', charge=2, initial=1.e-4, atolscale=1e-6)
       

         #self.cl_vec = h.Vector().record(self.soma(0.5)._ref_icl)
        #self.cl_concentration = h.Vector().record(self.soma(0.5)._ref_cli)



        #------for test-----------
        #self.stim = h.IClamp(self.soma(0.5))
        #self.stim.delay = 50
        #self.stim.dur = 1
        #self.stim.amp = 1
        #print(self.id)
        #print(self.axon.psection())

class Axax23(Cell): #
    def __init__(self, x, y, z, num):
        super().__init__(x , y, z, num)
        self.id = 2
        self.Excitatory = -1
        self.name = 'superficial interneurons axoaxonic'

        # ---------------soma----------------
        for mechanism_s in ['extracellular', 'Nafin', 'kdrin', 'IKsin', 'hin', 'kapin', 'canin', 'kctin', 'cadynin', 'nap',
                            'pas']:
            self.soma.insert(mechanism_s)



        self.soma(0.5).Nafin.gnafbar = 0.75
        self.soma(0.5).kdrin.gkdrbar = 0.001
        self.soma(0.5).IKsin.gKsbar = 0.000725 * 0.1
        self.soma(0.5).hin.gbar = 0.00001
        self.soma(0.5).kapin.gkabar = 0.0032 * 15
        self.soma(0.5).canin.gcalbar = 0.0003
        self.soma(0.5).kctin.gkcbar = 0.0001
        self.soma(0.5).pas.g = 0.002
        self.soma(0.5).pas.e = -70
        self.soma.Ra = 100
        self.soma(0.5).nap.gnapbar = 0.000018

        self.v1 = h.Vector().record(self.soma(0.5)._ref_ina_Nafin)
        # self.v2 = h.Vector().record(self.soma(0.5)._ref_ina_nap)
        self.v3 = h.Vector().record(self.soma(0.5)._ref_ik_kdrin)
        self.v4 = h.Vector().record(self.soma(0.5)._ref_ik_IKsin)
        # self.v5 = h.Vector().record(self.soma(0.5)._ref_ik_kc_fast)
        # self.v6 = h.Vector().record(self.soma(0.5)._ref_ik_km)
        # self.v7 = h.Vector().record(self.soma(0.5)._ref_ik_k2)
        # self.v8 = h.Vector().record(self.soma(0.5)._ref_ik_kahp_slower)
        # self.v9 = h.Vector().record(self.soma(0.5)._ref_ica_cal)

        # ---------------dend----------------
        for mechanism_d in ['Nafin', 'kdrin', 'kapin', 'pas','nap']:
            self.dend.insert(mechanism_d)
            self.dend1.insert(mechanism_d)
            self.dend2.insert(mechanism_d)
            self.dend3.insert(mechanism_d)
            self.dend4.insert(mechanism_d)

            # print(mechanism_d)

        # self.dend(0.5).naf2.gbar =   0.2
        self.dend(0.5).Nafin.gnafbar = 0.00018 * 10
        self.dend(0.5).kdrin.gkdrbar = 0.018
        self.dend(0.5).kapin.gkabar = 0.000032 #* 15 * 10
        self.dend(0.5).nap.gnapbar = 0.000018
        self.dend(0.5).pas.g = 1 / 100
        self.dend(0.5).pas.e = -73
        self.dend.Ra = 150

        self.dend1(0.5).Nafin.gnafbar = 0.00018 * 10
        self.dend1(0.5).kdrin.gkdrbar = 0.018 * 0.5
        self.dend1(0.5).kapin.gkabar = 0.000032 #* 15 * 10
        self.dend1(0.5).pas.g = 1 / 100
        self.dend1(0.5).pas.e = -73
        self.dend1.Ra = 150
        self.dend1(0.5).nap.gnapbar = 0.000018

        self.dend2(0.5).Nafin.gnafbar = 0.00018 * 10
        self.dend2(0.5).kdrin.gkdrbar = 0.018 * 0.5
        self.dend2(0.5).kapin.gkabar = 0.000032 #* 15 * 10
        self.dend2(0.5).pas.g = 1 / 100
        self.dend2(0.5).pas.e = -73
        self.dend2.Ra = 150
        self.dend2(0.5).nap.gnapbar = 0.000018

        self.dend3(0.5).Nafin.gnafbar = 0.00018 * 10
        self.dend3(0.5).kdrin.gkdrbar = 0.018 * 0.5
        self.dend3(0.5).kapin.gkabar = 0.000032 #* 15 * 10
        self.dend3(0.5).pas.g = 1 / 100
        self.dend3(0.5).pas.e = -73
        self.dend3.Ra = 150
        self.dend3(0.5).nap.gnapbar = 0.000018

        self.dend4(0.5).Nafin.gnafbar = 0.00018 * 10
        self.dend4(0.5).kdrin.gkdrbar = 0.018 * 0.5
        self.dend4(0.5).kapin.gkabar = 0.000032 #* 15 * 10
        self.dend4(0.5).pas.g = 1 / 100
        self.dend4(0.5).pas.e = -73
        self.dend4.Ra = 150
        self.dend4(0.5).nap.gnapbar = 0.000018

        self.vd1 = h.Vector().record(self.dend(0.5)._ref_ina_Nafin)
        # self.vd2 = h.Vector().record(self.dend(0.5)._ref_ina_napf_spinstell)
        self.vd3 = h.Vector().record(self.dend(0.5)._ref_ik_kdrin)
        self.vd4 = h.Vector().record(self.dend(0.5)._ref_ik_kapin)

        # ---------------axon----------------
        for mechanism_a in ['Nafin', 'kdrin', 'pas']:
            self.axon.insert(mechanism_a)
            # print(mechanism_a)

        self.axon(0.5).Nafin.gnafbar = 0.4
        self.axon(0.5).kdrin.gkdrbar = 0.001
        self.axon(0.5).pas.g = 0.0002
        self.axon(0.5).pas.e = -73
        self.axon.Ra = 100
        self.axon.cm = 1.2
        
        for sec in self.all:        
            sec.cm = 0.9
            sec.ena =   50.
            #sec.eca =   125.

        self.k_vec = h.Vector().record(self.soma(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.soma(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.soma(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.soma(0.5)._ref_ki)

        self.v_vec = h.Vector().record(self.soma(0.5)._ref_vext[0])
        self.cyt = rxd.Region(self.all, name='cyt', nrn_region='i', dx=1.0, geometry=rxd.FractionalVolume(0.9, surface_fraction=1.0))
        self.na = rxd.Species([self.cyt], name='na', charge=1, d=1.0, initial=10)
        self.k = rxd.Species([self.cyt], name='k', charge=1, d=1.0, initial=148)
        self.k_i= self.k[self.cyt]
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_vext[0])
        self.ca = rxd.Species([self.cyt], d=0.08, name='ca', charge=2, initial=1.e-4, atolscale=1e-6)
        #------for test-----------
        #self.stim = h.IClamp(self.soma(0.5))
        #self.stim.delay = 50
        #self.stim.dur = 1
        #self.stim.amp = 1
        #print(self.id)
    


class LTS23(Cell):  #
    def __init__(self, x, y, z, num):
        super().__init__(x , y, z, num)
        self.id = 3
        self.Excitatory = -1
        self.name = 'superficial interneurons low threshold spiking'

        # ---------------soma----------------
        for mechanism_s in ['extracellular', 'Nafin', 'kdrin', 'IKsin', 'hin', 'kapin', 'canin', 'kctin', 'cadynin', 'nap',
                            'pas']:
            self.soma.insert(mechanism_s)

        self.soma(0.5).Nafin.gnafbar = 0.45
        self.soma(0.5).kdrin.gkdrbar = 0.0001
        self.soma(0.5).IKsin.gKsbar = 0.000725 * 0.1
        self.soma(0.5).hin.gbar = 0.00001
        self.soma(0.5).kapin.gkabar = 0.0032 * 15
        self.soma(0.5).canin.gcalbar = 0.0003
        self.soma(0.5).kctin.gkcbar = 0.0001
        self.soma(0.5).pas.g = 1/100
        self.soma(0.5).pas.e = -73
        self.soma.Ra = 150
        self.soma.cm = 1.2
        self.soma(0.5).nap.gnapbar = 0.000018



        # ---------------dend----------------
        for mechanism_d in ['Nafin', 'kdrin', 'kapin', 'pas', 'nap']:
            self.dend.insert(mechanism_d)
            self.dend1.insert(mechanism_d)
            self.dend2.insert(mechanism_d)
            self.dend3.insert(mechanism_d)
            self.dend4.insert(mechanism_d)

            # print(mechanism_d)

        # self.dend(0.5).naf2.gbar =   0.2
        self.dend(0.5).Nafin.gnafbar = 0.0018 * 5
        self.dend(0.5).kdrin.gkdrbar = 0.018
        self.dend(0.5).kapin.gkabar = 0.000032 #* 15 * 10
        self.dend(0.5).nap.gnapbar = 0.000018
        self.dend(0.5).pas.g = 1 / 100
        self.dend(0.5).pas.e = -73
        self.dend.Ra = 150

        self.dend1(0.5).Nafin.gnafbar = 0.0018 * 5
        self.dend1(0.5).kdrin.gkdrbar = 0.018 * 0.5
        self.dend1(0.5).kapin.gkabar = 0.000032 #* 15 * 10
        self.dend1(0.5).pas.g = 1 / 100
        self.dend1(0.5).pas.e = -73
        self.dend1.Ra = 150
        self.dend1(0.5).nap.gnapbar = 0.000018

        self.dend2(0.5).Nafin.gnafbar = 0.0018 * 5
        self.dend2(0.5).kdrin.gkdrbar = 0.018 * 0.5
        self.dend2(0.5).kapin.gkabar = 0.000032 #* 15 * 10
        self.dend2(0.5).pas.g = 1 / 100
        self.dend2(0.5).pas.e = -73
        self.dend2.Ra = 150
        self.dend2(0.5).nap.gnapbar = 0.000018

        self.dend3(0.5).Nafin.gnafbar = 0.0018 * 5
        self.dend3(0.5).kdrin.gkdrbar = 0.018 * 0.5
        self.dend3(0.5).kapin.gkabar = 0.000032 #* 15 * 10
        self.dend3(0.5).pas.g = 1 / 100
        self.dend3(0.5).pas.e = -73
        self.dend3.Ra = 150
        self.dend3(0.5).nap.gnapbar = 0.000018

        self.dend4(0.5).Nafin.gnafbar = 0.0018 * 5
        self.dend4(0.5).kdrin.gkdrbar = 0.018 * 0.5
        self.dend4(0.5).kapin.gkabar = 0.000032 #* 15 * 10
        self.dend4(0.5).pas.g = 1 / 100
        self.dend4(0.5).pas.e = -73
        self.dend4.Ra = 150
        self.dend4(0.5).nap.gnapbar = 0.000018

        self.vd1 = h.Vector().record(self.dend(0.5)._ref_ina_Nafin)
        # self.vd2 = h.Vector().record(self.dend(0.5)._ref_ina_napf_spinstell)
        self.vd3 = h.Vector().record(self.dend(0.5)._ref_ik_kdrin)
        self.vd4 = h.Vector().record(self.dend(0.5)._ref_ik_kapin)

        # ---------------axon----------------
        for mechanism_a in ['Nafin', 'kdrin', 'pas']:
            self.axon.insert(mechanism_a)
            # print(mechanism_a)

        self.axon(0.5).Nafin.gnafbar = 0.4
        self.axon(0.5).kdrin.gkdrbar = 0.001
        self.axon(0.5).pas.g = 0.0002
        self.axon(0.5).pas.e = -73
        self.axon.Ra = 100
        self.axon.cm = 1.2

        for sec in self.all:        
            #sec.cm = 1
            sec.ena = 50.

        self.k_vec = h.Vector().record(self.soma(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.soma(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.soma(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.soma(0.5)._ref_ki)
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_vext[0])
        self.cyt = rxd.Region(self.all, name='cyt', nrn_region='i', dx=1.0,
                              geometry=rxd.FractionalVolume(0.9, surface_fraction=1.0))
        self.na = rxd.Species([self.cyt], name='na', charge=1, d=1.0, initial=10)
        self.k = rxd.Species([self.cyt], name='k', charge=1, d=1.0, initial=148)
        self.k_i = self.k[self.cyt]
        self.ca = rxd.Species([self.cyt], d=0.08, name='ca', charge=2, initial=1.e-4, atolscale=1e-6)
        #------for test-----------
        #self.stim = h.IClamp(self.soma(0.5))
        #self.stim.delay = 50
        #self.stim.dur = 1
        #self.stim.amp = 1
        #print(self.id)

class Spinstel4(Cell):  #
    def __init__(self, x, y, z, num):
        super().__init__(x , y, z, num)
        self.id = 4
        self.Excitatory = 1
        self.name = 'spiny stellate'
        
        for mechanism_s in ['extracellular', 'Naf', 'nap', 'calc', 'cal', 'can', 'car', 'cat', 'kdrpr', 'IKs', 'kad',
                            'h',
                            'kca', 'ican', 'cadyn',
                            'pas']:
            # print(mechanism_s)
            self.soma.insert(mechanism_s)

        self.soma(0.5).Naf.gnafbar = 0.018 * 3
        self.soma(0.5).nap.gnapbar = 0.000018
        self.soma(0.5).calc.gcabar = 0.0001 * 0.1
        self.soma(0.5).cal.gcalbar = 0.0001 * 0.3
        self.soma(0.5).can.gcabar = 0.0002 * 0.1
        self.soma(0.5).car.gcabar = 0.000001 * 0.3 * 0.1
        self.soma(0.5).cat.gcatbar = 0.0002 * 0.3 * 0.1
        self.soma(0.5).kdrpr.gkdrbar = 0.018 * 0.3
        self.soma(0.5).IKs.gKsbar = 0.0012 * 0.5
        self.soma(0.5).kad.gkabar = 0.0007
        self.soma(0.5).kca.gbar = 0.005 * 5
        self.soma(0.5).h.gbar = 1.8e-5 * 0.5
        self.soma(0.5).ican.gbar = 0.001 * 0.07 * 0
        self.soma(0.5).pas.g = 0.01
        self.soma(0.5).pas.e = -65
        self.soma.Ra = 100

        # self.v1 = h.Vector().record(self.soma(0.5)._ref_ina_Nafin)
        # self.v2 = h.Vector().record(self.soma(0.5)._ref_ina_nap)
        # self.v3 = h.Vector().record(self.soma(0.5)._ref_ik_kdrin)
        # self.v4 = h.Vector().record(self.soma(0.5)._ref_ik_IKsin)
        # self.v5 = h.Vector().record(self.soma(0.5)._ref_ik_kc_fast)
        # self.v6 = h.Vector().record(self.soma(0.5)._ref_ik_km)
        # self.v7 = h.Vector().record(self.soma(0.5)._ref_ik_k2)
        # self.v8 = h.Vector().record(self.soma(0.5)._ref_ik_kahp_slower)
        # self.v9 = h.Vector().record(self.soma(0.5)._ref_ica_cal)

        # ---------------dend----------------
        for mechanism_d in ['Naf', 'nap', 'calc', 'cal', 'can', 'car', 'cat', 'kdrpr', 'IKs', 'kad', 'h', 'kca', 'ican',
                            'cadyn', 'pas']:
            self.dend.insert(mechanism_d)
            self.dend1.insert(mechanism_d)
            self.dend2.insert(mechanism_d)
            self.dend3.insert(mechanism_d)
            self.dend4.insert(mechanism_d)

            # print(mechanism_d)

        self.dend(0.5).Naf.gnafbar = 0.018 * 0.1
        self.dend(0.5).nap.gnapbar = 0.000018
        self.dend(0.5).calc.gcabar = 0.0001 * 0.1  #
        self.dend(0.5).cal.gcalbar = 0.0001 * 0.3  #
        self.dend(0.5).can.gcabar = 0.0002 * 0.3
        self.dend(0.5).car.gcabar = 0.000001 * 0.3 * 0.1 * 0.3  #
        self.dend(0.5).cat.gcatbar = 0.0002 * 0.3 * 0.1  #
        self.dend(0.5).kdrpr.gkdrbar = 0.018 * 0.09
        self.dend(0.5).IKs.gKsbar = 0.0012
        self.dend(0.5).kad.gkabar = 0.0007
        self.dend(0.5).kca.gbar = 0.005 * 5 * 0.001  #
        self.dend(0.5).h.gbar = 1.8e-5 * 0.5  #
        self.dend(0.5).ican.gbar = 0.001 * 0.07 * 0.1  #
        self.dend(0.5).pas.g = 0.01
        self.dend(0.5).pas.e = -65
        self.dend.Ra = 150

        self.dend1(0.5).Naf.gnafbar = 0.018 * 0.4
        self.dend1(0.5).nap.gnapbar = 0.000018  # * 3
        self.dend1(0.5).calc.gcabar = 0.0001 * 0.1  #
        self.dend1(0.5).cal.gcalbar = 0.0001 * 0.3  #
        self.dend1(0.5).can.gcabar = 0.0002 * 0.3
        self.dend1(0.5).car.gcabar = 0.000001 * 0.3 * 0.1 * 0.3  #
        self.dend1(0.5).cat.gcatbar = 0.0002 * 0.3 * 0.1  #
        self.dend1(0.5).kdrpr.gkdrbar = 0.018 * 0.09
        self.dend1(0.5).IKs.gKsbar = 0.0012
        self.dend1(0.5).kad.gkabar = 0.0007
        self.dend1(0.5).kca.gbar = 0.005 * 5 * 0.0001  #
        self.dend1(0.5).h.gbar = 1.8e-5 * 0.5  #
        self.dend1(0.5).ican.gbar = 0.001 * 0.07 * 0.1  #
        self.dend1(0.5).pas.g = 0.01
        self.dend1(0.5).pas.e = -65
        self.dend1.Ra = 150

        self.dend2(0.5).Naf.gnafbar = 0.018 * 0.1
        self.dend2(0.5).nap.gnapbar = 0.000018
        self.dend2(0.5).calc.gcabar = 0.0001 * 0.1  #
        self.dend2(0.5).cal.gcalbar = 0.0001 * 0.3  #
        self.dend2(0.5).can.gcabar = 0.0002 * 0.3
        self.dend2(0.5).car.gcabar = 0.000001 * 0.3 * 0.1 * 0.3  #
        self.dend2(0.5).cat.gcatbar = 0.0002 * 0.3 * 0.1  #
        self.dend2(0.5).kdrpr.gkdrbar = 0.018 * 0.09
        self.dend2(0.5).IKs.gKsbar = 0.0012
        self.dend2(0.5).kad.gkabar = 0.0007
        self.dend2(0.5).kca.gbar = 0.005 * 5 * 0.001  #
        self.dend2(0.5).h.gbar = 1.8e-5 * 0.5  #
        self.dend2(0.5).ican.gbar = 0.001 * 0.07 * 0.1  #
        self.dend2(0.5).pas.g = 0.01
        self.dend2(0.5).pas.e = -65
        self.dend2.Ra = 150

        self.dend3(0.5).Naf.gnafbar = 0.018 * 0.1
        self.dend3(0.5).nap.gnapbar = 0.000018
        self.dend3(0.5).calc.gcabar = 0.0001 * 0.1  #
        self.dend3(0.5).cal.gcalbar = 0.0001 * 0.3  #
        self.dend3(0.5).can.gcabar = 0.0002 * 0.3
        self.dend3(0.5).car.gcabar = 0.000001 * 0.3 * 0.1 * 0.3  #
        self.dend3(0.5).cat.gcatbar = 0.0002 * 0.3 * 0.1  #
        self.dend3(0.5).kdrpr.gkdrbar = 0.018 * 0.09
        self.dend3(0.5).IKs.gKsbar = 0.0012
        self.dend3(0.5).kad.gkabar = 0.0007
        self.dend3(0.5).kca.gbar = 0.005 * 5 * 0.001  #
        self.dend3(0.5).h.gbar = 1.8e-5 * 0.5  #
        self.dend3(0.5).ican.gbar = 0.001 * 0.07 * 0.1  #
        self.dend3(0.5).pas.g = 0.01
        self.dend3(0.5).pas.e = -65
        self.dend3.Ra = 150

        self.dend4(0.5).Naf.gnafbar = 0.018 * 0.1
        self.dend4(0.5).nap.gnapbar = 0.000018
        self.dend4(0.5).calc.gcabar = 0.0001 * 0.1  #
        self.dend4(0.5).cal.gcalbar = 0.0001 * 0.3  #
        self.dend4(0.5).can.gcabar = 0.0002 * 0.3
        self.dend4(0.5).car.gcabar = 0.000001 * 0.3 * 0.1 * 0.3  #
        self.dend4(0.5).cat.gcatbar = 0.0002 * 0.3 * 0.1  #
        self.dend4(0.5).kdrpr.gkdrbar = 0.018 * 0.09
        self.dend4(0.5).IKs.gKsbar = 0.0012
        self.dend4(0.5).kad.gkabar = 0.0007
        self.dend4(0.5).kca.gbar = 0.005 * 5 * 0.001  #
        self.dend4(0.5).h.gbar = 1.8e-5 * 0.5  #
        self.dend4(0.5).ican.gbar = 0.001 * 0.07 * 0.1  #
        self.dend4(0.5).pas.g = 0.01
        self.dend4(0.5).pas.e = -65
        self.dend4.Ra = 150

        # ---------------axon----------------
        for mechanism_a in ['Nafin', 'kdrin', 'pas']:
            self.axon.insert(mechanism_a)
            # print(mechanism_a)

        self.axon(0.5).Nafin.gnafbar = 0.4
        self.axon(0.5).kdrin.gkdrbar = 0.001
        self.axon(0.5).pas.g = 0.0002
        self.axon(0.5).pas.e = -73
        self.axon.Ra = 100
        self.axon.cm = 1.2

        for sec in self.all:
            sec.cm = 0.9
            sec.ena = 50.
            sec.ek = -95.


        self.k_vec = h.Vector().record(self.soma(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.soma(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.soma(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.soma(0.5)._ref_ki)
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_vext[0])

        self.cyt = rxd.Region(self.all, name='cyt', nrn_region='i', dx=1.0,
                              geometry=rxd.FractionalVolume(0.9, surface_fraction=1.0))
        self.na = rxd.Species([self.cyt], name='na', charge=1, d=1.0, initial=10)
        self.k = rxd.Species([self.cyt], name='k', charge=1, d=1.0, initial=148)
        self.k_i = self.k[self.cyt]
        self.ca = rxd.Species([self.cyt], d=0.08, name='ca', charge=2, initial=1.e-4, atolscale=1e-6)


class EpilepsySpinstel4(Cell):  #
    def __init__(self, x, y, z, num):
        super().__init__(x, y, z, num)
        self.id = 4
        self.Excitatory = 1
        self.name = 'spiny stellate'

        for mechanism_s in ['extracellular', 'naf2_cc', 'pas', 'napf_spinstell', 'kdr_fs_cc', 'kc_fast_cc', 'ka_cc',
                        'km_cc', 'k2_cc', 'kahp_slower', 'cal_cc', 'cat_cc', 'ar', 'cad_cc']:
            self.soma.insert(mechanism_s)
        # print(mechanism_s)

        self.soma(0.5).naf2_cc.gbar = 0.65
        self.soma(0.5).napf_spinstell.gbar = 0.0002
        self.soma(0.5).kdr_fs_cc.gbar = 0.1 * 10
        self.soma(0.5).kc_fast_cc.gbar = 0.001 * 10
        self.soma(0.5).ka_cc.gbar = 0.03
        self.soma(0.5).km_cc.gbar = 0.00375
        self.soma(0.5).k2_cc.gbar = 0.0001
        self.soma(0.5).kahp_slower.gbar = 0.0001
        self.soma(0.5).cal_cc.gbar = 0.0005
        self.soma(0.5).cat_cc.gbar = 0.0001
        self.soma(0.5).ar.gbar = 0.00025
        self.soma(0.5).cad_cc.beta = 0.02
        self.soma(0.5).cad_cc.phi = 260000.
        self.soma(0.5).pas.g = 0.001
        self.soma(0.5).pas.e = -65
        self.soma.Ra = 150.

        # ---------------dend----------------
        for mechanism_d in ['naf2_cc', 'napf_spinstell', 'pas', 'kdr_fs_cc', 'kc_fast_cc', 'ka_cc', 'km_cc', 'k2_cc',
                            'kahp_slower', 'cal_cc', 'cat_cc', 'ar', 'cad_cc']:
            self.dend.insert(mechanism_d)
            self.dend1.insert(mechanism_d)
            self.dend2.insert(mechanism_d)
            self.dend3.insert(mechanism_d)
            self.dend4.insert(mechanism_d)
            # print(mechanism_d)

        self.dend(0.5).naf2_cc.gbar = 0.0075
        self.dend(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend(0.5).kc_fast_cc.gbar = 0.01
        self.dend(0.5).ka_cc.gbar = 0.03
        self.dend(0.5).km_cc.gbar = 0.00375
        self.dend(0.5).k2_cc.gbar = 0.0001
        self.dend(0.5).kahp_slower.gbar = 0.0001
        self.dend(0.5).cal_cc.gbar = 0.0005
        self.dend(0.5).cat_cc.gbar = 0.0001
        self.dend(0.5).ar.gbar = 0.00025
        self.dend(0.5).cad_cc.beta = 0.05
        self.dend(0.5).cad_cc.phi = 260000.
        self.dend(0.5).pas.g = 0.02
        self.dend(0.5).pas.e = -65
        self.dend.Ra = 250.

        self.dend1(0.5).naf2_cc.gbar = 0.0075
        self.dend1(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend1(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend1(0.5).kc_fast_cc.gbar = 0.01
        self.dend1(0.5).ka_cc.gbar = 0.03
        self.dend1(0.5).km_cc.gbar = 0.00375
        self.dend1(0.5).k2_cc.gbar = 0.0001
        self.dend1(0.5).kahp_slower.gbar = 0.0001
        self.dend1(0.5).cal_cc.gbar = 0.0005
        self.dend1(0.5).cat_cc.gbar = 0.0001
        self.dend1(0.5).ar.gbar = 0.00025
        self.dend1(0.5).cad_cc.beta = 0.05
        self.dend1(0.5).cad_cc.phi = 260000.
        self.dend1(0.5).pas.g = 0.02
        self.dend1(0.5).pas.e = -65
        self.dend1.Ra = 250.

        self.dend2(0.5).naf2_cc.gbar = 0.0075
        self.dend2(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend2(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend2(0.5).kc_fast_cc.gbar = 0.01
        self.dend2(0.5).ka_cc.gbar = 0.03
        self.dend2(0.5).km_cc.gbar = 0.00375
        self.dend2(0.5).k2_cc.gbar = 0.0001
        self.dend2(0.5).kahp_slower.gbar = 0.0001
        self.dend2(0.5).cal_cc.gbar = 0.0005
        self.dend2(0.5).cat_cc.gbar = 0.0001
        self.dend2(0.5).ar.gbar = 0.00025
        self.dend2(0.5).cad_cc.beta = 0.05
        self.dend2(0.5).cad_cc.phi = 260000.
        self.dend2(0.5).pas.g = 0.02
        self.dend2(0.5).pas.e = -65
        self.dend2.Ra = 250.

        self.dend3(0.5).naf2_cc.gbar = 0.0075
        self.dend3(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend3(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend3(0.5).kc_fast_cc.gbar = 0.01
        self.dend3(0.5).ka_cc.gbar = 0.03
        self.dend3(0.5).km_cc.gbar = 0.00375
        self.dend3(0.5).k2_cc.gbar = 0.0001
        self.dend3(0.5).kahp_slower.gbar = 0.0001
        self.dend3(0.5).cal_cc.gbar = 0.0005
        self.dend3(0.5).cat_cc.gbar = 0.0001
        self.dend3(0.5).ar.gbar = 0.00025
        self.dend3(0.5).cad_cc.beta = 0.05
        self.dend3(0.5).cad_cc.phi = 260000.
        self.dend3(0.5).pas.g = 0.02
        self.dend3(0.5).pas.e = -65
        self.dend3.Ra = 250.

        self.dend4(0.5).naf2_cc.gbar = 0.0075
        self.dend4(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend4(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend4(0.5).kc_fast_cc.gbar = 0.01
        self.dend4(0.5).ka_cc.gbar = 0.03
        self.dend4(0.5).km_cc.gbar = 0.00375
        self.dend4(0.5).k2_cc.gbar = 0.0001
        self.dend4(0.5).kahp_slower.gbar = 0.0001
        self.dend4(0.5).cal_cc.gbar = 0.0005
        self.dend4(0.5).cat_cc.gbar = 0.0001
        self.dend4(0.5).ar.gbar = 0.00025
        self.dend4(0.5).cad_cc.beta = 0.05
        self.dend4(0.5).cad_cc.phi = 260000.
        self.dend4(0.5).pas.g = 0.02
        self.dend4(0.5).pas.e = -65
        self.dend4.Ra = 250.

        # self.vd1 = h.Vector().record(self.dend(0.5)._ref_ina_naf2)
        # self.vd2 = h.Vector().record(self.dend(0.5)._ref_ina_napf_spinstell)
        # self.vd3 = h.Vector().record(self.dend(0.5)._ref_ik_kdr_fs)
        # self.vd4 = h.Vector().record(self.dend(0.5)._ref_ik_ka)
        # self.vd5 = h.Vector().record(self.dend(0.5)._ref_ik_kc_fast)
        # self.vd7 = h.Vector().record(self.dend(0.5)._ref_ik_k2)
        # self.vd8 = h.Vector().record(self.dend(0.5)._ref_ik_kahp_slower)
        # self.vd9 = h.Vector().record(self.dend(0.5)._ref_ica_cal)

        # ---------------axon----------------
        for mechanism_a in ['naf2_cc', 'kdr_fs_cc', 'ka_cc', 'k2_cc', 'pas']:
            self.axon.insert(mechanism_a)
            # print(mechanism_a)

        self.axon(0.5).naf2_cc.gbar = 0.1 * 4
        self.axon(0.5).kdr_fs_cc.gbar = 0.9
        self.axon(0.5).ka_cc.gbar = 0.002
        self.axon(0.5).k2_cc.gbar = 0.1
        self.axon(0.5).pas.g = 0.01
        self.axon(0.5).pas.e = -65
        self.axon.Ra = 100.

        for sec in self.all:
            sec.cm = 0.9
            sec.ena = 50.
            sec.ek = -90

        self.k_vec = h.Vector().record(self.soma(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.soma(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.soma(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.soma(0.5)._ref_ki)
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_vext[0])

        self.cyt = rxd.Region(self.all, name='cyt', nrn_region='i', dx=1.0,
                              geometry=rxd.FractionalVolume(0.9, surface_fraction=1.0))
        self.na = rxd.Species([self.cyt], name='na', charge=1, d=1.0, initial=10)
        self.k = rxd.Species([self.cyt], name='k', charge=1, d=1.0, initial=148)
        self.k_i = self.k[self.cyt]
        self.ca = rxd.Species([self.cyt], d=0.08, name='ca', charge=2, initial=1.e-4, atolscale=1e-6)


class Bask4(Cell):
    def __init__(self, x, y, z, num):
        super().__init__(x, y, z, num)
        self.id = 16
        self.Excitatory = -1
        self.name = 'superficial interneurons basket L4'

        # ---------------soma----------------
        for mechanism_s in ['extracellular', 'Nafin', 'kdrin', 'IKsin', 'hin', 'kapin', 'canin', 'kctin', 'cadynin',
                            'pas']:
            self.soma.insert(mechanism_s)

        self.soma(0.5).Nafin.gnafbar = 0.5
        self.soma(0.5).kdrin.gkdrbar = 0.001 *100
        self.soma(0.5).IKsin.gKsbar = 0.000725 * 0.1
        self.soma(0.5).hin.gbar = 0.00001
        self.soma(0.5).kapin.gkabar = 0.0032 * 15
        self.soma(0.5).canin.gcalbar = 0.0003
        self.soma(0.5).kctin.gkcbar = 0.0001
        self.soma(0.5).pas.g = 0.0002
        self.soma(0.5).pas.e = -70
        self.soma.Ra = 100


        # ---------------dend----------------
        for mechanism_d in ['Nafin', 'kdrin', 'kapin', 'pas', 'nap']:
            self.dend.insert(mechanism_d)
            self.dend1.insert(mechanism_d)
            self.dend2.insert(mechanism_d)
            self.dend3.insert(mechanism_d)
            self.dend4.insert(mechanism_d)

            # print(mechanism_d)

        # self.dend(0.5).naf2.gbar =   0.2
        self.dend(0.5).Nafin.gnafbar = 0.00018 * 10
        self.dend(0.5).kdrin.gkdrbar = 0.018
        self.dend(0.5).kapin.gkabar = 0.000032 * 15 * 10
        self.dend(0.5).nap.gnapbar = 0.000018
        self.dend(0.5).pas.g = 1 / 100
        self.dend(0.5).pas.e = -73
        self.dend.Ra = 150

        self.dend1(0.5).Nafin.gnafbar = 0.00018 * 10
        self.dend1(0.5).kdrin.gkdrbar = 0.018 * 0.5
        self.dend1(0.5).kapin.gkabar = 0.000032 * 15 * 10
        self.dend1(0.5).pas.g = 1 / 100
        self.dend1(0.5).pas.e = -73
        self.dend1.Ra = 150
        self.dend1(0.5).nap.gnapbar = 0.000018

        self.dend2(0.5).Nafin.gnafbar = 0.00018 * 10
        self.dend2(0.5).kdrin.gkdrbar = 0.018 * 0.5
        self.dend2(0.5).kapin.gkabar = 0.000032 * 15 * 10
        self.dend2(0.5).pas.g = 1 / 100
        self.dend2(0.5).pas.e = -73
        self.dend2.Ra = 150
        self.dend2(0.5).nap.gnapbar = 0.000018

        self.dend3(0.5).Nafin.gnafbar = 0.00018 * 10
        self.dend3(0.5).kdrin.gkdrbar = 0.018 * 0.5
        self.dend3(0.5).kapin.gkabar = 0.000032 * 15 * 10
        self.dend3(0.5).pas.g = 1 / 100
        self.dend3(0.5).pas.e = -73
        self.dend3.Ra = 150
        self.dend3(0.5).nap.gnapbar = 0.000018

        self.dend4(0.5).Nafin.gnafbar = 0.00018 * 10
        self.dend4(0.5).kdrin.gkdrbar = 0.018 * 0.5
        self.dend4(0.5).kapin.gkabar = 0.000032 * 15 * 10
        self.dend4(0.5).pas.g = 1 / 100
        self.dend4(0.5).pas.e = -73
        self.dend4.Ra = 150
        self.dend4(0.5).nap.gnapbar = 0.000018

        self.vd1 = h.Vector().record(self.dend(0.5)._ref_ina_Nafin)
        # self.vd2 = h.Vector().record(self.dend(0.5)._ref_ina_napf_spinstell)
        self.vd3 = h.Vector().record(self.dend(0.5)._ref_ik_kdrin)
        self.vd4 = h.Vector().record(self.dend(0.5)._ref_ik_kapin)

        # ---------------axon----------------
        for mechanism_a in ['Nafin', 'kdrin', 'pas']:
            self.axon.insert(mechanism_a)
            # print(mechanism_a)

        self.axon(0.5).Nafin.gnafbar = 0.4
        self.axon(0.5).kdrin.gkdrbar = 0.001
        self.axon(0.5).pas.g = 0.0002
        self.axon(0.5).pas.e = -73
        self.axon.Ra =100
        self.axon.cm = 1.2

        for sec in self.all:
            sec.cm = 1.2
            # sec.cm = 0.9
            sec.ena = 50.
            sec.ek = -90
        self.k_vec = h.Vector().record(self.soma(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.soma(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.soma(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.soma(0.5)._ref_ki)
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_vext[0])

        self.cyt = rxd.Region(self.all, name='cyt', nrn_region='i', dx=1.0,
                              geometry=rxd.FractionalVolume(0.9, surface_fraction=1.0))
        self.na = rxd.Species([self.cyt], name='na', charge=1, d=1.0, initial=10)
        self.k = rxd.Species([self.cyt], name='k', charge=1, d=1.0, initial=148)
        self.k_i = self.k[self.cyt]

        self.ca = rxd.Species([self.cyt], d=0.08, name='ca', charge=2, initial=1.e-4, atolscale=1e-6)



class TuftIB5(Cell):
    def __init__(self, x, y, z, num):
        super().__init__(x , y, z, num)
        self.id = 5
        self.Excitatory = 1
        self.name = 'pyramidal tufted intrinsic bursting'

        # ---------------soma----------------
        for mechanism_s in ['extracellular', 'napf', 'pas', 'naf2_cc', 'kdr_fs_cc', 'kc', 'ka_cc', 'km_cc', 'k2_cc',
                            'kahp_slower', 'cal_cc', 'cat_a', 'ar', 'cad_cc']:
            self.soma.insert(mechanism_s)
            # print(mechanism_s)

        self.soma(0.5).naf2_cc.gbar = 0.6
        self.soma(0.5).napf.gbar = 0.00006
        self.soma(0.5).kdr_fs_cc.gbar = 0.5
        self.soma(0.5).ka_cc.gbar = 0.005
        self.soma(0.5).km_cc.gbar = 0.0005
        self.soma(0.5).kc.gbar = 0.01
        self.soma(0.5).k2_cc.gbar = 0.0005
        self.soma(0.5).kahp_slower.gbar = 0.0001
        self.soma(0.5).cal_cc.gbar = 0.0001
        self.soma(0.5).cat_a.gbar = 5.E-05
        self.soma(0.5).ar.gbar = 2.5E-05
        self.soma(0.5).cad_cc.beta = 0.02
        self.soma(0.5).cad_cc.phi = 10400.
        self.soma(0.5).pas.e = -70
        self.soma(0.5).pas.g = 0.001
        self.soma.Ra = 100.




        # ---------------dend----------------
        for mechanism_d in ['naf_tcr', 'napf_tcr', 'kdr_thlms','ka', 'kc', 'km', 'k2', 'kahp_slower', 'cal_thlms', 'cat_thlms', 'ar', 'cad',  'pas']:
            self.dend.insert(mechanism_d)
            self.dend1.insert(mechanism_d)
            self.dend2.insert(mechanism_d)
            self.dend3.insert(mechanism_d)
            self.dend4.insert(mechanism_d)

            # print(mechanism_d)

        # self.dend(0.5).naf2.gbar =   0.2
        self.dend(0.5).naf_tcr.gbar =   0.1
        self.dend(0.5).napf_tcr.gbar =   0.0002
        self.dend(0.5).kdr_thlms.gbar =   0.075
        self.dend(0.5).kc.gbar =   0.012
        self.dend(0.5).ka.gbar =   0.03
        self.dend(0.5).km.gbar =   0 #// 0.0005
        self.dend(0.5).k2.gbar =   0.002
        self.dend(0.5).cal_thlms.gbar =   0.0005
        self.dend(0.5).cat_thlms.gbar =   0.0005
        self.dend(0.5).ar.gbar =   0.00025
        self.dend(0.5).cad.beta  =   0.02
        self.dend(0.5).cad.phi =   52000.
        self.dend(0.5).pas.g = 1 / 100
        self.dend(0.5).pas.e = -70
        self.dend.Ra = 175

        self.dend1(0.5).naf_tcr.gbar = 0.1
        self.dend1(0.5).napf_tcr.gbar = 0.0002
        self.dend1(0.5).kdr_thlms.gbar = 0.075
        self.dend1(0.5).kc.gbar = 0.012
        self.dend1(0.5).ka.gbar = 0.03
        self.dend1(0.5).km.gbar = 0  # // 0.0005
        self.dend1(0.5).k2.gbar = 0.002
        self.dend1(0.5).cal_thlms.gbar = 0.0005
        self.dend1(0.5).cat_thlms.gbar = 0.0005
        self.dend1(0.5).ar.gbar = 0.00025
        self.dend1(0.5).cad.beta = 0.02
        self.dend1(0.5).cad.phi = 52000.
        self.dend1(0.5).pas.g = 1 / 100
        self.dend1(0.5).pas.e = -70
        self.dend1.Ra = 175

        self.dend2(0.5).naf_tcr.gbar = 0.1
        self.dend2(0.5).napf_tcr.gbar = 0.0002
        self.dend2(0.5).kdr_thlms.gbar = 0.075
        self.dend2(0.5).kc.gbar = 0.012
        self.dend2(0.5).ka.gbar = 0.03
        self.dend2(0.5).km.gbar = 0  # // 0.0005
        self.dend2(0.5).k2.gbar = 0.002
        self.dend2(0.5).cal_thlms.gbar = 0.0005
        self.dend2(0.5).cat_thlms.gbar = 0.0005
        self.dend2(0.5).ar.gbar = 0.00025
        self.dend2(0.5).cad.beta = 0.02
        self.dend2(0.5).cad.phi = 52000.
        self.dend2(0.5).pas.g = 1 / 100
        self.dend2(0.5).pas.e = -70
        self.dend2.Ra = 175

        self.dend3(0.5).naf_tcr.gbar = 0.1
        self.dend3(0.5).napf_tcr.gbar = 0.0002
        self.dend3(0.5).kdr_thlms.gbar = 0.075
        self.dend3(0.5).kc.gbar = 0.012
        self.dend3(0.5).ka.gbar = 0.03
        self.dend3(0.5).km.gbar = 0  # // 0.0005
        self.dend3(0.5).k2.gbar = 0.002
        self.dend3(0.5).cal_thlms.gbar = 0.0005
        self.dend3(0.5).cat_thlms.gbar = 0.0005
        self.dend3(0.5).ar.gbar = 0.00025
        self.dend3(0.5).cad.beta = 0.02
        self.dend3(0.5).cad.phi = 52000.
        self.dend3(0.5).pas.g = 1 / 100
        self.dend3(0.5).pas.e = -70
        self.dend3.Ra = 175

        self.dend4(0.5).naf_tcr.gbar = 0.1
        self.dend4(0.5).napf_tcr.gbar = 0.0002
        self.dend4(0.5).kdr_thlms.gbar = 0.075
        self.dend4(0.5).kc.gbar = 0.012
        self.dend4(0.5).ka.gbar = 0.03
        self.dend4(0.5).km.gbar = 0  # // 0.0005
        self.dend4(0.5).k2.gbar = 0.002
        self.dend4(0.5).cal_thlms.gbar = 0.0005
        self.dend4(0.5).cat_thlms.gbar = 0.0005
        self.dend4(0.5).ar.gbar = 0.00025
        self.dend4(0.5).cad.beta = 0.02
        self.dend4(0.5).cad.phi = 52000.
        self.dend4(0.5).pas.g = 1 / 100
        self.dend4(0.5).pas.e = -70
        self.dend4.Ra = 175


        # ---------------axon----------------
        for mechanism_a in ['Nafin', 'kdrin', 'pas']:
            self.axon.insert(mechanism_a)
            # print(mechanism_a)

        self.axon(0.5).Nafin.gnafbar = 0.4
        self.axon(0.5).kdrin.gkdrbar = 0.001
        self.axon(0.5).pas.g = 0.005
        self.axon(0.5).pas.e = -70
        self.axon.Ra = 100
        #self.axon.cm = 1.2

        for sec in self.all:
            sec.cm = 0.9
            sec.ena = 50.
            sec.ek = -95

        # self.dend1(0.5).Nafin.gnafbar = 0.00018 * 10
        # self.dend1(0.5).kdrin.gkdrbar = 0.00018 * 0.5
        # self.dend1(0.5).kapin.gkabar = 0.000032 #* 15 * 10
        # self.dend1(0.5).pas.g = 1 / 100
        # self.dend1(0.5).pas.e = -73
        # self.dend1.Ra = 150
        # self.dend1(0.5).nap.gnapbar = 0.000018
        #
        # self.dend2(0.5).Nafin.gnafbar = 0.00018 * 10
        # self.dend2(0.5).kdrin.gkdrbar = 0.00018 * 0.5
        # self.dend2(0.5).kapin.gkabar = 0.000032 #* 15 * 10
        # self.dend2(0.5).pas.g = 1 / 100
        # self.dend2(0.5).pas.e = -73
        # self.dend2.Ra = 150
        # self.dend2(0.5).nap.gnapbar = 0.000018
        #
        # self.dend3(0.5).Nafin.gnafbar = 0.0018 * 10
        # self.dend3(0.5).kdrin.gkdrbar = 0.00018 * 0.5
        # self.dend3(0.5).kapin.gkabar = 0.000032 #* 15 * 10
        # self.dend3(0.5).pas.g = 1 / 100
        # self.dend3(0.5).pas.e = -73
        # self.dend3.Ra = 150
        # self.dend3(0.5).nap.gnapbar = 0.000018
        #
        # self.dend4(0.5).Nafin.gnafbar = 0.0018 * 10
        # self.dend4(0.5).kdrin.gkdrbar = 0.0018 * 0.5
        # self.dend4(0.5).kapin.gkabar = 0.000032 #* 15 * 10
        # self.dend4(0.5).pas.g = 1 / 100
        # self.dend4(0.5).pas.e = -73
        # self.dend4.Ra = 150
        # self.dend4(0.5).nap.gnapbar = 0.000018

        # ---------------axon----------------


        self.k_vec = h.Vector().record(self.soma(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.soma(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.soma(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.soma(0.5)._ref_ki)
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_vext[0])



        self.cyt = rxd.Region(self.all, name='cyt', nrn_region='i', dx=1.0,
                              geometry=rxd.FractionalVolume(0.9, surface_fraction=1.0))
        self.na = rxd.Species([self.cyt], name='na', charge=1, d=1.0, initial=10)
        self.k = rxd.Species([self.cyt], name='k', charge=1, d=1.0, initial=148)
        self.k_i = self.k[self.cyt]
        self.ca = rxd.Species([self.cyt], d=0.08, name='ca', charge=2, initial=1.e-4, atolscale=1e-6)



        #------for test-----------
        #self.stim = h.IClamp(self.soma(0.5))
        #self.stim.delay = 50
        #self.stim.dur = 1
        #self.stim.amp = 1
        #print(self.id)

class EpilepsyTuftIB5(Cell):
    def __init__(self, x, y, z, num):
        super().__init__(x , y, z, num)
        self.id = 5
        self.Excitatory = 1
        self.name = 'pyramidal tufted intrinsic bursting'

        # ---------------soma----------------
        for mechanism_s in ['extracellular', 'naf2_cc', 'pas', 'napf_spinstell', 'kdr_fs_cc', 'kc_fast_cc', 'ka_cc',
                        'km_cc', 'k2_cc', 'kahp_slower', 'cal_cc', 'cat_cc', 'ar', 'cad_cc']:
            self.soma.insert(mechanism_s)
        # print(mechanism_s)

        self.soma(0.5).naf2_cc.gbar = 0.65
        self.soma(0.5).napf_spinstell.gbar = 0.0002
        self.soma(0.5).kdr_fs_cc.gbar = 0.1 * 10
        self.soma(0.5).kc_fast_cc.gbar = 0.001 * 10
        self.soma(0.5).ka_cc.gbar = 0.03
        self.soma(0.5).km_cc.gbar = 0.00375
        self.soma(0.5).k2_cc.gbar = 0.0001
        self.soma(0.5).kahp_slower.gbar = 0.0001
        self.soma(0.5).cal_cc.gbar = 0.0005
        self.soma(0.5).cat_cc.gbar = 0.0001
        self.soma(0.5).ar.gbar = 0.00025
        self.soma(0.5).cad_cc.beta = 0.02
        self.soma(0.5).cad_cc.phi = 260000.
        self.soma(0.5).pas.g = 0.001
        self.soma(0.5).pas.e = -65
        self.soma.Ra = 150.

        # ---------------dend----------------
        for mechanism_d in ['naf2_cc', 'napf_spinstell', 'pas', 'kdr_fs_cc', 'kc_fast_cc', 'ka_cc', 'km_cc', 'k2_cc',
                            'kahp_slower', 'cal_cc', 'cat_cc', 'ar', 'cad_cc']:
            self.dend.insert(mechanism_d)
            self.dend1.insert(mechanism_d)
            self.dend2.insert(mechanism_d)
            self.dend3.insert(mechanism_d)
            self.dend4.insert(mechanism_d)
            # print(mechanism_d)

        self.dend(0.5).naf2_cc.gbar = 0.0075
        self.dend(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend(0.5).kc_fast_cc.gbar = 0.01
        self.dend(0.5).ka_cc.gbar = 0.03
        self.dend(0.5).km_cc.gbar = 0.00375
        self.dend(0.5).k2_cc.gbar = 0.0001
        self.dend(0.5).kahp_slower.gbar = 0.0001
        self.dend(0.5).cal_cc.gbar = 0.0005
        self.dend(0.5).cat_cc.gbar = 0.0001
        self.dend(0.5).ar.gbar = 0.00025
        self.dend(0.5).cad_cc.beta = 0.05
        self.dend(0.5).cad_cc.phi = 260000.
        self.dend(0.5).pas.g = 0.02
        self.dend(0.5).pas.e = -65
        self.dend.Ra = 250.

        self.dend1(0.5).naf2_cc.gbar = 0.0075
        self.dend1(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend1(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend1(0.5).kc_fast_cc.gbar = 0.01
        self.dend1(0.5).ka_cc.gbar = 0.03
        self.dend1(0.5).km_cc.gbar = 0.00375
        self.dend1(0.5).k2_cc.gbar = 0.0001
        self.dend1(0.5).kahp_slower.gbar = 0.0001
        self.dend1(0.5).cal_cc.gbar = 0.0005
        self.dend1(0.5).cat_cc.gbar = 0.0001
        self.dend1(0.5).ar.gbar = 0.00025
        self.dend1(0.5).cad_cc.beta = 0.05
        self.dend1(0.5).cad_cc.phi = 260000.
        self.dend1(0.5).pas.g = 0.02
        self.dend1(0.5).pas.e = -65
        self.dend1.Ra = 250.

        self.dend2(0.5).naf2_cc.gbar = 0.0075
        self.dend2(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend2(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend2(0.5).kc_fast_cc.gbar = 0.01
        self.dend2(0.5).ka_cc.gbar = 0.03
        self.dend2(0.5).km_cc.gbar = 0.00375
        self.dend2(0.5).k2_cc.gbar = 0.0001
        self.dend2(0.5).kahp_slower.gbar = 0.0001
        self.dend2(0.5).cal_cc.gbar = 0.0005
        self.dend2(0.5).cat_cc.gbar = 0.0001
        self.dend2(0.5).ar.gbar = 0.00025
        self.dend2(0.5).cad_cc.beta = 0.05
        self.dend2(0.5).cad_cc.phi = 260000.
        self.dend2(0.5).pas.g = 0.02
        self.dend2(0.5).pas.e = -65
        self.dend2.Ra = 250.

        self.dend3(0.5).naf2_cc.gbar = 0.0075
        self.dend3(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend3(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend3(0.5).kc_fast_cc.gbar = 0.01
        self.dend3(0.5).ka_cc.gbar = 0.03
        self.dend3(0.5).km_cc.gbar = 0.00375
        self.dend3(0.5).k2_cc.gbar = 0.0001
        self.dend3(0.5).kahp_slower.gbar = 0.0001
        self.dend3(0.5).cal_cc.gbar = 0.0005
        self.dend3(0.5).cat_cc.gbar = 0.0001
        self.dend3(0.5).ar.gbar = 0.00025
        self.dend3(0.5).cad_cc.beta = 0.05
        self.dend3(0.5).cad_cc.phi = 260000.
        self.dend3(0.5).pas.g = 0.02
        self.dend3(0.5).pas.e = -65
        self.dend3.Ra = 250.

        self.dend4(0.5).naf2_cc.gbar = 0.0075
        self.dend4(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend4(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend4(0.5).kc_fast_cc.gbar = 0.01
        self.dend4(0.5).ka_cc.gbar = 0.03
        self.dend4(0.5).km_cc.gbar = 0.00375
        self.dend4(0.5).k2_cc.gbar = 0.0001
        self.dend4(0.5).kahp_slower.gbar = 0.0001
        self.dend4(0.5).cal_cc.gbar = 0.0005
        self.dend4(0.5).cat_cc.gbar = 0.0001
        self.dend4(0.5).ar.gbar = 0.00025
        self.dend4(0.5).cad_cc.beta = 0.05
        self.dend4(0.5).cad_cc.phi = 260000.
        self.dend4(0.5).pas.g = 0.02
        self.dend4(0.5).pas.e = -65
        self.dend4.Ra = 250.

        # self.vd1 = h.Vector().record(self.dend(0.5)._ref_ina_naf2)
        # self.vd2 = h.Vector().record(self.dend(0.5)._ref_ina_napf_spinstell)
        # self.vd3 = h.Vector().record(self.dend(0.5)._ref_ik_kdr_fs)
        # self.vd4 = h.Vector().record(self.dend(0.5)._ref_ik_ka)
        # self.vd5 = h.Vector().record(self.dend(0.5)._ref_ik_kc_fast)
        # self.vd7 = h.Vector().record(self.dend(0.5)._ref_ik_k2)
        # self.vd8 = h.Vector().record(self.dend(0.5)._ref_ik_kahp_slower)
        # self.vd9 = h.Vector().record(self.dend(0.5)._ref_ica_cal)

        # ---------------axon----------------
        for mechanism_a in ['naf2_cc', 'kdr_fs_cc', 'ka_cc', 'k2_cc', 'pas']:
            self.axon.insert(mechanism_a)
            # print(mechanism_a)

        self.axon(0.5).naf2_cc.gbar = 0.1 * 4
        self.axon(0.5).kdr_fs_cc.gbar = 0.9
        self.axon(0.5).ka_cc.gbar = 0.002
        self.axon(0.5).k2_cc.gbar = 0.1
        self.axon(0.5).pas.g = 0.01
        self.axon(0.5).pas.e = -65
        self.axon.Ra = 100.

        for sec in self.all:
            sec.cm = 0.9
            sec.ena = 50.
            sec.ek = -90

        # self.dend1(0.5).Nafin.gnafbar = 0.00018 * 10
        # self.dend1(0.5).kdrin.gkdrbar = 0.00018 * 0.5
        # self.dend1(0.5).kapin.gkabar = 0.000032 #* 15 * 10
        # self.dend1(0.5).pas.g = 1 / 100
        # self.dend1(0.5).pas.e = -73
        # self.dend1.Ra = 150
        # self.dend1(0.5).nap.gnapbar = 0.000018
        #
        # self.dend2(0.5).Nafin.gnafbar = 0.00018 * 10
        # self.dend2(0.5).kdrin.gkdrbar = 0.00018 * 0.5
        # self.dend2(0.5).kapin.gkabar = 0.000032 #* 15 * 10
        # self.dend2(0.5).pas.g = 1 / 100
        # self.dend2(0.5).pas.e = -73
        # self.dend2.Ra = 150
        # self.dend2(0.5).nap.gnapbar = 0.000018
        #
        # self.dend3(0.5).Nafin.gnafbar = 0.0018 * 10
        # self.dend3(0.5).kdrin.gkdrbar = 0.00018 * 0.5
        # self.dend3(0.5).kapin.gkabar = 0.000032 #* 15 * 10
        # self.dend3(0.5).pas.g = 1 / 100
        # self.dend3(0.5).pas.e = -73
        # self.dend3.Ra = 150
        # self.dend3(0.5).nap.gnapbar = 0.000018
        #
        # self.dend4(0.5).Nafin.gnafbar = 0.0018 * 10
        # self.dend4(0.5).kdrin.gkdrbar = 0.0018 * 0.5
        # self.dend4(0.5).kapin.gkabar = 0.000032 #* 15 * 10
        # self.dend4(0.5).pas.g = 1 / 100
        # self.dend4(0.5).pas.e = -73
        # self.dend4.Ra = 150
        # self.dend4(0.5).nap.gnapbar = 0.000018

        # ---------------axon----------------


        self.k_vec = h.Vector().record(self.soma(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.soma(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.soma(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.soma(0.5)._ref_ki)
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_vext[0])



        self.cyt = rxd.Region(self.all, name='cyt', nrn_region='i', dx=1.0,
                              geometry=rxd.FractionalVolume(0.9, surface_fraction=1.0))
        self.na = rxd.Species([self.cyt], name='na', charge=1, d=1.0, initial=10)
        self.k = rxd.Species([self.cyt], name='k', charge=1, d=1.0, initial=148)
        self.k_i = self.k[self.cyt]
        self.ca = rxd.Species([self.cyt], d=0.08, name='ca', charge=2, initial=1.e-4, atolscale=1e-6)



        #------for test-----------
        #self.stim = h.IClamp(self.soma(0.5))
        #self.stim.delay = 50
        #self.stim.dur = 1
        #self.stim.amp = 1
        #print(self.id)

class TuftRS5(Cell):  #
    def __init__(self, x, y, z, num):
        super().__init__(x , y, z, num)
        self.id = 6
        self.Excitatory = 1
        self.name = 'pyramidal tufted regular spiking'

        # ---------------soma----------------
        for mechanism_s in ['extracellular', 'napf', 'pas', 'naf2_cc', 'kdr_fs_cc', 'kc', 'ka_cc', 'km_cc', 'k2_cc',
                            'kahp_slower', 'cal_cc', 'cat_a', 'ar', 'cad_cc']:
            self.soma.insert(mechanism_s)
            # print(mechanism_s)

        self.soma(0.5).naf2_cc.gbar = 0.6
        self.soma(0.5).napf.gbar = 0.00006
        self.soma(0.5).kdr_fs_cc.gbar = 0.5
        self.soma(0.5).ka_cc.gbar = 0.005
        self.soma(0.5).km_cc.gbar = 0.0005
        self.soma(0.5).kc.gbar = 0.01
        self.soma(0.5).k2_cc.gbar = 0.0005
        self.soma(0.5).kahp_slower.gbar = 0.0001
        self.soma(0.5).cal_cc.gbar = 0.0001
        self.soma(0.5).cat_a.gbar = 5.E-05
        self.soma(0.5).ar.gbar = 2.5E-05
        self.soma(0.5).cad_cc.beta = 0.02
        self.soma(0.5).cad_cc.phi = 10400.
        self.soma(0.5).pas.e = -70
        self.soma(0.5).pas.g = 0.001
        self.soma.Ra = 100.




        # ---------------dend----------------
        for mechanism_d in ['naf_tcr', 'napf_tcr', 'kdr_thlms','ka', 'kc', 'km', 'k2', 'kahp_slower', 'cal_thlms', 'cat_thlms', 'ar', 'cad',  'pas']:
            self.dend.insert(mechanism_d)
            self.dend1.insert(mechanism_d)
            self.dend2.insert(mechanism_d)
            self.dend3.insert(mechanism_d)
            self.dend4.insert(mechanism_d)

            # print(mechanism_d)

        # self.dend(0.5).naf2.gbar =   0.2
        self.dend(0.5).naf_tcr.gbar =   0.1
        self.dend(0.5).napf_tcr.gbar =   0.0002
        self.dend(0.5).kdr_thlms.gbar =   0.075
        self.dend(0.5).kc.gbar =   0.012
        self.dend(0.5).ka.gbar =   0.03
        self.dend(0.5).km.gbar =   0 #// 0.0005
        self.dend(0.5).k2.gbar =   0.002
        self.dend(0.5).cal_thlms.gbar =   0.0005
        self.dend(0.5).cat_thlms.gbar =   0.0005
        self.dend(0.5).ar.gbar =   0.00025
        self.dend(0.5).cad.beta  =   0.02
        self.dend(0.5).cad.phi =   52000.
        self.dend(0.5).pas.g = 1 / 100
        self.dend(0.5).pas.e = -70
        self.dend.Ra = 175

        self.dend1(0.5).naf_tcr.gbar = 0.1
        self.dend1(0.5).napf_tcr.gbar = 0.0002
        self.dend1(0.5).kdr_thlms.gbar = 0.075
        self.dend1(0.5).kc.gbar = 0.012
        self.dend1(0.5).ka.gbar = 0.03
        self.dend1(0.5).km.gbar = 0  # // 0.0005
        self.dend1(0.5).k2.gbar = 0.002
        self.dend1(0.5).cal_thlms.gbar = 0.0005
        self.dend1(0.5).cat_thlms.gbar = 0.0005
        self.dend1(0.5).ar.gbar = 0.00025
        self.dend1(0.5).cad.beta = 0.02
        self.dend1(0.5).cad.phi = 52000.
        self.dend1(0.5).pas.g = 1 / 100
        self.dend1(0.5).pas.e = -70
        self.dend1.Ra = 175

        self.dend2(0.5).naf_tcr.gbar = 0.1
        self.dend2(0.5).napf_tcr.gbar = 0.0002
        self.dend2(0.5).kdr_thlms.gbar = 0.075
        self.dend2(0.5).kc.gbar = 0.012
        self.dend2(0.5).ka.gbar = 0.03
        self.dend2(0.5).km.gbar = 0  # // 0.0005
        self.dend2(0.5).k2.gbar = 0.002
        self.dend2(0.5).cal_thlms.gbar = 0.0005
        self.dend2(0.5).cat_thlms.gbar = 0.0005
        self.dend2(0.5).ar.gbar = 0.00025
        self.dend2(0.5).cad.beta = 0.02
        self.dend2(0.5).cad.phi = 52000.
        self.dend2(0.5).pas.g = 1 / 100
        self.dend2(0.5).pas.e = -70
        self.dend2.Ra = 175

        self.dend3(0.5).naf_tcr.gbar = 0.1
        self.dend3(0.5).napf_tcr.gbar = 0.0002
        self.dend3(0.5).kdr_thlms.gbar = 0.075
        self.dend3(0.5).kc.gbar = 0.012
        self.dend3(0.5).ka.gbar = 0.03
        self.dend3(0.5).km.gbar = 0  # // 0.0005
        self.dend3(0.5).k2.gbar = 0.002
        self.dend3(0.5).cal_thlms.gbar = 0.0005
        self.dend3(0.5).cat_thlms.gbar = 0.0005
        self.dend3(0.5).ar.gbar = 0.00025
        self.dend3(0.5).cad.beta = 0.02
        self.dend3(0.5).cad.phi = 52000.
        self.dend3(0.5).pas.g = 1 / 100
        self.dend3(0.5).pas.e = -70
        self.dend3.Ra = 175

        self.dend4(0.5).naf_tcr.gbar = 0.1
        self.dend4(0.5).napf_tcr.gbar = 0.0002
        self.dend4(0.5).kdr_thlms.gbar = 0.075
        self.dend4(0.5).kc.gbar = 0.012
        self.dend4(0.5).ka.gbar = 0.03
        self.dend4(0.5).km.gbar = 0  # // 0.0005
        self.dend4(0.5).k2.gbar = 0.002
        self.dend4(0.5).cal_thlms.gbar = 0.0005
        self.dend4(0.5).cat_thlms.gbar = 0.0005
        self.dend4(0.5).ar.gbar = 0.00025
        self.dend4(0.5).cad.beta = 0.02
        self.dend4(0.5).cad.phi = 52000.
        self.dend4(0.5).pas.g = 1 / 100
        self.dend4(0.5).pas.e = -70
        self.dend4.Ra = 175


        # ---------------axon----------------
        for mechanism_a in ['Nafin', 'kdrin', 'pas']:
            self.axon.insert(mechanism_a)
            # print(mechanism_a)

        self.axon(0.5).Nafin.gnafbar = 0.4
        self.axon(0.5).kdrin.gkdrbar = 0.001
        self.axon(0.5).pas.g = 0.005
        self.axon(0.5).pas.e = -70
        self.axon.Ra = 100
        #self.axon.cm = 1.2

        for sec in self.all:
            sec.cm = 0.9
            sec.ena = 50.
            sec.ek = -95

        self.k_vec = h.Vector().record(self.soma(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.soma(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.soma(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.soma(0.5)._ref_ki)
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_vext[0])
        self.cyt = rxd.Region(self.all, name='cyt', nrn_region='i', dx=1.0,
                              geometry=rxd.FractionalVolume(0.9, surface_fraction=1.0))
        self.na = rxd.Species([self.cyt], name='na', charge=1, d=1.0, initial=10)
        self.k = rxd.Species([self.cyt], name='k', charge=1, d=1.0, initial=148)
        self.k_i = self.k[self.cyt]
        self.ca = rxd.Species([self.cyt], d=0.08, name='ca', charge=2, initial=1.e-4, atolscale=1e-6)

        #------for test-----------
        #self.stim = h.IClamp(self.soma(0.5))
        #self.stim.delay = 50
        #self.stim.dur = 1
        #self.stim.amp = 1
        #print(self.id)
    
class EpilepsyTuftRS5(Cell):  #
    def __init__(self, x, y, z, num):
        super().__init__(x , y, z, num)
        self.id = 6
        self.Excitatory = 1
        self.name = 'pyramidal tufted regular spiking'

        # ---------------soma----------------
        for mechanism_s in ['extracellular', 'naf2_cc', 'pas', 'napf_spinstell', 'kdr_fs_cc', 'kc_fast_cc', 'ka_cc',
                        'km_cc', 'k2_cc', 'kahp_slower', 'cal_cc', 'cat_cc', 'ar', 'cad_cc']:
            self.soma.insert(mechanism_s)
        # print(mechanism_s)

        self.soma(0.5).naf2_cc.gbar = 0.65
        self.soma(0.5).napf_spinstell.gbar = 0.0002
        self.soma(0.5).kdr_fs_cc.gbar = 0.1 * 10
        self.soma(0.5).kc_fast_cc.gbar = 0.001 * 10
        self.soma(0.5).ka_cc.gbar = 0.03
        self.soma(0.5).km_cc.gbar = 0.00375
        self.soma(0.5).k2_cc.gbar = 0.0001
        self.soma(0.5).kahp_slower.gbar = 0.0001
        self.soma(0.5).cal_cc.gbar = 0.0005
        self.soma(0.5).cat_cc.gbar = 0.0001
        self.soma(0.5).ar.gbar = 0.00025
        self.soma(0.5).cad_cc.beta = 0.02
        self.soma(0.5).cad_cc.phi = 260000.
        self.soma(0.5).pas.g = 0.001
        self.soma(0.5).pas.e = -65
        self.soma.Ra = 150.

        # ---------------dend----------------
        for mechanism_d in ['naf2_cc', 'napf_spinstell', 'pas', 'kdr_fs_cc', 'kc_fast_cc', 'ka_cc', 'km_cc', 'k2_cc',
                            'kahp_slower', 'cal_cc', 'cat_cc', 'ar', 'cad_cc']:
            self.dend.insert(mechanism_d)
            self.dend1.insert(mechanism_d)
            self.dend2.insert(mechanism_d)
            self.dend3.insert(mechanism_d)
            self.dend4.insert(mechanism_d)
            # print(mechanism_d)

        self.dend(0.5).naf2_cc.gbar = 0.0075
        self.dend(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend(0.5).kc_fast_cc.gbar = 0.01
        self.dend(0.5).ka_cc.gbar = 0.03
        self.dend(0.5).km_cc.gbar = 0.00375
        self.dend(0.5).k2_cc.gbar = 0.0001
        self.dend(0.5).kahp_slower.gbar = 0.0001
        self.dend(0.5).cal_cc.gbar = 0.0005
        self.dend(0.5).cat_cc.gbar = 0.0001
        self.dend(0.5).ar.gbar = 0.00025
        self.dend(0.5).cad_cc.beta = 0.05
        self.dend(0.5).cad_cc.phi = 260000.
        self.dend(0.5).pas.g = 0.02
        self.dend(0.5).pas.e = -65
        self.dend.Ra = 250.

        self.dend1(0.5).naf2_cc.gbar = 0.0075
        self.dend1(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend1(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend1(0.5).kc_fast_cc.gbar = 0.01
        self.dend1(0.5).ka_cc.gbar = 0.03
        self.dend1(0.5).km_cc.gbar = 0.00375
        self.dend1(0.5).k2_cc.gbar = 0.0001
        self.dend1(0.5).kahp_slower.gbar = 0.0001
        self.dend1(0.5).cal_cc.gbar = 0.0005
        self.dend1(0.5).cat_cc.gbar = 0.0001
        self.dend1(0.5).ar.gbar = 0.00025
        self.dend1(0.5).cad_cc.beta = 0.05
        self.dend1(0.5).cad_cc.phi = 260000.
        self.dend1(0.5).pas.g = 0.02
        self.dend1(0.5).pas.e = -65
        self.dend1.Ra = 250.

        self.dend2(0.5).naf2_cc.gbar = 0.0075
        self.dend2(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend2(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend2(0.5).kc_fast_cc.gbar = 0.01
        self.dend2(0.5).ka_cc.gbar = 0.03
        self.dend2(0.5).km_cc.gbar = 0.00375
        self.dend2(0.5).k2_cc.gbar = 0.0001
        self.dend2(0.5).kahp_slower.gbar = 0.0001
        self.dend2(0.5).cal_cc.gbar = 0.0005
        self.dend2(0.5).cat_cc.gbar = 0.0001
        self.dend2(0.5).ar.gbar = 0.00025
        self.dend2(0.5).cad_cc.beta = 0.05
        self.dend2(0.5).cad_cc.phi = 260000.
        self.dend2(0.5).pas.g = 0.02
        self.dend2(0.5).pas.e = -65
        self.dend2.Ra = 250.

        self.dend3(0.5).naf2_cc.gbar = 0.0075
        self.dend3(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend3(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend3(0.5).kc_fast_cc.gbar = 0.01
        self.dend3(0.5).ka_cc.gbar = 0.03
        self.dend3(0.5).km_cc.gbar = 0.00375
        self.dend3(0.5).k2_cc.gbar = 0.0001
        self.dend3(0.5).kahp_slower.gbar = 0.0001
        self.dend3(0.5).cal_cc.gbar = 0.0005
        self.dend3(0.5).cat_cc.gbar = 0.0001
        self.dend3(0.5).ar.gbar = 0.00025
        self.dend3(0.5).cad_cc.beta = 0.05
        self.dend3(0.5).cad_cc.phi = 260000.
        self.dend3(0.5).pas.g = 0.02
        self.dend3(0.5).pas.e = -65
        self.dend3.Ra = 250.

        self.dend4(0.5).naf2_cc.gbar = 0.0075
        self.dend4(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend4(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend4(0.5).kc_fast_cc.gbar = 0.01
        self.dend4(0.5).ka_cc.gbar = 0.03
        self.dend4(0.5).km_cc.gbar = 0.00375
        self.dend4(0.5).k2_cc.gbar = 0.0001
        self.dend4(0.5).kahp_slower.gbar = 0.0001
        self.dend4(0.5).cal_cc.gbar = 0.0005
        self.dend4(0.5).cat_cc.gbar = 0.0001
        self.dend4(0.5).ar.gbar = 0.00025
        self.dend4(0.5).cad_cc.beta = 0.05
        self.dend4(0.5).cad_cc.phi = 260000.
        self.dend4(0.5).pas.g = 0.02
        self.dend4(0.5).pas.e = -65
        self.dend4.Ra = 250.

        # self.vd1 = h.Vector().record(self.dend(0.5)._ref_ina_naf2)
        # self.vd2 = h.Vector().record(self.dend(0.5)._ref_ina_napf_spinstell)
        # self.vd3 = h.Vector().record(self.dend(0.5)._ref_ik_kdr_fs)
        # self.vd4 = h.Vector().record(self.dend(0.5)._ref_ik_ka)
        # self.vd5 = h.Vector().record(self.dend(0.5)._ref_ik_kc_fast)
        # self.vd7 = h.Vector().record(self.dend(0.5)._ref_ik_k2)
        # self.vd8 = h.Vector().record(self.dend(0.5)._ref_ik_kahp_slower)
        # self.vd9 = h.Vector().record(self.dend(0.5)._ref_ica_cal)

        # ---------------axon----------------
        for mechanism_a in ['naf2_cc', 'kdr_fs_cc', 'ka_cc', 'k2_cc', 'pas']:
            self.axon.insert(mechanism_a)
            # print(mechanism_a)

        self.axon(0.5).naf2_cc.gbar = 0.1 * 4
        self.axon(0.5).kdr_fs_cc.gbar = 0.9
        self.axon(0.5).ka_cc.gbar = 0.002
        self.axon(0.5).k2_cc.gbar = 0.1
        self.axon(0.5).pas.g = 0.01
        self.axon(0.5).pas.e = -65
        self.axon.Ra = 100.

        for sec in self.all:
            sec.cm = 0.9
            sec.ena = 50.
            sec.ek = -90



        self.k_vec = h.Vector().record(self.soma(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.soma(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.soma(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.soma(0.5)._ref_ki)
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_vext[0])
        self.cyt = rxd.Region(self.all, name='cyt', nrn_region='i', dx=1.0,
                              geometry=rxd.FractionalVolume(0.9, surface_fraction=1.0))
        self.na = rxd.Species([self.cyt], name='na', charge=1, d=1.0, initial=10)
        self.k = rxd.Species([self.cyt], name='k', charge=1, d=1.0, initial=148)
        self.k_i = self.k[self.cyt]
        self.ca = rxd.Species([self.cyt], d=0.08, name='ca', charge=2, initial=1.e-4, atolscale=1e-6)

        #------for test-----------
        #self.stim = h.IClamp(self.soma(0.5))
        #self.stim.delay = 50
        #self.stim.dur = 1
        #self.stim.amp = 1
        #print(self.id)

class Bask56(Cell):  #
    def __init__(self, x, y, z, num):
        super().__init__(x , y, z, num)
        self.id = 7
        self.Excitatory = -1
        self.name = 'deep interneurons basket'
        # ---------------soma----------------
        for mechanism_s in ['extracellular', 'Nafin', 'kdrin', 'IKsin', 'hin', 'kapin', 'canin', 'kctin', 'cadynin','nap',
                            'pas']:
            self.soma.insert(mechanism_s)

        self.soma(0.5).Nafin.gnafbar = 0.45
        self.soma(0.5).kdrin.gkdrbar = 0.001
        self.soma(0.5).IKsin.gKsbar = 0.000725 * 0.1
        self.soma(0.5).hin.gbar = 0.00001
        self.soma(0.5).kapin.gkabar = 0.0032 * 15
        self.soma(0.5).canin.gcalbar = 0.0003
        self.soma(0.5).kctin.gkcbar = 0.0001
        self.soma(0.5).pas.g = 0.002
        self.soma(0.5).pas.e = -70
        self.soma.Ra = 100
        self.soma(0.5).nap.gnapbar = 0.000018

        self.v1 = h.Vector().record(self.soma(0.5)._ref_ina_Nafin)
        # self.v2 = h.Vector().record(self.soma(0.5)._ref_ina_nap)
        self.v3 = h.Vector().record(self.soma(0.5)._ref_ik_kdrin)
        self.v4 = h.Vector().record(self.soma(0.5)._ref_ik_IKsin)
        # self.v5 = h.Vector().record(self.soma(0.5)._ref_ik_kc_fast)
        # self.v6 = h.Vector().record(self.soma(0.5)._ref_ik_km)
        # self.v7 = h.Vector().record(self.soma(0.5)._ref_ik_k2)
        # self.v8 = h.Vector().record(self.soma(0.5)._ref_ik_kahp_slower)
        # self.v9 = h.Vector().record(self.soma(0.5)._ref_ica_cal)

        # ---------------dend----------------
        for mechanism_d in ['Nafin', 'kdrin', 'kapin', 'pas', 'nap']:
            self.dend.insert(mechanism_d)
            self.dend1.insert(mechanism_d)
            self.dend2.insert(mechanism_d)
            self.dend3.insert(mechanism_d)
            self.dend4.insert(mechanism_d)

            # print(mechanism_d)

        # self.dend(0.5).naf2.gbar =   0.2
        self.dend(0.5).Nafin.gnafbar = 0.018 * 10
        self.dend(0.5).kdrin.gkdrbar = 0.018
        self.dend(0.5).kapin.gkabar = 0.000032 #* 15 * 10
        self.dend(0.5).nap.gnapbar = 0.000018
        self.dend(0.5).pas.g = 1 / 100
        self.dend(0.5).pas.e = -73
        self.dend.Ra = 150

        self.dend1(0.5).Nafin.gnafbar = 0.018 * 10
        self.dend1(0.5).kdrin.gkdrbar = 0.018 * 0.5
        self.dend1(0.5).kapin.gkabar = 0.000032 #* 15 * 10
        self.dend1(0.5).pas.g = 1 / 100
        self.dend1(0.5).pas.e = -73
        self.dend1.Ra = 150
        self.dend1(0.5).nap.gnapbar = 0.000018

        self.dend2(0.5).Nafin.gnafbar = 0.018 * 10
        self.dend2(0.5).kdrin.gkdrbar = 0.018 * 0.5
        self.dend2(0.5).kapin.gkabar = 0.000032 #* 15 * 10
        self.dend2(0.5).pas.g = 1 / 100
        self.dend2(0.5).pas.e = -73
        self.dend2.Ra = 150
        self.dend2(0.5).nap.gnapbar = 0.000018

        self.dend3(0.5).Nafin.gnafbar = 0.018 * 10
        self.dend3(0.5).kdrin.gkdrbar = 0.018 * 0.5
        self.dend3(0.5).kapin.gkabar = 0.000032 #* 15 * 10
        self.dend3(0.5).pas.g = 1 / 100
        self.dend3(0.5).pas.e = -73
        self.dend3.Ra = 150
        self.dend3(0.5).nap.gnapbar = 0.000018

        self.dend4(0.5).Nafin.gnafbar = 0.018 * 10
        self.dend4(0.5).kdrin.gkdrbar = 0.018 * 0.5
        self.dend4(0.5).kapin.gkabar = 0.000032 #* 15 * 10
        self.dend4(0.5).pas.g = 1 / 100
        self.dend4(0.5).pas.e = -73
        self.dend4.Ra = 150
        self.dend4(0.5).nap.gnapbar = 0.000018

        self.vd1 = h.Vector().record(self.dend(0.5)._ref_ina_Nafin)
        # self.vd2 = h.Vector().record(self.dend(0.5)._ref_ina_napf_spinstell)
        self.vd3 = h.Vector().record(self.dend(0.5)._ref_ik_kdrin)
        self.vd4 = h.Vector().record(self.dend(0.5)._ref_ik_kapin)

        # ---------------axon----------------
        for mechanism_a in ['Nafin', 'kdrin', 'pas']:
            self.axon.insert(mechanism_a)
            # print(mechanism_a)

        self.axon(0.5).Nafin.gnafbar = 0.4
        self.axon(0.5).kdrin.gkdrbar = 0.001
        self.axon(0.5).pas.g = 0.0002
        self.axon(0.5).pas.e = -73
        self.axon.Ra = 100
        self.axon.cm = 1.2

        for sec in self.all:        
            sec.cm = 1
            sec.ena = 50.
            sec.ek =  -100.

        self.k_vec = h.Vector().record(self.soma(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.soma(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.soma(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.soma(0.5)._ref_ki)
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_vext[0])
        self.cyt = rxd.Region(self.all, name='cyt', nrn_region='i', dx=1.0,
                              geometry=rxd.FractionalVolume(0.9, surface_fraction=1.0))
        self.na = rxd.Species([self.cyt], name='na', charge=1, d=1.0, initial=10)
        self.k = rxd.Species([self.cyt], name='k', charge=1, d=1.0, initial=148)
        self.k_i = self.k[self.cyt]
        self.ca = rxd.Species([self.cyt], d=0.08, name='ca', charge=2, initial=1.e-4, atolscale=1e-6)
        #------for test-----------
        #self.stim = h.IClamp(self.soma(0.5))
        #self.stim.delay = 50
        #self.stim.dur = 1
        #self.stim.amp = 1
        #print(self.id)
    


class Axax56(Cell):  #
    def __init__(self, x, y, z, num):
        super().__init__(x , y, z, num)
        self.id = 8
        self.Excitatory = -1
        self.name = 'deep interneurons axoaxonic'

        # ---------------soma----------------
        for mechanism_s in ['extracellular', 'naf2_cc', 'pas', 'napf_spinstell', 'kdr_fs_cc', 'kc_fast_cc', 'ka_cc',
                            'km_cc', 'k2_cc', 'kahp_slower', 'cal_cc', 'cat_cc', 'ar', 'cad_cc']:
            self.soma.insert(mechanism_s)
            # print(mechanism_s)

        self.soma(0.5).naf2_cc.gbar = 0.65
        self.soma(0.5).napf_spinstell.gbar = 0.0002
        self.soma(0.5).kdr_fs_cc.gbar = 0.1 * 10
        self.soma(0.5).kc_fast_cc.gbar = 0.001 * 10
        self.soma(0.5).ka_cc.gbar = 0.03
        self.soma(0.5).km_cc.gbar = 0.00375
        self.soma(0.5).k2_cc.gbar = 0.0001
        self.soma(0.5).kahp_slower.gbar = 0.0001
        self.soma(0.5).cal_cc.gbar = 0.0005
        self.soma(0.5).cat_cc.gbar = 0.0001
        self.soma(0.5).ar.gbar = 0.00025
        self.soma(0.5).cad_cc.beta = 0.02
        self.soma(0.5).cad_cc.phi = 260000.
        self.soma(0.5).pas.g = 0.001
        self.soma(0.5).pas.e = -65
        self.soma.Ra = 150.

        # ---------------dend----------------
        for mechanism_d in ['naf2_cc', 'napf_spinstell', 'pas', 'kdr_fs_cc', 'kc_fast_cc', 'ka_cc', 'km_cc', 'k2_cc',
                            'kahp_slower', 'cal_cc', 'cat_cc', 'ar', 'cad_cc']:
            self.dend.insert(mechanism_d)
            self.dend1.insert(mechanism_d)
            self.dend2.insert(mechanism_d)
            self.dend3.insert(mechanism_d)
            self.dend4.insert(mechanism_d)
            # print(mechanism_d)

        self.dend(0.5).naf2_cc.gbar = 0.0075
        self.dend(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend(0.5).kc_fast_cc.gbar = 0.01
        self.dend(0.5).ka_cc.gbar = 0.03
        self.dend(0.5).km_cc.gbar = 0.00375
        self.dend(0.5).k2_cc.gbar = 0.0001
        self.dend(0.5).kahp_slower.gbar = 0.0001
        self.dend(0.5).cal_cc.gbar = 0.0005
        self.dend(0.5).cat_cc.gbar = 0.0001
        self.dend(0.5).ar.gbar = 0.00025
        self.dend(0.5).cad_cc.beta = 0.05
        self.dend(0.5).cad_cc.phi = 260000.
        self.dend(0.5).pas.g = 0.02
        self.dend(0.5).pas.e = -65
        self.dend.Ra = 250.

        self.dend1(0.5).naf2_cc.gbar = 0.0075
        self.dend1(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend1(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend1(0.5).kc_fast_cc.gbar = 0.01
        self.dend1(0.5).ka_cc.gbar = 0.03
        self.dend1(0.5).km_cc.gbar = 0.00375
        self.dend1(0.5).k2_cc.gbar = 0.0001
        self.dend1(0.5).kahp_slower.gbar = 0.0001
        self.dend1(0.5).cal_cc.gbar = 0.0005
        self.dend1(0.5).cat_cc.gbar = 0.0001
        self.dend1(0.5).ar.gbar = 0.00025
        self.dend1(0.5).cad_cc.beta = 0.05
        self.dend1(0.5).cad_cc.phi = 260000.
        self.dend1(0.5).pas.g = 0.02
        self.dend1(0.5).pas.e = -65
        self.dend1.Ra = 250.

        self.dend2(0.5).naf2_cc.gbar = 0.0075
        self.dend2(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend2(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend2(0.5).kc_fast_cc.gbar = 0.01
        self.dend2(0.5).ka_cc.gbar = 0.03
        self.dend2(0.5).km_cc.gbar = 0.00375
        self.dend2(0.5).k2_cc.gbar = 0.0001
        self.dend2(0.5).kahp_slower.gbar = 0.0001
        self.dend2(0.5).cal_cc.gbar = 0.0005
        self.dend2(0.5).cat_cc.gbar = 0.0001
        self.dend2(0.5).ar.gbar = 0.00025
        self.dend2(0.5).cad_cc.beta = 0.05
        self.dend2(0.5).cad_cc.phi = 260000.
        self.dend2(0.5).pas.g = 0.02
        self.dend2(0.5).pas.e = -65
        self.dend2.Ra = 250.

        self.dend3(0.5).naf2_cc.gbar = 0.0075
        self.dend3(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend3(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend3(0.5).kc_fast_cc.gbar = 0.01
        self.dend3(0.5).ka_cc.gbar = 0.03
        self.dend3(0.5).km_cc.gbar = 0.00375
        self.dend3(0.5).k2_cc.gbar = 0.0001
        self.dend3(0.5).kahp_slower.gbar = 0.0001
        self.dend3(0.5).cal_cc.gbar = 0.0005
        self.dend3(0.5).cat_cc.gbar = 0.0001
        self.dend3(0.5).ar.gbar = 0.00025
        self.dend3(0.5).cad_cc.beta = 0.05
        self.dend3(0.5).cad_cc.phi = 260000.
        self.dend3(0.5).pas.g = 0.02
        self.dend3(0.5).pas.e = -65
        self.dend3.Ra = 250.

        self.dend4(0.5).naf2_cc.gbar = 0.0075
        self.dend4(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend4(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend4(0.5).kc_fast_cc.gbar = 0.01
        self.dend4(0.5).ka_cc.gbar = 0.03
        self.dend4(0.5).km_cc.gbar = 0.00375
        self.dend4(0.5).k2_cc.gbar = 0.0001
        self.dend4(0.5).kahp_slower.gbar = 0.0001
        self.dend4(0.5).cal_cc.gbar = 0.0005
        self.dend4(0.5).cat_cc.gbar = 0.0001
        self.dend4(0.5).ar.gbar = 0.00025
        self.dend4(0.5).cad_cc.beta = 0.05
        self.dend4(0.5).cad_cc.phi = 260000.
        self.dend4(0.5).pas.g = 0.02
        self.dend4(0.5).pas.e = -65
        self.dend4.Ra = 250.

        # self.vd1 = h.Vector().record(self.dend(0.5)._ref_ina_naf2)
        # self.vd2 = h.Vector().record(self.dend(0.5)._ref_ina_napf_spinstell)
        # self.vd3 = h.Vector().record(self.dend(0.5)._ref_ik_kdr_fs)
        # self.vd4 = h.Vector().record(self.dend(0.5)._ref_ik_ka)
        # self.vd5 = h.Vector().record(self.dend(0.5)._ref_ik_kc_fast)
        # self.vd7 = h.Vector().record(self.dend(0.5)._ref_ik_k2)
        # self.vd8 = h.Vector().record(self.dend(0.5)._ref_ik_kahp_slower)
        # self.vd9 = h.Vector().record(self.dend(0.5)._ref_ica_cal)

        # ---------------axon----------------
        for mechanism_a in ['naf2_cc', 'kdr_fs_cc', 'ka_cc', 'k2_cc', 'pas']:
            self.axon.insert(mechanism_a)
            # print(mechanism_a)

        self.axon(0.5).naf2_cc.gbar = 0.1 * 4
        self.axon(0.5).kdr_fs_cc.gbar = 0.9
        self.axon(0.5).ka_cc.gbar = 0.002
        self.axon(0.5).k2_cc.gbar = 0.1
        self.axon(0.5).pas.g = 0.01
        self.axon(0.5).pas.e = -65
        self.axon.Ra = 100.

        for sec in self.all:
            sec.cm = 0.9
            sec.ena = 50.
            sec.ek = -90

        self.k_vec = h.Vector().record(self.soma(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.soma(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.soma(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.soma(0.5)._ref_ki)
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_vext[0])
        self.cyt = rxd.Region(self.all, name='cyt', nrn_region='i', dx=1.0,
                              geometry=rxd.FractionalVolume(0.9, surface_fraction=1.0))
        self.na = rxd.Species([self.cyt], name='na', charge=1, d=1.0, initial=10)
        self.k = rxd.Species([self.cyt], name='k', charge=1, d=1.0, initial=148)
        self.k_i = self.k[self.cyt]
        self.ca = rxd.Species([self.cyt], d=0.08, name='ca', charge=2, initial=1.e-4, atolscale=1e-6)

        #------for test-----------
        #self.stim = h.IClamp(self.soma(0.5))
        #self.stim.delay = 50
        #self.stim.dur = 1
        #self.stim.amp = 1
        #print(self.id)



class LTS56(Cell):  #
    def __init__(self, x, y, z, num):
        super().__init__(x , y, z, num)
        self.id = 9
        self.Excitatory = -1
        self.name ='deep interneurons low threshold spiking'

        # ---------------soma----------------
        for mechanism_s in ['extracellular', 'Nafin', 'kdrin', 'IKsin', 'hin', 'kapin', 'canin', 'kctin', 'cadynin',
                            'pas']:
            self.soma.insert(mechanism_s)

        self.soma(0.5).Nafin.gnafbar = 0.25
        self.soma(0.5).kdrin.gkdrbar = 0.001
        self.soma(0.5).IKsin.gKsbar = 0.000725 * 0.1
        self.soma(0.5).hin.gbar = 0.00001
        self.soma(0.5).kapin.gkabar = 0.0032 * 15
        self.soma(0.5).canin.gcalbar = 0.0003
        self.soma(0.5).kctin.gkcbar = 0.0001
        self.soma(0.5).pas.g = 0.0002
        self.soma(0.5).pas.e = -70
        self.soma.Ra = 200
        #self.soma(0.5).nap.gnapbar = 0.000018

        self.v1 = h.Vector().record(self.soma(0.5)._ref_ina_Nafin)
        # self.v2 = h.Vector().record(self.soma(0.5)._ref_ina_nap)
        self.v3 = h.Vector().record(self.soma(0.5)._ref_ik_kdrin)
        self.v4 = h.Vector().record(self.soma(0.5)._ref_ik_IKsin)
        # self.v5 = h.Vector().record(self.soma(0.5)._ref_ik_kc_fast)
        # self.v6 = h.Vector().record(self.soma(0.5)._ref_ik_km)
        # self.v7 = h.Vector().record(self.soma(0.5)._ref_ik_k2)
        # self.v8 = h.Vector().record(self.soma(0.5)._ref_ik_kahp_slower)
        # self.v9 = h.Vector().record(self.soma(0.5)._ref_ica_cal)

        # ---------------dend----------------
        for mechanism_d in ['Nafin', 'kdrin', 'kapin', 'pas', 'nap']:
            self.dend.insert(mechanism_d)
            self.dend1.insert(mechanism_d)
            self.dend2.insert(mechanism_d)
            self.dend3.insert(mechanism_d)
            self.dend4.insert(mechanism_d)

            # print(mechanism_d)

        # self.dend(0.5).naf2.gbar =   0.2
        self.dend(0.5).Nafin.gnafbar = 0.018 * 10
        self.dend(0.5).kdrin.gkdrbar = 0.018
        self.dend(0.5).kapin.gkabar = 0.000032 #* 15 * 10
        self.dend(0.5).nap.gnapbar = 0.000018
        self.dend(0.5).pas.g = 1 / 100
        self.dend(0.5).pas.e = -73
        self.dend.Ra = 150

        self.dend1(0.5).Nafin.gnafbar = 0.018 * 5
        self.dend1(0.5).kdrin.gkdrbar = 0.018 * 0.5
        self.dend1(0.5).kapin.gkabar = 0.000032 #* 15 * 10
        self.dend1(0.5).pas.g = 1 / 100
        self.dend1(0.5).pas.e = -73
        self.dend1.Ra = 150
        self.dend1(0.5).nap.gnapbar = 0.000018

        self.dend2(0.5).Nafin.gnafbar = 0.018 * 5
        self.dend2(0.5).kdrin.gkdrbar = 0.018 * 0.5
        self.dend2(0.5).kapin.gkabar = 0.000032 #* 15 * 10
        self.dend2(0.5).pas.g = 1 / 100
        self.dend2(0.5).pas.e = -73
        self.dend2.Ra = 150
        self.dend2(0.5).nap.gnapbar = 0.000018

        self.dend3(0.5).Nafin.gnafbar = 0.018 * 5
        self.dend3(0.5).kdrin.gkdrbar = 0.018 * 0.5
        self.dend3(0.5).kapin.gkabar = 0.000032 #* 15 * 10
        self.dend3(0.5).pas.g = 1 / 100
        self.dend3(0.5).pas.e = -73
        self.dend3.Ra = 150
        self.dend3(0.5).nap.gnapbar = 0.000018

        self.dend4(0.5).Nafin.gnafbar = 0.018 * 5
        self.dend4(0.5).kdrin.gkdrbar = 0.018 * 0.5
        self.dend4(0.5).kapin.gkabar = 0.000032 #* 15 * 10
        self.dend4(0.5).pas.g = 1 / 100
        self.dend4(0.5).pas.e = -73
        self.dend4.Ra = 150
        self.dend4(0.5).nap.gnapbar = 0.000018

        self.vd1 = h.Vector().record(self.dend(0.5)._ref_ina_Nafin)
        # self.vd2 = h.Vector().record(self.dend(0.5)._ref_ina_napf_spinstell)
        self.vd3 = h.Vector().record(self.dend(0.5)._ref_ik_kdrin)
        self.vd4 = h.Vector().record(self.dend(0.5)._ref_ik_kapin)

        # ---------------axon----------------
        for mechanism_a in ['Nafin', 'kdrin', 'pas']:
            self.axon.insert(mechanism_a)
            # print(mechanism_a)

        self.axon(0.5).Nafin.gnafbar = 0.4
        self.axon(0.5).kdrin.gkdrbar = 0.001
        self.axon(0.5).pas.g = 0.0002
        self.axon(0.5).pas.e = -73
        self.axon.Ra = 100
        self.axon.cm = 1.2

        for sec in self.all:        
            sec.cm = 1
            sec.ena = 50.
            sec.ek =  -100.

        self.k_vec = h.Vector().record(self.soma(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.soma(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.soma(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.soma(0.5)._ref_ki)
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_vext[0])
        self.cyt = rxd.Region(self.all, name='cyt', nrn_region='i', dx=1.0,
                              geometry=rxd.FractionalVolume(0.9, surface_fraction=1.0))
        self.na = rxd.Species([self.cyt], name='na', charge=1, d=1.0, initial=10)
        self.k = rxd.Species([self.cyt], name='k', charge=1, d=1.0, initial=148)
        self.k_i = self.k[self.cyt]
        self.ca = rxd.Species([self.cyt], d=0.08, name='ca', charge=2, initial=1.e-4, atolscale=1e-6)
        #------for test-----------
        #self.stim = h.IClamp(self.soma(0.5))
        #self.stim.delay = 50
        #self.stim.dur = 1
        #self.stim.amp = 1
   

class NontuftRS6(Cell):  #
    def __init__(self, x, y, z, num):
        super().__init__(x , y, z, num)
        self.id = 10
        self.Excitatory = 1
        self.name ='pyramidal nontufted regular spiking'

        # ---------------soma----------------
        #for mechanism_s in ['extracellular', 'Nafin', 'kdrin', 'IKsin', 'hin', 'kapin', 'canin', 'kctin', 'cadynin',
        #                    'pas']:
        #    self.soma.insert(mechanism_s)
#
        #self.soma(0.5).Nafin.gnafbar = 0.5
        #self.soma(0.5).kdrin.gkdrbar = 0.001
        #self.soma(0.5).IKsin.gKsbar = 0.000725 * 0.1
        #self.soma(0.5).hin.gbar = 0.00001
        #self.soma(0.5).kapin.gkabar = 0.0032 * 15
        #self.soma(0.5).canin.gcalbar = 0.0003
        #self.soma(0.5).kctin.gkcbar = 0.0001
        #self.soma(0.5).pas.g = 0.0002
        #self.soma(0.5).pas.e = -70
        #self.soma.Ra = 100
        ##self.soma(0.5).nap.gnapbar = 0.018
#
        #self.v1 = h.Vector().record(self.soma(0.5)._ref_ina_Nafin)
        ## self.v2 = h.Vector().record(self.soma(0.5)._ref_ina_nap)
        #self.v3 = h.Vector().record(self.soma(0.5)._ref_ik_kdrin)
        #self.v4 = h.Vector().record(self.soma(0.5)._ref_ik_IKsin)
        ## self.v5 = h.Vector().record(self.soma(0.5)._ref_ik_kc_fast)
        ## self.v6 = h.Vector().record(self.soma(0.5)._ref_ik_km)
        ## self.v7 = h.Vector().record(self.soma(0.5)._ref_ik_k2)
        ## self.v8 = h.Vector().record(self.soma(0.5)._ref_ik_kahp_slower)
        ## self.v9 = h.Vector().record(self.soma(0.5)._ref_ica_cal)
#
        ## ---------------dend----------------
        #for mechanism_d in ['Nafin', 'kdrin', 'kapin', 'pas', 'nap']:
        #    self.dend.insert(mechanism_d)
        #    self.dend1.insert(mechanism_d)
        #    self.dend2.insert(mechanism_d)
        #    self.dend3.insert(mechanism_d)
        #    self.dend4.insert(mechanism_d)
#
        #    # print(mechanism_d)
#
        ## self.dend(0.5).naf2.gbar =   0.2
        #self.dend(0.5).Nafin.gnafbar = 0.00018 * 10
        #self.dend(0.5).kdrin.gkdrbar = 0.018
        #self.dend(0.5).kapin.gkabar = 0.000032 * 15 * 10
        #self.dend(0.5).nap.gnapbar = 0.000018
        #self.dend(0.5).pas.g = 1 / 100
        #self.dend(0.5).pas.e = -73
        #self.dend.Ra = 150
#
        #self.dend1(0.5).Nafin.gnafbar = 0.00018 * 10
        #self.dend1(0.5).kdrin.gkdrbar = 0.018 * 0.5
        #self.dend1(0.5).kapin.gkabar = 0.000032 * 15 * 10
        #self.dend1(0.5).pas.g = 1 / 100
        #self.dend1(0.5).pas.e = -73
        #self.dend1.Ra = 150
        #self.dend1(0.5).nap.gnapbar = 0.000018
#
        #self.dend2(0.5).Nafin.gnafbar = 0.00018 * 10
        #self.dend2(0.5).kdrin.gkdrbar = 0.018 * 0.5
        #self.dend2(0.5).kapin.gkabar = 0.000032 * 15 * 10
        #self.dend2(0.5).pas.g = 1 / 100
        #self.dend2(0.5).pas.e = -73
        #self.dend2.Ra = 150
        #self.dend2(0.5).nap.gnapbar = 0.000018
#
        #self.dend3(0.5).Nafin.gnafbar = 0.00018 * 10
        #self.dend3(0.5).kdrin.gkdrbar = 0.018 * 0.5
        #self.dend3(0.5).kapin.gkabar = 0.000032 * 15 * 10
        #self.dend3(0.5).pas.g = 1 / 100
        #self.dend3(0.5).pas.e = -73
        #self.dend3.Ra = 150
        #self.dend3(0.5).nap.gnapbar = 0.000018
#
        #self.dend4(0.5).Nafin.gnafbar = 0.00018 * 10
        #self.dend4(0.5).kdrin.gkdrbar = 0.018 * 0.5
        #self.dend4(0.5).kapin.gkabar = 0.000032 * 15 * 10
        #self.dend4(0.5).pas.g = 1 / 100
        #self.dend4(0.5).pas.e = -73
        #self.dend4.Ra = 150
        #self.dend4(0.5).nap.gnapbar = 0.000018
#
        #self.vd1 = h.Vector().record(self.dend(0.5)._ref_ina_Nafin)
        ## self.vd2 = h.Vector().record(self.dend(0.5)._ref_ina_napf_spinstell)
        #self.vd3 = h.Vector().record(self.dend(0.5)._ref_ik_kdrin)
        #self.vd4 = h.Vector().record(self.dend(0.5)._ref_ik_kapin)
#
        ## ---------------axon----------------
        #for mechanism_a in ['Nafin', 'kdrin', 'pas']:
        #    self.axon.insert(mechanism_a)
        #    # print(mechanism_a)
#
        #self.axon(0.5).Nafin.gnafbar = 0.5
        #self.axon(0.5).kdrin.gkdrbar = 0.001
        #self.axon(0.5).pas.g = 0.0002
        #self.axon(0.5).pas.e = -73
        #self.axon.Ra = 100
        #self.axon.cm = 1.2
#
        #for sec in self.all:
        #    sec.cm = 1.2
        #   # sec.cm = 0.9
        #    sec.ena = 50.
        #    sec.ek = -90
        for mechanism_s in ['extracellular', 'napf', 'pas', 'naf2_cc', 'kdr_fs_cc', 'kc', 'ka_cc', 'km_cc', 'k2_cc',
                            'kahp_slower', 'cal_cc', 'cat_a', 'ar', 'cad_cc']:
            self.soma.insert(mechanism_s)
            # print(mechanism_s)

        self.soma(0.5).naf2_cc.gbar = 0.6
        self.soma(0.5).napf.gbar = 0.00006
        self.soma(0.5).kdr_fs_cc.gbar = 0.5
        self.soma(0.5).ka_cc.gbar = 0.005
        self.soma(0.5).km_cc.gbar = 0.0005
        self.soma(0.5).kc.gbar = 0.01
        self.soma(0.5).k2_cc.gbar = 0.0005
        self.soma(0.5).kahp_slower.gbar = 0.0001
        self.soma(0.5).cal_cc.gbar = 0.0001
        self.soma(0.5).cat_a.gbar = 5.E-05
        self.soma(0.5).ar.gbar = 2.5E-05
        self.soma(0.5).cad_cc.beta = 0.02
        self.soma(0.5).cad_cc.phi = 10400.
        self.soma(0.5).pas.e = -70
        self.soma(0.5).pas.g = 0.001
        self.soma.Ra = 100.




        # ---------------dend----------------
        for mechanism_d in ['naf_tcr', 'napf_tcr', 'kdr_thlms','ka', 'kc', 'km', 'k2', 'kahp_slower', 'cal_thlms', 'cat_thlms', 'ar', 'cad',  'pas']:
            self.dend.insert(mechanism_d)
            self.dend1.insert(mechanism_d)
            self.dend2.insert(mechanism_d)
            self.dend3.insert(mechanism_d)
            self.dend4.insert(mechanism_d)

            # print(mechanism_d)

        # self.dend(0.5).naf2.gbar =   0.2
        self.dend(0.5).naf_tcr.gbar =   0.1
        self.dend(0.5).napf_tcr.gbar =   0.0002
        self.dend(0.5).kdr_thlms.gbar =   0.075
        self.dend(0.5).kc.gbar =   0.012
        self.dend(0.5).ka.gbar =   0.03
        self.dend(0.5).km.gbar =   0 #// 0.0005
        self.dend(0.5).k2.gbar =   0.002
        self.dend(0.5).cal_thlms.gbar =   0.0005
        self.dend(0.5).cat_thlms.gbar =   0.0005
        self.dend(0.5).ar.gbar =   0.00025
        self.dend(0.5).cad.beta  =   0.02
        self.dend(0.5).cad.phi =   52000.
        self.dend(0.5).pas.g = 1 / 100
        self.dend(0.5).pas.e = -70
        self.dend.Ra = 175

        self.dend1(0.5).naf_tcr.gbar = 0.1
        self.dend1(0.5).napf_tcr.gbar = 0.0002
        self.dend1(0.5).kdr_thlms.gbar = 0.075
        self.dend1(0.5).kc.gbar = 0.012
        self.dend1(0.5).ka.gbar = 0.03
        self.dend1(0.5).km.gbar = 0  # // 0.0005
        self.dend1(0.5).k2.gbar = 0.002
        self.dend1(0.5).cal_thlms.gbar = 0.0005
        self.dend1(0.5).cat_thlms.gbar = 0.0005
        self.dend1(0.5).ar.gbar = 0.00025
        self.dend1(0.5).cad.beta = 0.02
        self.dend1(0.5).cad.phi = 52000.
        self.dend1(0.5).pas.g = 1 / 100
        self.dend1(0.5).pas.e = -70
        self.dend1.Ra = 175

        self.dend2(0.5).naf_tcr.gbar = 0.1
        self.dend2(0.5).napf_tcr.gbar = 0.0002
        self.dend2(0.5).kdr_thlms.gbar = 0.075
        self.dend2(0.5).kc.gbar = 0.012
        self.dend2(0.5).ka.gbar = 0.03
        self.dend2(0.5).km.gbar = 0  # // 0.0005
        self.dend2(0.5).k2.gbar = 0.002
        self.dend2(0.5).cal_thlms.gbar = 0.0005
        self.dend2(0.5).cat_thlms.gbar = 0.0005
        self.dend2(0.5).ar.gbar = 0.00025
        self.dend2(0.5).cad.beta = 0.02
        self.dend2(0.5).cad.phi = 52000.
        self.dend2(0.5).pas.g = 1 / 100
        self.dend2(0.5).pas.e = -70
        self.dend2.Ra = 175

        self.dend3(0.5).naf_tcr.gbar = 0.1
        self.dend3(0.5).napf_tcr.gbar = 0.0002
        self.dend3(0.5).kdr_thlms.gbar = 0.075
        self.dend3(0.5).kc.gbar = 0.012
        self.dend3(0.5).ka.gbar = 0.03
        self.dend3(0.5).km.gbar = 0  # // 0.0005
        self.dend3(0.5).k2.gbar = 0.002
        self.dend3(0.5).cal_thlms.gbar = 0.0005
        self.dend3(0.5).cat_thlms.gbar = 0.0005
        self.dend3(0.5).ar.gbar = 0.00025
        self.dend3(0.5).cad.beta = 0.02
        self.dend3(0.5).cad.phi = 52000.
        self.dend3(0.5).pas.g = 1 / 100
        self.dend3(0.5).pas.e = -70
        self.dend3.Ra = 175

        self.dend4(0.5).naf_tcr.gbar = 0.1
        self.dend4(0.5).napf_tcr.gbar = 0.0002
        self.dend4(0.5).kdr_thlms.gbar = 0.075
        self.dend4(0.5).kc.gbar = 0.012
        self.dend4(0.5).ka.gbar = 0.03
        self.dend4(0.5).km.gbar = 0  # // 0.0005
        self.dend4(0.5).k2.gbar = 0.002
        self.dend4(0.5).cal_thlms.gbar = 0.0005
        self.dend4(0.5).cat_thlms.gbar = 0.0005
        self.dend4(0.5).ar.gbar = 0.00025
        self.dend4(0.5).cad.beta = 0.02
        self.dend4(0.5).cad.phi = 52000.
        self.dend4(0.5).pas.g = 1 / 100
        self.dend4(0.5).pas.e = -70
        self.dend4.Ra = 175


        # ---------------axon----------------
        for mechanism_a in ['Nafin', 'kdrin', 'pas']:
            self.axon.insert(mechanism_a)
            # print(mechanism_a)

        self.axon(0.5).Nafin.gnafbar = 0.4
        self.axon(0.5).kdrin.gkdrbar = 0.001
        self.axon(0.5).pas.g = 0.005
        self.axon(0.5).pas.e = -70
        self.axon.Ra = 100
        #self.axon.cm = 1.2

        for sec in self.all:
            sec.cm = 0.9
            sec.ena = 50.
            sec.ek = -95
        # self.dend1(0.5).Nafin.gnafbar = 0.00018 * 10
        # self.dend1(0.5).kdrin.gkdrbar = 0.00018 * 0.5
        # self.dend1(0.5).kapin.gkabar = 0.000032 #* 15 * 10
        # self.dend1(0.5).pas.g = 1 / 100
        # self.dend1(0.5).pas.e = -73
        # self.dend1.Ra = 150
        # self.dend1(0.5).nap.gnapbar = 0.000018
        #
        # self.dend2(0.5).Nafin.gnafbar = 0.00018 * 10
        # self.dend2(0.5).kdrin.gkdrbar = 0.00018 * 0.5
        # self.dend2(0.5).kapin.gkabar = 0.000032 #* 15 * 10
        # self.dend2(0.5).pas.g = 1 / 100
        # self.dend2(0.5).pas.e = -73
        # self.dend2.Ra = 150
        # self.dend2(0.5).nap.gnapbar = 0.000018
        #
        # self.dend3(0.5).Nafin.gnafbar = 0.0018 * 10
        # self.dend3(0.5).kdrin.gkdrbar = 0.00018 * 0.5
        # self.dend3(0.5).kapin.gkabar = 0.000032 #* 15 * 10
        # self.dend3(0.5).pas.g = 1 / 100
        # self.dend3(0.5).pas.e = -73
        # self.dend3.Ra = 150
        # self.dend3(0.5).nap.gnapbar = 0.000018
        #
        # self.dend4(0.5).Nafin.gnafbar = 0.0018 * 10
        # self.dend4(0.5).kdrin.gkdrbar = 0.0018 * 0.5
        # self.dend4(0.5).kapin.gkabar = 0.000032 #* 15 * 10
        # self.dend4(0.5).pas.g = 1 / 100
        # self.dend4(0.5).pas.e = -73
        # self.dend4.Ra = 150
        # self.dend4(0.5).nap.gnapbar = 0.000018

        # ---------------axon----------------


        self.k_vec = h.Vector().record(self.soma(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.soma(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.soma(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.soma(0.5)._ref_ki)
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_vext[0])
        self.cyt = rxd.Region(self.all, name='cyt', nrn_region='i', dx=1.0,
                              geometry=rxd.FractionalVolume(0.9, surface_fraction=1.0))
        self.na = rxd.Species([self.cyt], name='na', charge=1, d=1.0, initial=10)
        self.k = rxd.Species([self.cyt], name='k', charge=1, d=1.0, initial=148)
        self.k_i = self.k[self.cyt]
        self.ca = rxd.Species([self.cyt], d=0.08, name='ca', charge=2, initial=1.e-4, atolscale=1e-6)
        #------for test-----------
        #self.stim = h.IClamp(self.soma(0.5))
        #self.stim.delay = 50
        #self.stim.dur = 1
        #self.stim.amp = 1
       # print(self.id)

class EpilepsyNontuftRS6(Cell):  #
    def __init__(self, x, y, z, num):
        super().__init__(x , y, z, num)
        self.id = 10
        self.Excitatory = 1
        self.name ='pyramidal nontufted regular spiking'

        # ---------------soma----------------
        #for mechanism_s in ['extracellular', 'Nafin', 'kdrin', 'IKsin', 'hin', 'kapin', 'canin', 'kctin', 'cadynin',
        #                    'pas']:
        #    self.soma.insert(mechanism_s)
#
        #self.soma(0.5).Nafin.gnafbar = 0.5
        #self.soma(0.5).kdrin.gkdrbar = 0.001
        #self.soma(0.5).IKsin.gKsbar = 0.000725 * 0.1
        #self.soma(0.5).hin.gbar = 0.00001
        #self.soma(0.5).kapin.gkabar = 0.0032 * 15
        #self.soma(0.5).canin.gcalbar = 0.0003
        #self.soma(0.5).kctin.gkcbar = 0.0001
        #self.soma(0.5).pas.g = 0.0002
        #self.soma(0.5).pas.e = -70
        #self.soma.Ra = 100
        ##self.soma(0.5).nap.gnapbar = 0.018
#
        #self.v1 = h.Vector().record(self.soma(0.5)._ref_ina_Nafin)
        ## self.v2 = h.Vector().record(self.soma(0.5)._ref_ina_nap)
        #self.v3 = h.Vector().record(self.soma(0.5)._ref_ik_kdrin)
        #self.v4 = h.Vector().record(self.soma(0.5)._ref_ik_IKsin)
        ## self.v5 = h.Vector().record(self.soma(0.5)._ref_ik_kc_fast)
        ## self.v6 = h.Vector().record(self.soma(0.5)._ref_ik_km)
        ## self.v7 = h.Vector().record(self.soma(0.5)._ref_ik_k2)
        ## self.v8 = h.Vector().record(self.soma(0.5)._ref_ik_kahp_slower)
        ## self.v9 = h.Vector().record(self.soma(0.5)._ref_ica_cal)
#
        ## ---------------dend----------------
        #for mechanism_d in ['Nafin', 'kdrin', 'kapin', 'pas', 'nap']:
        #    self.dend.insert(mechanism_d)
        #    self.dend1.insert(mechanism_d)
        #    self.dend2.insert(mechanism_d)
        #    self.dend3.insert(mechanism_d)
        #    self.dend4.insert(mechanism_d)
#
        #    # print(mechanism_d)
#
        ## self.dend(0.5).naf2.gbar =   0.2
        #self.dend(0.5).Nafin.gnafbar = 0.00018 * 10
        #self.dend(0.5).kdrin.gkdrbar = 0.018
        #self.dend(0.5).kapin.gkabar = 0.000032 * 15 * 10
        #self.dend(0.5).nap.gnapbar = 0.000018
        #self.dend(0.5).pas.g = 1 / 100
        #self.dend(0.5).pas.e = -73
        #self.dend.Ra = 150
#
        #self.dend1(0.5).Nafin.gnafbar = 0.00018 * 10
        #self.dend1(0.5).kdrin.gkdrbar = 0.018 * 0.5
        #self.dend1(0.5).kapin.gkabar = 0.000032 * 15 * 10
        #self.dend1(0.5).pas.g = 1 / 100
        #self.dend1(0.5).pas.e = -73
        #self.dend1.Ra = 150
        #self.dend1(0.5).nap.gnapbar = 0.000018
#
        #self.dend2(0.5).Nafin.gnafbar = 0.00018 * 10
        #self.dend2(0.5).kdrin.gkdrbar = 0.018 * 0.5
        #self.dend2(0.5).kapin.gkabar = 0.000032 * 15 * 10
        #self.dend2(0.5).pas.g = 1 / 100
        #self.dend2(0.5).pas.e = -73
        #self.dend2.Ra = 150
        #self.dend2(0.5).nap.gnapbar = 0.000018
#
        #self.dend3(0.5).Nafin.gnafbar = 0.00018 * 10
        #self.dend3(0.5).kdrin.gkdrbar = 0.018 * 0.5
        #self.dend3(0.5).kapin.gkabar = 0.000032 * 15 * 10
        #self.dend3(0.5).pas.g = 1 / 100
        #self.dend3(0.5).pas.e = -73
        #self.dend3.Ra = 150
        #self.dend3(0.5).nap.gnapbar = 0.000018
#
        #self.dend4(0.5).Nafin.gnafbar = 0.00018 * 10
        #self.dend4(0.5).kdrin.gkdrbar = 0.018 * 0.5
        #self.dend4(0.5).kapin.gkabar = 0.000032 * 15 * 10
        #self.dend4(0.5).pas.g = 1 / 100
        #self.dend4(0.5).pas.e = -73
        #self.dend4.Ra = 150
        #self.dend4(0.5).nap.gnapbar = 0.000018
#
        #self.vd1 = h.Vector().record(self.dend(0.5)._ref_ina_Nafin)
        ## self.vd2 = h.Vector().record(self.dend(0.5)._ref_ina_napf_spinstell)
        #self.vd3 = h.Vector().record(self.dend(0.5)._ref_ik_kdrin)
        #self.vd4 = h.Vector().record(self.dend(0.5)._ref_ik_kapin)
#
        ## ---------------axon----------------
        #for mechanism_a in ['Nafin', 'kdrin', 'pas']:
        #    self.axon.insert(mechanism_a)
        #    # print(mechanism_a)
#
        #self.axon(0.5).Nafin.gnafbar = 0.5
        #self.axon(0.5).kdrin.gkdrbar = 0.001
        #self.axon(0.5).pas.g = 0.0002
        #self.axon(0.5).pas.e = -73
        #self.axon.Ra = 100
        #self.axon.cm = 1.2
#
        #for sec in self.all:
        #    sec.cm = 1.2
        #   # sec.cm = 0.9
        #    sec.ena = 50.
        #    sec.ek = -90
        for mechanism_s in ['extracellular', 'naf2_cc', 'pas', 'napf_spinstell', 'kdr_fs_cc', 'kc_fast_cc', 'ka_cc',
                        'km_cc', 'k2_cc', 'kahp_slower', 'cal_cc', 'cat_cc', 'ar', 'cad_cc']:
            self.soma.insert(mechanism_s)
        # print(mechanism_s)

        self.soma(0.5).naf2_cc.gbar = 0.65
        self.soma(0.5).napf_spinstell.gbar = 0.0002
        self.soma(0.5).kdr_fs_cc.gbar = 0.1 * 10
        self.soma(0.5).kc_fast_cc.gbar = 0.001 * 10
        self.soma(0.5).ka_cc.gbar = 0.03
        self.soma(0.5).km_cc.gbar = 0.00375
        self.soma(0.5).k2_cc.gbar = 0.0001
        self.soma(0.5).kahp_slower.gbar = 0.0001
        self.soma(0.5).cal_cc.gbar = 0.0005
        self.soma(0.5).cat_cc.gbar = 0.0001
        self.soma(0.5).ar.gbar = 0.00025
        self.soma(0.5).cad_cc.beta = 0.02
        self.soma(0.5).cad_cc.phi = 260000.
        self.soma(0.5).pas.g = 0.001
        self.soma(0.5).pas.e = -65
        self.soma.Ra = 150.

        # ---------------dend----------------
        for mechanism_d in ['naf2_cc', 'napf_spinstell', 'pas', 'kdr_fs_cc', 'kc_fast_cc', 'ka_cc', 'km_cc', 'k2_cc',
                            'kahp_slower', 'cal_cc', 'cat_cc', 'ar', 'cad_cc']:
            self.dend.insert(mechanism_d)
            self.dend1.insert(mechanism_d)
            self.dend2.insert(mechanism_d)
            self.dend3.insert(mechanism_d)
            self.dend4.insert(mechanism_d)
            # print(mechanism_d)

        self.dend(0.5).naf2_cc.gbar = 0.0075
        self.dend(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend(0.5).kc_fast_cc.gbar = 0.01
        self.dend(0.5).ka_cc.gbar = 0.03
        self.dend(0.5).km_cc.gbar = 0.00375
        self.dend(0.5).k2_cc.gbar = 0.0001
        self.dend(0.5).kahp_slower.gbar = 0.0001
        self.dend(0.5).cal_cc.gbar = 0.0005
        self.dend(0.5).cat_cc.gbar = 0.0001
        self.dend(0.5).ar.gbar = 0.00025
        self.dend(0.5).cad_cc.beta = 0.05
        self.dend(0.5).cad_cc.phi = 260000.
        self.dend(0.5).pas.g = 0.02
        self.dend(0.5).pas.e = -65
        self.dend.Ra = 250.

        self.dend1(0.5).naf2_cc.gbar = 0.0075
        self.dend1(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend1(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend1(0.5).kc_fast_cc.gbar = 0.01
        self.dend1(0.5).ka_cc.gbar = 0.03
        self.dend1(0.5).km_cc.gbar = 0.00375
        self.dend1(0.5).k2_cc.gbar = 0.0001
        self.dend1(0.5).kahp_slower.gbar = 0.0001
        self.dend1(0.5).cal_cc.gbar = 0.0005
        self.dend1(0.5).cat_cc.gbar = 0.0001
        self.dend1(0.5).ar.gbar = 0.00025
        self.dend1(0.5).cad_cc.beta = 0.05
        self.dend1(0.5).cad_cc.phi = 260000.
        self.dend1(0.5).pas.g = 0.02
        self.dend1(0.5).pas.e = -65
        self.dend1.Ra = 250.

        self.dend2(0.5).naf2_cc.gbar = 0.0075
        self.dend2(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend2(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend2(0.5).kc_fast_cc.gbar = 0.01
        self.dend2(0.5).ka_cc.gbar = 0.03
        self.dend2(0.5).km_cc.gbar = 0.00375
        self.dend2(0.5).k2_cc.gbar = 0.0001
        self.dend2(0.5).kahp_slower.gbar = 0.0001
        self.dend2(0.5).cal_cc.gbar = 0.0005
        self.dend2(0.5).cat_cc.gbar = 0.0001
        self.dend2(0.5).ar.gbar = 0.00025
        self.dend2(0.5).cad_cc.beta = 0.05
        self.dend2(0.5).cad_cc.phi = 260000.
        self.dend2(0.5).pas.g = 0.02
        self.dend2(0.5).pas.e = -65
        self.dend2.Ra = 250.

        self.dend3(0.5).naf2_cc.gbar = 0.0075
        self.dend3(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend3(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend3(0.5).kc_fast_cc.gbar = 0.01
        self.dend3(0.5).ka_cc.gbar = 0.03
        self.dend3(0.5).km_cc.gbar = 0.00375
        self.dend3(0.5).k2_cc.gbar = 0.0001
        self.dend3(0.5).kahp_slower.gbar = 0.0001
        self.dend3(0.5).cal_cc.gbar = 0.0005
        self.dend3(0.5).cat_cc.gbar = 0.0001
        self.dend3(0.5).ar.gbar = 0.00025
        self.dend3(0.5).cad_cc.beta = 0.05
        self.dend3(0.5).cad_cc.phi = 260000.
        self.dend3(0.5).pas.g = 0.02
        self.dend3(0.5).pas.e = -65
        self.dend3.Ra = 250.

        self.dend4(0.5).naf2_cc.gbar = 0.0075
        self.dend4(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend4(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend4(0.5).kc_fast_cc.gbar = 0.01
        self.dend4(0.5).ka_cc.gbar = 0.03
        self.dend4(0.5).km_cc.gbar = 0.00375
        self.dend4(0.5).k2_cc.gbar = 0.0001
        self.dend4(0.5).kahp_slower.gbar = 0.0001
        self.dend4(0.5).cal_cc.gbar = 0.0005
        self.dend4(0.5).cat_cc.gbar = 0.0001
        self.dend4(0.5).ar.gbar = 0.00025
        self.dend4(0.5).cad_cc.beta = 0.05
        self.dend4(0.5).cad_cc.phi = 260000.
        self.dend4(0.5).pas.g = 0.02
        self.dend4(0.5).pas.e = -65
        self.dend4.Ra = 250.

        # self.vd1 = h.Vector().record(self.dend(0.5)._ref_ina_naf2)
        # self.vd2 = h.Vector().record(self.dend(0.5)._ref_ina_napf_spinstell)
        # self.vd3 = h.Vector().record(self.dend(0.5)._ref_ik_kdr_fs)
        # self.vd4 = h.Vector().record(self.dend(0.5)._ref_ik_ka)
        # self.vd5 = h.Vector().record(self.dend(0.5)._ref_ik_kc_fast)
        # self.vd7 = h.Vector().record(self.dend(0.5)._ref_ik_k2)
        # self.vd8 = h.Vector().record(self.dend(0.5)._ref_ik_kahp_slower)
        # self.vd9 = h.Vector().record(self.dend(0.5)._ref_ica_cal)

        # ---------------axon----------------
        for mechanism_a in ['naf2_cc', 'kdr_fs_cc', 'ka_cc', 'k2_cc', 'pas']:
            self.axon.insert(mechanism_a)
            # print(mechanism_a)

        self.axon(0.5).naf2_cc.gbar = 0.1 * 4
        self.axon(0.5).kdr_fs_cc.gbar = 0.9
        self.axon(0.5).ka_cc.gbar = 0.002
        self.axon(0.5).k2_cc.gbar = 0.1
        self.axon(0.5).pas.g = 0.01
        self.axon(0.5).pas.e = -65
        self.axon.Ra = 100.

        for sec in self.all:
            sec.cm = 0.9
            sec.ena = 50.
            sec.ek = -90
        # self.dend1(0.5).Nafin.gnafbar = 0.00018 * 10
        # self.dend1(0.5).kdrin.gkdrbar = 0.00018 * 0.5
        # self.dend1(0.5).kapin.gkabar = 0.000032 #* 15 * 10
        # self.dend1(0.5).pas.g = 1 / 100
        # self.dend1(0.5).pas.e = -73
        # self.dend1.Ra = 150
        # self.dend1(0.5).nap.gnapbar = 0.000018
        #
        # self.dend2(0.5).Nafin.gnafbar = 0.00018 * 10
        # self.dend2(0.5).kdrin.gkdrbar = 0.00018 * 0.5
        # self.dend2(0.5).kapin.gkabar = 0.000032 #* 15 * 10
        # self.dend2(0.5).pas.g = 1 / 100
        # self.dend2(0.5).pas.e = -73
        # self.dend2.Ra = 150
        # self.dend2(0.5).nap.gnapbar = 0.000018
        #
        # self.dend3(0.5).Nafin.gnafbar = 0.0018 * 10
        # self.dend3(0.5).kdrin.gkdrbar = 0.00018 * 0.5
        # self.dend3(0.5).kapin.gkabar = 0.000032 #* 15 * 10
        # self.dend3(0.5).pas.g = 1 / 100
        # self.dend3(0.5).pas.e = -73
        # self.dend3.Ra = 150
        # self.dend3(0.5).nap.gnapbar = 0.000018
        #
        # self.dend4(0.5).Nafin.gnafbar = 0.0018 * 10
        # self.dend4(0.5).kdrin.gkdrbar = 0.0018 * 0.5
        # self.dend4(0.5).kapin.gkabar = 0.000032 #* 15 * 10
        # self.dend4(0.5).pas.g = 1 / 100
        # self.dend4(0.5).pas.e = -73
        # self.dend4.Ra = 150
        # self.dend4(0.5).nap.gnapbar = 0.000018

        # ---------------axon----------------


        self.k_vec = h.Vector().record(self.soma(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.soma(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.soma(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.soma(0.5)._ref_ki)
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_vext[0])
        self.cyt = rxd.Region(self.all, name='cyt', nrn_region='i', dx=1.0,
                              geometry=rxd.FractionalVolume(0.9, surface_fraction=1.0))
        self.na = rxd.Species([self.cyt], name='na', charge=1, d=1.0, initial=10)
        self.k = rxd.Species([self.cyt], name='k', charge=1, d=1.0, initial=148)
        self.k_i = self.k[self.cyt]
        self.ca = rxd.Species([self.cyt], d=0.08, name='ca', charge=2, initial=1.e-4, atolscale=1e-6)
        #------for test-----------
        #self.stim = h.IClamp(self.soma(0.5))
        #self.stim.delay = 50
        #self.stim.dur = 1
        #self.stim.amp = 1
       # print(self.id)

'''

class Bask4(Cell):  #
    def __init__(self, x, y, z, num):
        super().__init__(x , y, z, num)
        self.id = 11
        self.Excitatory = 1
        self.name ='bask 4'
        #self.soma.nseg = 1+2*int(somaR*2/40)
        
        # ---------------soma----------------
        for mechanism_s in ['extracellular', 'pas','Ih', 'NaV', 'Kd', 'Kv2like', 'Kv3_1', 'K_T', 'Im_v2', 'SK', 'Ca_HVA', 'Ca_LVA', 'CaDynamics']:
            self.soma.insert(mechanism_s)
            #print(mechanism_s)

        self.soma(0.5).Ih.gbar = 0.00080878256233100009
        self.soma(0.5).NaV.gbar = 0.22494483174199997
        self.soma(0.5).Kd.gbar = 0.0
        self.soma(0.5).Kv2like.gbar = 0.634543840079
        self.soma(0.5).Kv3_1.gbar = 0.566198697679
        self.soma(0.5).K_T.gbar = 0.056532023518500001
        self.soma(0.5).Im_v2.gbar = 0.018603641341
        self.soma(0.5).SK.gbar = 0.0
        self.soma(0.5).Ca_HVA.gbar = 0.00022584367833099997
        self.soma(0.5).Ca_LVA.gbar = 0.00574872727545
        self.soma(0.5).CaDynamics.gamma = 0.024961434791900005
        self.soma(0.5).CaDynamics.decay = 465.51479610500002
        self.soma(0.5).pas.e = -85.15087381998698
        self.soma(0.5).pas.g = 1.3446992367900001e-05
        self.soma.ek = -107.0
        self.soma.ena = 53


        # ---------------dend----------------
        self.dend.nseg = 1+2*int(dendL/40)
        for mechanism_d in ['pas']:
            self.dend.insert(mechanism_d)
            #print(mechanism_d)

        
        self.dend(0.5).pas.e = -85.15087381998698
        self.dend(0.5).pas.g = 2.90017977354e-06
        

        # ---------------axon----------------
        self.soma.nseg = 1+2*int(axonL/40)
        for mechanism_a in ['pas']:
            self.axon.insert(mechanism_a)
            #print(mechanism_a)


        self.axon(0.5).pas.g = 3.0949651596799999e-05
        self.axon(0.5).pas.e = -85.15087381998698
        self.axon.Ra = 100

        for sec in self.all:        
            sec.cm = 4.65
            sec.Ra = 65.22
            #sec.pas.e = -85.15087381998698


        self.k_vec = h.Vector().record(self.soma(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.soma(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.soma(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.soma(0.5)._ref_ki)
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_vext[0])
        self.cyt = rxd.Region(self.all, name='cyt', nrn_region='i', dx=1.0,
                              geometry=rxd.FractionalVolume(0.9, surface_fraction=1.0))
        self.na = rxd.Species([self.cyt], name='na', charge=1, d=1.0, initial=10)
        self.k = rxd.Species([self.cyt], name='k', charge=1, d=1.0, initial=148)
        self.k_i = self.k[self.cyt]
        self.ca = rxd.Species([self.cyt], d=0.08, name='ca', charge=2, initial=1.e-4, atolscale=1e-6)
        #------for test-----------
        #self.stim = h.IClamp(self.soma(0.5))
        #self.stim.delay = 50
        #self.stim.dur = 1
        #self.stim.amp = 1
        #print(self.id)
    def connect(self, target):
            self.nc = h.NetCon(self.soma(0.5)._ref_v, target.synE, sec=self.soma)
            self.nc.weight[0] = 10
            self.nc.delay = 5
            target._ncs.append(self.nc)
            target.count+=1
            target.cells[self.number]=self.id
'''

class SyppyrFRB(Cell):  #
    def __init__(self, x, y, z, num):
        super().__init__(x , y, z, num)
        self.id = 12
        self.Excitatory = 1
        self.name ='pyramidal fast rythmic bursting'
        #self.soma.nseg = 1+2*int(somaR*2/40)

        # ---------------soma----------------
        for mechanism_s in ['extracellular', 'Naf', 'nap', 'calc', 'cal', 'can', 'car', 'cat', 'kdrpr', 'IKs', 'kad',
                            'h',
                            'kca', 'ican', 'cadyn',
                            'pas']:
            # print(mechanism_s)
            self.soma.insert(mechanism_s)

        self.soma(0.5).Naf.gnafbar = 0.018 * 3
        self.soma(0.5).nap.gnapbar = 0.000018
        self.soma(0.5).calc.gcabar = 0.0001 * 0.1
        self.soma(0.5).cal.gcalbar = 0.0001 * 0.3
        self.soma(0.5).can.gcabar = 0.0002 * 0.1
        self.soma(0.5).car.gcabar = 0.000001 * 0.3 * 0.1
        self.soma(0.5).cat.gcatbar = 0.0002 * 0.3 * 0.1
        self.soma(0.5).kdrpr.gkdrbar = 0.018 * 0.3
        self.soma(0.5).IKs.gKsbar = 0.0012 * 0.5
        self.soma(0.5).kad.gkabar = 0.0007
        self.soma(0.5).kca.gbar = 0.005 * 5
        self.soma(0.5).h.gbar = 1.8e-5 * 0.5
        self.soma(0.5).ican.gbar = 0.001 * 0.07 * 0
        self.soma(0.5).pas.g = 0.01
        self.soma(0.5).pas.e = -65
        self.soma.Ra = 100

        # self.v1 = h.Vector().record(self.soma(0.5)._ref_ina_Nafin)
        # self.v2 = h.Vector().record(self.soma(0.5)._ref_ina_nap)
        # self.v3 = h.Vector().record(self.soma(0.5)._ref_ik_kdrin)
        # self.v4 = h.Vector().record(self.soma(0.5)._ref_ik_IKsin)
        # self.v5 = h.Vector().record(self.soma(0.5)._ref_ik_kc_fast)
        # self.v6 = h.Vector().record(self.soma(0.5)._ref_ik_km)
        # self.v7 = h.Vector().record(self.soma(0.5)._ref_ik_k2)
        # self.v8 = h.Vector().record(self.soma(0.5)._ref_ik_kahp_slower)
        # self.v9 = h.Vector().record(self.soma(0.5)._ref_ica_cal)

        # ---------------dend----------------
        for mechanism_d in ['Naf', 'nap', 'calc', 'cal', 'can', 'car', 'cat', 'kdrpr', 'IKs', 'kad', 'h', 'kca', 'ican',
                            'cadyn', 'pas']:
            self.dend.insert(mechanism_d)
            self.dend1.insert(mechanism_d)
            self.dend2.insert(mechanism_d)
            self.dend3.insert(mechanism_d)
            self.dend4.insert(mechanism_d)

            # print(mechanism_d)

        self.dend(0.5).Naf.gnafbar = 0.018 * 0.1
        self.dend(0.5).nap.gnapbar = 0.000018
        self.dend(0.5).calc.gcabar = 0.0001 * 0.1  #
        self.dend(0.5).cal.gcalbar = 0.0001 * 0.3  #
        self.dend(0.5).can.gcabar = 0.0002 * 0.3
        self.dend(0.5).car.gcabar = 0.000001 * 0.3 * 0.1 * 0.3  #
        self.dend(0.5).cat.gcatbar = 0.0002 * 0.3 * 0.1  #
        self.dend(0.5).kdrpr.gkdrbar = 0.018 * 0.09
        self.dend(0.5).IKs.gKsbar = 0.0012
        self.dend(0.5).kad.gkabar = 0.0007
        self.dend(0.5).kca.gbar = 0.005 * 5 * 0.001  #
        self.dend(0.5).h.gbar = 1.8e-5 * 0.5  #
        self.dend(0.5).ican.gbar = 0.001 * 0.07 * 0.1  #
        self.dend(0.5).pas.g = 0.01
        self.dend(0.5).pas.e = -65
        self.dend.Ra = 150

        self.dend1(0.5).Naf.gnafbar = 0.018 * 0.4
        self.dend1(0.5).nap.gnapbar = 0.000018  # * 3
        self.dend1(0.5).calc.gcabar = 0.0001 * 0.1  #
        self.dend1(0.5).cal.gcalbar = 0.0001 * 0.3  #
        self.dend1(0.5).can.gcabar = 0.0002 * 0.3
        self.dend1(0.5).car.gcabar = 0.000001 * 0.3 * 0.1 * 0.3  #
        self.dend1(0.5).cat.gcatbar = 0.0002 * 0.3 * 0.1  #
        self.dend1(0.5).kdrpr.gkdrbar = 0.018 * 0.09
        self.dend1(0.5).IKs.gKsbar = 0.0012
        self.dend1(0.5).kad.gkabar = 0.0007
        self.dend1(0.5).kca.gbar = 0.005 * 5 * 0.0001  #
        self.dend1(0.5).h.gbar = 1.8e-5 * 0.5  #
        self.dend1(0.5).ican.gbar = 0.001 * 0.07 * 0.1  #
        self.dend1(0.5).pas.g = 0.01
        self.dend1(0.5).pas.e = -65
        self.dend1.Ra = 150

        self.dend2(0.5).Naf.gnafbar = 0.018 * 0.1
        self.dend2(0.5).nap.gnapbar = 0.000018
        self.dend2(0.5).calc.gcabar = 0.0001 * 0.1  #
        self.dend2(0.5).cal.gcalbar = 0.0001 * 0.3  #
        self.dend2(0.5).can.gcabar = 0.0002 * 0.3
        self.dend2(0.5).car.gcabar = 0.000001 * 0.3 * 0.1 * 0.3  #
        self.dend2(0.5).cat.gcatbar = 0.0002 * 0.3 * 0.1  #
        self.dend2(0.5).kdrpr.gkdrbar = 0.018 * 0.09
        self.dend2(0.5).IKs.gKsbar = 0.0012
        self.dend2(0.5).kad.gkabar = 0.0007
        self.dend2(0.5).kca.gbar = 0.005 * 5 * 0.001  #
        self.dend2(0.5).h.gbar = 1.8e-5 * 0.5  #
        self.dend2(0.5).ican.gbar = 0.001 * 0.07 * 0.1  #
        self.dend2(0.5).pas.g = 0.01
        self.dend2(0.5).pas.e = -65
        self.dend2.Ra = 150

        self.dend3(0.5).Naf.gnafbar = 0.018 * 0.1
        self.dend3(0.5).nap.gnapbar = 0.000018
        self.dend3(0.5).calc.gcabar = 0.0001 * 0.1  #
        self.dend3(0.5).cal.gcalbar = 0.0001 * 0.3  #
        self.dend3(0.5).can.gcabar = 0.0002 * 0.3
        self.dend3(0.5).car.gcabar = 0.000001 * 0.3 * 0.1 * 0.3  #
        self.dend3(0.5).cat.gcatbar = 0.0002 * 0.3 * 0.1  #
        self.dend3(0.5).kdrpr.gkdrbar = 0.018 * 0.09
        self.dend3(0.5).IKs.gKsbar = 0.0012
        self.dend3(0.5).kad.gkabar = 0.0007
        self.dend3(0.5).kca.gbar = 0.005 * 5 * 0.001  #
        self.dend3(0.5).h.gbar = 1.8e-5 * 0.5  #
        self.dend3(0.5).ican.gbar = 0.001 * 0.07 * 0.1  #
        self.dend3(0.5).pas.g = 0.01
        self.dend3(0.5).pas.e = -65
        self.dend3.Ra = 150

        self.dend4(0.5).Naf.gnafbar = 0.018 * 0.1
        self.dend4(0.5).nap.gnapbar = 0.000018
        self.dend4(0.5).calc.gcabar = 0.0001 * 0.1  #
        self.dend4(0.5).cal.gcalbar = 0.0001 * 0.3  #
        self.dend4(0.5).can.gcabar = 0.0002 * 0.3
        self.dend4(0.5).car.gcabar = 0.000001 * 0.3 * 0.1 * 0.3  #
        self.dend4(0.5).cat.gcatbar = 0.0002 * 0.3 * 0.1  #
        self.dend4(0.5).kdrpr.gkdrbar = 0.018 * 0.09
        self.dend4(0.5).IKs.gKsbar = 0.0012
        self.dend4(0.5).kad.gkabar = 0.0007
        self.dend4(0.5).kca.gbar = 0.005 * 5 * 0.001  #
        self.dend4(0.5).h.gbar = 1.8e-5 * 0.5  #
        self.dend4(0.5).ican.gbar = 0.001 * 0.07 * 0.1  #
        self.dend4(0.5).pas.g = 0.01
        self.dend4(0.5).pas.e = -65
        self.dend4.Ra = 150

        # ---------------axon----------------
        for mechanism_a in ['Nafin', 'kdrin', 'pas']:
            self.axon.insert(mechanism_a)
            # print(mechanism_a)

        self.axon(0.5).Nafin.gnafbar = 0.4
        self.axon(0.5).kdrin.gkdrbar = 0.001
        self.axon(0.5).pas.g = 0.0002
        self.axon(0.5).pas.e = -73
        self.axon.Ra = 100
        self.axon.cm = 1.2

        for sec in self.all:
            sec.cm = 0.9
            sec.ena = 50.
            sec.ek = -95.

        self.k_vec = h.Vector().record(self.soma(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.soma(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.soma(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.soma(0.5)._ref_ki)
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_vext[0])
        self.cyt = rxd.Region(self.all, name='cyt', nrn_region='i', dx=1.0,
                              geometry=rxd.FractionalVolume(0.9, surface_fraction=1.0))
        self.na = rxd.Species([self.cyt], name='na', charge=1, d=1.0, initial=10)
        self.k = rxd.Species([self.cyt], name='k', charge=1, d=1.0, initial=148)
        self.k_i = self.k[self.cyt]
        self.ca = rxd.Species([self.cyt], d=0.08, name='ca', charge=2, initial=1.e-4, atolscale=1e-6)
        #------for test-----------
        #self.stim = h.IClamp(self.soma(0.5))
        #self.stim.delay = 50
        #self.stim.dur = 1
        #self.stim.amp = 1
        #print(self.id)



class SyppyrRS(Cell):  #
    def __init__(self, x, y, z, num):
        super().__init__(x , y, z, num)
        self.id = 13
        self.Excitatory = 1
        self.name ='pyramidal regular spiking'
        #self.soma.nseg = 1+2*int(somaR*2/40)

        # ---------------soma----------------
        for mechanism_s in ['extracellular', 'Naf', 'nap', 'calc', 'cal', 'can', 'car', 'cat', 'kdrpr', 'IKs', 'kad',
                            'h',
                            'kca', 'ican', 'cadyn',
                            'pas']:
            # print(mechanism_s)
            self.soma.insert(mechanism_s)

        self.soma(0.5).Naf.gnafbar = 0.018 * 3
        self.soma(0.5).nap.gnapbar = 0.000018
        self.soma(0.5).calc.gcabar = 0.0001 * 0.1
        self.soma(0.5).cal.gcalbar = 0.0001 * 0.3
        self.soma(0.5).can.gcabar = 0.0002 * 0.1
        self.soma(0.5).car.gcabar = 0.000001 * 0.3 * 0.1
        self.soma(0.5).cat.gcatbar = 0.0002 * 0.3 * 0.1
        self.soma(0.5).kdrpr.gkdrbar = 0.018 * 0.3
        self.soma(0.5).IKs.gKsbar = 0.0012 * 0.5
        self.soma(0.5).kad.gkabar = 0.0007
        self.soma(0.5).kca.gbar = 0.005 * 5
        self.soma(0.5).h.gbar = 1.8e-5 * 0.5
        self.soma(0.5).ican.gbar = 0.001 * 0.07 * 0
        self.soma(0.5).pas.g = 0.01
        self.soma(0.5).pas.e = -65
        self.soma.Ra = 100

        # self.v1 = h.Vector().record(self.soma(0.5)._ref_ina_Nafin)
        # self.v2 = h.Vector().record(self.soma(0.5)._ref_ina_nap)
        # self.v3 = h.Vector().record(self.soma(0.5)._ref_ik_kdrin)
        # self.v4 = h.Vector().record(self.soma(0.5)._ref_ik_IKsin)
        # self.v5 = h.Vector().record(self.soma(0.5)._ref_ik_kc_fast)
        # self.v6 = h.Vector().record(self.soma(0.5)._ref_ik_km)
        # self.v7 = h.Vector().record(self.soma(0.5)._ref_ik_k2)
        # self.v8 = h.Vector().record(self.soma(0.5)._ref_ik_kahp_slower)
        # self.v9 = h.Vector().record(self.soma(0.5)._ref_ica_cal)

        # ---------------dend----------------
        for mechanism_d in ['Naf', 'nap', 'calc', 'cal', 'can', 'car', 'cat', 'kdrpr', 'IKs', 'kad', 'h', 'kca', 'ican',
                            'cadyn', 'pas']:
            self.dend.insert(mechanism_d)
            self.dend1.insert(mechanism_d)
            self.dend2.insert(mechanism_d)
            self.dend3.insert(mechanism_d)
            self.dend4.insert(mechanism_d)

            # print(mechanism_d)

        self.dend(0.5).Naf.gnafbar = 0.018 * 0.1
        self.dend(0.5).nap.gnapbar = 0.000018
        self.dend(0.5).calc.gcabar = 0.0001 * 0.1  #
        self.dend(0.5).cal.gcalbar = 0.0001 * 0.3  #
        self.dend(0.5).can.gcabar = 0.0002 * 0.3
        self.dend(0.5).car.gcabar = 0.000001 * 0.3 * 0.1 * 0.3  #
        self.dend(0.5).cat.gcatbar = 0.0002 * 0.3 * 0.1  #
        self.dend(0.5).kdrpr.gkdrbar = 0.018 * 0.09
        self.dend(0.5).IKs.gKsbar = 0.0012
        self.dend(0.5).kad.gkabar = 0.0007
        self.dend(0.5).kca.gbar = 0.005 * 5 * 0.001  #
        self.dend(0.5).h.gbar = 1.8e-5 * 0.5  #
        self.dend(0.5).ican.gbar = 0.001 * 0.07 * 0.1  #
        self.dend(0.5).pas.g = 0.01
        self.dend(0.5).pas.e = -65
        self.dend.Ra = 150

        self.dend1(0.5).Naf.gnafbar = 0.018 * 0.4
        self.dend1(0.5).nap.gnapbar = 0.000018  # * 3
        self.dend1(0.5).calc.gcabar = 0.0001 * 0.1  #
        self.dend1(0.5).cal.gcalbar = 0.0001 * 0.3  #
        self.dend1(0.5).can.gcabar = 0.0002 * 0.3
        self.dend1(0.5).car.gcabar = 0.000001 * 0.3 * 0.1 * 0.3  #
        self.dend1(0.5).cat.gcatbar = 0.0002 * 0.3 * 0.1  #
        self.dend1(0.5).kdrpr.gkdrbar = 0.018 * 0.09
        self.dend1(0.5).IKs.gKsbar = 0.0012
        self.dend1(0.5).kad.gkabar = 0.0007
        self.dend1(0.5).kca.gbar = 0.005 * 5 * 0.0001  #
        self.dend1(0.5).h.gbar = 1.8e-5 * 0.5  #
        self.dend1(0.5).ican.gbar = 0.001 * 0.07 * 0.1  #
        self.dend1(0.5).pas.g = 0.01
        self.dend1(0.5).pas.e = -65
        self.dend1.Ra = 150

        self.dend2(0.5).Naf.gnafbar = 0.018 * 0.1
        self.dend2(0.5).nap.gnapbar = 0.000018
        self.dend2(0.5).calc.gcabar = 0.0001 * 0.1  #
        self.dend2(0.5).cal.gcalbar = 0.0001 * 0.3  #
        self.dend2(0.5).can.gcabar = 0.0002 * 0.3
        self.dend2(0.5).car.gcabar = 0.000001 * 0.3 * 0.1 * 0.3  #
        self.dend2(0.5).cat.gcatbar = 0.0002 * 0.3 * 0.1  #
        self.dend2(0.5).kdrpr.gkdrbar = 0.018 * 0.09
        self.dend2(0.5).IKs.gKsbar = 0.0012
        self.dend2(0.5).kad.gkabar = 0.0007
        self.dend2(0.5).kca.gbar = 0.005 * 5 * 0.001  #
        self.dend2(0.5).h.gbar = 1.8e-5 * 0.5  #
        self.dend2(0.5).ican.gbar = 0.001 * 0.07 * 0.1  #
        self.dend2(0.5).pas.g = 0.01
        self.dend2(0.5).pas.e = -65
        self.dend2.Ra = 150

        self.dend3(0.5).Naf.gnafbar = 0.018 * 0.1
        self.dend3(0.5).nap.gnapbar = 0.000018
        self.dend3(0.5).calc.gcabar = 0.0001 * 0.1  #
        self.dend3(0.5).cal.gcalbar = 0.0001 * 0.3  #
        self.dend3(0.5).can.gcabar = 0.0002 * 0.3
        self.dend3(0.5).car.gcabar = 0.000001 * 0.3 * 0.1 * 0.3  #
        self.dend3(0.5).cat.gcatbar = 0.0002 * 0.3 * 0.1  #
        self.dend3(0.5).kdrpr.gkdrbar = 0.018 * 0.09
        self.dend3(0.5).IKs.gKsbar = 0.0012
        self.dend3(0.5).kad.gkabar = 0.0007
        self.dend3(0.5).kca.gbar = 0.005 * 5 * 0.001  #
        self.dend3(0.5).h.gbar = 1.8e-5 * 0.5  #
        self.dend3(0.5).ican.gbar = 0.001 * 0.07 * 0.1  #
        self.dend3(0.5).pas.g = 0.01
        self.dend3(0.5).pas.e = -65
        self.dend3.Ra = 150

        self.dend4(0.5).Naf.gnafbar = 0.018 * 0.1
        self.dend4(0.5).nap.gnapbar = 0.000018
        self.dend4(0.5).calc.gcabar = 0.0001 * 0.1  #
        self.dend4(0.5).cal.gcalbar = 0.0001 * 0.3  #
        self.dend4(0.5).can.gcabar = 0.0002 * 0.3
        self.dend4(0.5).car.gcabar = 0.000001 * 0.3 * 0.1 * 0.3  #
        self.dend4(0.5).cat.gcatbar = 0.0002 * 0.3 * 0.1  #
        self.dend4(0.5).kdrpr.gkdrbar = 0.018 * 0.09
        self.dend4(0.5).IKs.gKsbar = 0.0012
        self.dend4(0.5).kad.gkabar = 0.0007
        self.dend4(0.5).kca.gbar = 0.005 * 5 * 0.001  #
        self.dend4(0.5).h.gbar = 1.8e-5 * 0.5  #
        self.dend4(0.5).ican.gbar = 0.001 * 0.07 * 0.1  #
        self.dend4(0.5).pas.g = 0.01
        self.dend4(0.5).pas.e = -65
        self.dend4.Ra = 150

        # ---------------axon----------------
        for mechanism_a in ['Nafin', 'kdrin', 'pas']:
            self.axon.insert(mechanism_a)
            # print(mechanism_a)

        self.axon(0.5).Nafin.gnafbar = 0.4
        self.axon(0.5).kdrin.gkdrbar = 0.001
        self.axon(0.5).pas.g = 0.0002
        self.axon(0.5).pas.e = -73
        self.axon.Ra = 100
        self.axon.cm = 1.2

        for sec in self.all:
            sec.cm = 0.9
            sec.ena = 50.
            sec.ek = -95.

        self.k_vec = h.Vector().record(self.soma(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.soma(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.soma(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.soma(0.5)._ref_ki)
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_vext[0])
        self.cyt = rxd.Region(self.all, name='cyt', nrn_region='i', dx=1.0,
                              geometry=rxd.FractionalVolume(0.9, surface_fraction=1.0))
        self.na = rxd.Species([self.cyt], name='na', charge=1, d=1.0, initial=10)
        self.k = rxd.Species([self.cyt], name='k', charge=1, d=1.0, initial=148)
        self.k_i = self.k[self.cyt]
        self.ca = rxd.Species([self.cyt], d=0.08, name='ca', charge=2, initial=1.e-4, atolscale=1e-6)
        #------for test-----------
        #self.stim = h.IClamp(self.soma(0.5))
        #self.stim.delay = 50
        #self.stim.dur = 1
        #self.stim.amp = 1
        #print(self.id)


    #============Thalamus=============

class EpilepsySyppyrFRB(Cell):  #
    def __init__(self, x, y, z, num):
        super().__init__(x , y, z, num)
        self.id = 12
        self.Excitatory = 1
        self.name ='pyramidal fast rythmic bursting'
        #self.soma.nseg = 1+2*int(somaR*2/40)

        # ---------------soma----------------
        for mechanism_s in ['extracellular', 'naf2_cc', 'pas', 'napf_spinstell', 'kdr_fs_cc', 'kc_fast_cc', 'ka_cc',
                        'km_cc', 'k2_cc', 'kahp_slower', 'cal_cc', 'cat_cc', 'ar', 'cad_cc']:
            self.soma.insert(mechanism_s)
        # print(mechanism_s)

        self.soma(0.5).naf2_cc.gbar = 0.65
        self.soma(0.5).napf_spinstell.gbar = 0.0002
        self.soma(0.5).kdr_fs_cc.gbar = 0.1 * 10
        self.soma(0.5).kc_fast_cc.gbar = 0.001 * 10
        self.soma(0.5).ka_cc.gbar = 0.03
        self.soma(0.5).km_cc.gbar = 0.00375
        self.soma(0.5).k2_cc.gbar = 0.0001
        self.soma(0.5).kahp_slower.gbar = 0.0001
        self.soma(0.5).cal_cc.gbar = 0.0005
        self.soma(0.5).cat_cc.gbar = 0.0001
        self.soma(0.5).ar.gbar = 0.00025
        self.soma(0.5).cad_cc.beta = 0.02
        self.soma(0.5).cad_cc.phi = 260000.
        self.soma(0.5).pas.g = 0.001
        self.soma(0.5).pas.e = -65
        self.soma.Ra = 150.

        # ---------------dend----------------
        for mechanism_d in ['naf2_cc', 'napf_spinstell', 'pas', 'kdr_fs_cc', 'kc_fast_cc', 'ka_cc', 'km_cc', 'k2_cc',
                            'kahp_slower', 'cal_cc', 'cat_cc', 'ar', 'cad_cc']:
            self.dend.insert(mechanism_d)
            self.dend1.insert(mechanism_d)
            self.dend2.insert(mechanism_d)
            self.dend3.insert(mechanism_d)
            self.dend4.insert(mechanism_d)
            # print(mechanism_d)

        self.dend(0.5).naf2_cc.gbar = 0.0075
        self.dend(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend(0.5).kc_fast_cc.gbar = 0.01
        self.dend(0.5).ka_cc.gbar = 0.03
        self.dend(0.5).km_cc.gbar = 0.00375
        self.dend(0.5).k2_cc.gbar = 0.0001
        self.dend(0.5).kahp_slower.gbar = 0.0001
        self.dend(0.5).cal_cc.gbar = 0.0005
        self.dend(0.5).cat_cc.gbar = 0.0001
        self.dend(0.5).ar.gbar = 0.00025
        self.dend(0.5).cad_cc.beta = 0.05
        self.dend(0.5).cad_cc.phi = 260000.
        self.dend(0.5).pas.g = 0.02
        self.dend(0.5).pas.e = -65
        self.dend.Ra = 250.

        self.dend1(0.5).naf2_cc.gbar = 0.0075
        self.dend1(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend1(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend1(0.5).kc_fast_cc.gbar = 0.01
        self.dend1(0.5).ka_cc.gbar = 0.03
        self.dend1(0.5).km_cc.gbar = 0.00375
        self.dend1(0.5).k2_cc.gbar = 0.0001
        self.dend1(0.5).kahp_slower.gbar = 0.0001
        self.dend1(0.5).cal_cc.gbar = 0.0005
        self.dend1(0.5).cat_cc.gbar = 0.0001
        self.dend1(0.5).ar.gbar = 0.00025
        self.dend1(0.5).cad_cc.beta = 0.05
        self.dend1(0.5).cad_cc.phi = 260000.
        self.dend1(0.5).pas.g = 0.02
        self.dend1(0.5).pas.e = -65
        self.dend1.Ra = 250.

        self.dend2(0.5).naf2_cc.gbar = 0.0075
        self.dend2(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend2(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend2(0.5).kc_fast_cc.gbar = 0.01
        self.dend2(0.5).ka_cc.gbar = 0.03
        self.dend2(0.5).km_cc.gbar = 0.00375
        self.dend2(0.5).k2_cc.gbar = 0.0001
        self.dend2(0.5).kahp_slower.gbar = 0.0001
        self.dend2(0.5).cal_cc.gbar = 0.0005
        self.dend2(0.5).cat_cc.gbar = 0.0001
        self.dend2(0.5).ar.gbar = 0.00025
        self.dend2(0.5).cad_cc.beta = 0.05
        self.dend2(0.5).cad_cc.phi = 260000.
        self.dend2(0.5).pas.g = 0.02
        self.dend2(0.5).pas.e = -65
        self.dend2.Ra = 250.

        self.dend3(0.5).naf2_cc.gbar = 0.0075
        self.dend3(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend3(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend3(0.5).kc_fast_cc.gbar = 0.01
        self.dend3(0.5).ka_cc.gbar = 0.03
        self.dend3(0.5).km_cc.gbar = 0.00375
        self.dend3(0.5).k2_cc.gbar = 0.0001
        self.dend3(0.5).kahp_slower.gbar = 0.0001
        self.dend3(0.5).cal_cc.gbar = 0.0005
        self.dend3(0.5).cat_cc.gbar = 0.0001
        self.dend3(0.5).ar.gbar = 0.00025
        self.dend3(0.5).cad_cc.beta = 0.05
        self.dend3(0.5).cad_cc.phi = 260000.
        self.dend3(0.5).pas.g = 0.02
        self.dend3(0.5).pas.e = -65
        self.dend3.Ra = 250.

        self.dend4(0.5).naf2_cc.gbar = 0.0075
        self.dend4(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend4(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend4(0.5).kc_fast_cc.gbar = 0.01
        self.dend4(0.5).ka_cc.gbar = 0.03
        self.dend4(0.5).km_cc.gbar = 0.00375
        self.dend4(0.5).k2_cc.gbar = 0.0001
        self.dend4(0.5).kahp_slower.gbar = 0.0001
        self.dend4(0.5).cal_cc.gbar = 0.0005
        self.dend4(0.5).cat_cc.gbar = 0.0001
        self.dend4(0.5).ar.gbar = 0.00025
        self.dend4(0.5).cad_cc.beta = 0.05
        self.dend4(0.5).cad_cc.phi = 260000.
        self.dend4(0.5).pas.g = 0.02
        self.dend4(0.5).pas.e = -65
        self.dend4.Ra = 250.

        # self.vd1 = h.Vector().record(self.dend(0.5)._ref_ina_naf2)
        # self.vd2 = h.Vector().record(self.dend(0.5)._ref_ina_napf_spinstell)
        # self.vd3 = h.Vector().record(self.dend(0.5)._ref_ik_kdr_fs)
        # self.vd4 = h.Vector().record(self.dend(0.5)._ref_ik_ka)
        # self.vd5 = h.Vector().record(self.dend(0.5)._ref_ik_kc_fast)
        # self.vd7 = h.Vector().record(self.dend(0.5)._ref_ik_k2)
        # self.vd8 = h.Vector().record(self.dend(0.5)._ref_ik_kahp_slower)
        # self.vd9 = h.Vector().record(self.dend(0.5)._ref_ica_cal)

        # ---------------axon----------------
        for mechanism_a in ['naf2_cc', 'kdr_fs_cc', 'ka_cc', 'k2_cc', 'pas']:
            self.axon.insert(mechanism_a)
            # print(mechanism_a)

        self.axon(0.5).naf2_cc.gbar = 0.1 * 4
        self.axon(0.5).kdr_fs_cc.gbar = 0.9
        self.axon(0.5).ka_cc.gbar = 0.002
        self.axon(0.5).k2_cc.gbar = 0.1
        self.axon(0.5).pas.g = 0.01
        self.axon(0.5).pas.e = -65
        self.axon.Ra = 100.

        for sec in self.all:
            sec.cm = 0.9
            sec.ena = 50.
            sec.ek = -90

        self.k_vec = h.Vector().record(self.soma(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.soma(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.soma(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.soma(0.5)._ref_ki)
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_vext[0])
        self.cyt = rxd.Region(self.all, name='cyt', nrn_region='i', dx=1.0,
                              geometry=rxd.FractionalVolume(0.9, surface_fraction=1.0))
        self.na = rxd.Species([self.cyt], name='na', charge=1, d=1.0, initial=10)
        self.k = rxd.Species([self.cyt], name='k', charge=1, d=1.0, initial=148)
        self.k_i = self.k[self.cyt]
        self.ca = rxd.Species([self.cyt], d=0.08, name='ca', charge=2, initial=1.e-4, atolscale=1e-6)
        #------for test-----------
        #self.stim = h.IClamp(self.soma(0.5))
        #self.stim.delay = 50
        #self.stim.dur = 1
        #self.stim.amp = 1
        #print(self.id)



class EpilepsySyppyrRS(Cell):  #
    def __init__(self, x, y, z, num):
        super().__init__(x , y, z, num)
        self.id = 13
        self.Excitatory = 1
        self.name ='pyramidal regular spiking'
        #self.soma.nseg = 1+2*int(somaR*2/40)

        # ---------------soma----------------
        for mechanism_s in ['extracellular', 'naf2_cc', 'pas', 'napf_spinstell', 'kdr_fs_cc', 'kc_fast_cc', 'ka_cc',
                        'km_cc', 'k2_cc', 'kahp_slower', 'cal_cc', 'cat_cc', 'ar', 'cad_cc']:
            self.soma.insert(mechanism_s)
        # print(mechanism_s)

        self.soma(0.5).naf2_cc.gbar = 0.65
        self.soma(0.5).napf_spinstell.gbar = 0.0002
        self.soma(0.5).kdr_fs_cc.gbar = 0.1 * 10
        self.soma(0.5).kc_fast_cc.gbar = 0.001 * 10
        self.soma(0.5).ka_cc.gbar = 0.03
        self.soma(0.5).km_cc.gbar = 0.00375
        self.soma(0.5).k2_cc.gbar = 0.0001
        self.soma(0.5).kahp_slower.gbar = 0.0001
        self.soma(0.5).cal_cc.gbar = 0.0005
        self.soma(0.5).cat_cc.gbar = 0.0001
        self.soma(0.5).ar.gbar = 0.00025
        self.soma(0.5).cad_cc.beta = 0.02
        self.soma(0.5).cad_cc.phi = 260000.
        self.soma(0.5).pas.g = 0.001
        self.soma(0.5).pas.e = -65
        self.soma.Ra = 150.

        # ---------------dend----------------
        for mechanism_d in ['naf2_cc', 'napf_spinstell', 'pas', 'kdr_fs_cc', 'kc_fast_cc', 'ka_cc', 'km_cc', 'k2_cc',
                            'kahp_slower', 'cal_cc', 'cat_cc', 'ar', 'cad_cc']:
            self.dend.insert(mechanism_d)
            self.dend1.insert(mechanism_d)
            self.dend2.insert(mechanism_d)
            self.dend3.insert(mechanism_d)
            self.dend4.insert(mechanism_d)
            # print(mechanism_d)

        self.dend(0.5).naf2_cc.gbar = 0.0075
        self.dend(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend(0.5).kc_fast_cc.gbar = 0.01
        self.dend(0.5).ka_cc.gbar = 0.03
        self.dend(0.5).km_cc.gbar = 0.00375
        self.dend(0.5).k2_cc.gbar = 0.0001
        self.dend(0.5).kahp_slower.gbar = 0.0001
        self.dend(0.5).cal_cc.gbar = 0.0005
        self.dend(0.5).cat_cc.gbar = 0.0001
        self.dend(0.5).ar.gbar = 0.00025
        self.dend(0.5).cad_cc.beta = 0.05
        self.dend(0.5).cad_cc.phi = 260000.
        self.dend(0.5).pas.g = 0.02
        self.dend(0.5).pas.e = -65
        self.dend.Ra = 250.

        self.dend1(0.5).naf2_cc.gbar = 0.0075
        self.dend1(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend1(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend1(0.5).kc_fast_cc.gbar = 0.01
        self.dend1(0.5).ka_cc.gbar = 0.03
        self.dend1(0.5).km_cc.gbar = 0.00375
        self.dend1(0.5).k2_cc.gbar = 0.0001
        self.dend1(0.5).kahp_slower.gbar = 0.0001
        self.dend1(0.5).cal_cc.gbar = 0.0005
        self.dend1(0.5).cat_cc.gbar = 0.0001
        self.dend1(0.5).ar.gbar = 0.00025
        self.dend1(0.5).cad_cc.beta = 0.05
        self.dend1(0.5).cad_cc.phi = 260000.
        self.dend1(0.5).pas.g = 0.02
        self.dend1(0.5).pas.e = -65
        self.dend1.Ra = 250.

        self.dend2(0.5).naf2_cc.gbar = 0.0075
        self.dend2(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend2(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend2(0.5).kc_fast_cc.gbar = 0.01
        self.dend2(0.5).ka_cc.gbar = 0.03
        self.dend2(0.5).km_cc.gbar = 0.00375
        self.dend2(0.5).k2_cc.gbar = 0.0001
        self.dend2(0.5).kahp_slower.gbar = 0.0001
        self.dend2(0.5).cal_cc.gbar = 0.0005
        self.dend2(0.5).cat_cc.gbar = 0.0001
        self.dend2(0.5).ar.gbar = 0.00025
        self.dend2(0.5).cad_cc.beta = 0.05
        self.dend2(0.5).cad_cc.phi = 260000.
        self.dend2(0.5).pas.g = 0.02
        self.dend2(0.5).pas.e = -65
        self.dend2.Ra = 250.

        self.dend3(0.5).naf2_cc.gbar = 0.0075
        self.dend3(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend3(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend3(0.5).kc_fast_cc.gbar = 0.01
        self.dend3(0.5).ka_cc.gbar = 0.03
        self.dend3(0.5).km_cc.gbar = 0.00375
        self.dend3(0.5).k2_cc.gbar = 0.0001
        self.dend3(0.5).kahp_slower.gbar = 0.0001
        self.dend3(0.5).cal_cc.gbar = 0.0005
        self.dend3(0.5).cat_cc.gbar = 0.0001
        self.dend3(0.5).ar.gbar = 0.00025
        self.dend3(0.5).cad_cc.beta = 0.05
        self.dend3(0.5).cad_cc.phi = 260000.
        self.dend3(0.5).pas.g = 0.02
        self.dend3(0.5).pas.e = -65
        self.dend3.Ra = 250.

        self.dend4(0.5).naf2_cc.gbar = 0.0075
        self.dend4(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend4(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend4(0.5).kc_fast_cc.gbar = 0.01
        self.dend4(0.5).ka_cc.gbar = 0.03
        self.dend4(0.5).km_cc.gbar = 0.00375
        self.dend4(0.5).k2_cc.gbar = 0.0001
        self.dend4(0.5).kahp_slower.gbar = 0.0001
        self.dend4(0.5).cal_cc.gbar = 0.0005
        self.dend4(0.5).cat_cc.gbar = 0.0001
        self.dend4(0.5).ar.gbar = 0.00025
        self.dend4(0.5).cad_cc.beta = 0.05
        self.dend4(0.5).cad_cc.phi = 260000.
        self.dend4(0.5).pas.g = 0.02
        self.dend4(0.5).pas.e = -65
        self.dend4.Ra = 250.

        # self.vd1 = h.Vector().record(self.dend(0.5)._ref_ina_naf2)
        # self.vd2 = h.Vector().record(self.dend(0.5)._ref_ina_napf_spinstell)
        # self.vd3 = h.Vector().record(self.dend(0.5)._ref_ik_kdr_fs)
        # self.vd4 = h.Vector().record(self.dend(0.5)._ref_ik_ka)
        # self.vd5 = h.Vector().record(self.dend(0.5)._ref_ik_kc_fast)
        # self.vd7 = h.Vector().record(self.dend(0.5)._ref_ik_k2)
        # self.vd8 = h.Vector().record(self.dend(0.5)._ref_ik_kahp_slower)
        # self.vd9 = h.Vector().record(self.dend(0.5)._ref_ica_cal)

        # ---------------axon----------------
        for mechanism_a in ['naf2_cc', 'kdr_fs_cc', 'ka_cc', 'k2_cc', 'pas']:
            self.axon.insert(mechanism_a)
            # print(mechanism_a)

        self.axon(0.5).naf2_cc.gbar = 0.1 * 4
        self.axon(0.5).kdr_fs_cc.gbar = 0.9
        self.axon(0.5).ka_cc.gbar = 0.002
        self.axon(0.5).k2_cc.gbar = 0.1
        self.axon(0.5).pas.g = 0.01
        self.axon(0.5).pas.e = -65
        self.axon.Ra = 100.

        for sec in self.all:
            sec.cm = 0.9
            sec.ena = 50.
            sec.ek = -90


        self.k_vec = h.Vector().record(self.soma(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.soma(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.soma(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.soma(0.5)._ref_ki)
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_vext[0])
        self.cyt = rxd.Region(self.all, name='cyt', nrn_region='i', dx=1.0,
                              geometry=rxd.FractionalVolume(0.9, surface_fraction=1.0))
        self.na = rxd.Species([self.cyt], name='na', charge=1, d=1.0, initial=10)
        self.k = rxd.Species([self.cyt], name='k', charge=1, d=1.0, initial=148)
        self.k_i = self.k[self.cyt]
        self.ca = rxd.Species([self.cyt], d=0.08, name='ca', charge=2, initial=1.e-4, atolscale=1e-6)
        #------for test-----------
        #self.stim = h.IClamp(self.soma(0.5))
        #self.stim.delay = 50
        #self.stim.dur = 1
        #self.stim.amp = 1
        #print(self.id)


    #============Thalamus=============

class TCR(Cell):  #
    def __init__(self, x, y, z, num):
        super().__init__(x, y, z, num)
        self.id = 14
        self.Excitatory = 1
        self.name = 'thalamocortical relay'
        # self.soma.nseg = 1+2*int(somaR*2/40)

        # ---------------soma----------------
        for mechanism_s in ['extracellular', 'napf', 'pas', 'naf2_cc', 'kdr_fs_cc', 'kc', 'ka_cc', 'km_cc', 'k2_cc',
                            'kahp_slower', 'cal_cc', 'cat_a', 'ar', 'cad_cc']:
            self.soma.insert(mechanism_s)
            # print(mechanism_s)

        self.soma(0.5).naf2_cc.gbar = 0.6
        self.soma(0.5).napf.gbar = 0.00006
        self.soma(0.5).kdr_fs_cc.gbar = 0.5
        self.soma(0.5).ka_cc.gbar = 0.005
        self.soma(0.5).km_cc.gbar = 0.0005
        self.soma(0.5).kc.gbar = 0.01
        self.soma(0.5).k2_cc.gbar = 0.0005
        self.soma(0.5).kahp_slower.gbar = 0.0001
        self.soma(0.5).cal_cc.gbar = 0.0001
        self.soma(0.5).cat_a.gbar = 5.E-05
        self.soma(0.5).ar.gbar = 2.5E-05
        self.soma(0.5).cad_cc.beta = 0.02
        self.soma(0.5).cad_cc.phi = 10400.
        self.soma(0.5).pas.e = -70
        self.soma(0.5).pas.g = 0.001
        self.soma.Ra = 100.




        # ---------------dend----------------
        for mechanism_d in ['naf_tcr', 'napf_tcr', 'kdr_thlms','ka', 'kc', 'km', 'k2', 'kahp_slower', 'cal_thlms', 'cat_thlms', 'ar', 'cad',  'pas']:
            self.dend.insert(mechanism_d)
            self.dend1.insert(mechanism_d)
            self.dend2.insert(mechanism_d)
            self.dend3.insert(mechanism_d)
            self.dend4.insert(mechanism_d)

            # print(mechanism_d)

        # self.dend(0.5).naf2.gbar =   0.2
        self.dend(0.5).naf_tcr.gbar =   0.1
        self.dend(0.5).napf_tcr.gbar =   0.0002
        self.dend(0.5).kdr_thlms.gbar =   0.075
        self.dend(0.5).kc.gbar =   0.012
        self.dend(0.5).ka.gbar =   0.03
        self.dend(0.5).km.gbar =   0 #// 0.0005
        self.dend(0.5).k2.gbar =   0.002
        self.dend(0.5).cal_thlms.gbar =   0.0005
        self.dend(0.5).cat_thlms.gbar =   0.0005
        self.dend(0.5).ar.gbar =   0.00025
        self.dend(0.5).cad.beta  =   0.02
        self.dend(0.5).cad.phi =   52000.
        self.dend(0.5).pas.g = 1 / 100
        self.dend(0.5).pas.e = -70
        self.dend.Ra = 175

        self.dend1(0.5).naf_tcr.gbar = 0.1
        self.dend1(0.5).napf_tcr.gbar = 0.0002
        self.dend1(0.5).kdr_thlms.gbar = 0.075
        self.dend1(0.5).kc.gbar = 0.012
        self.dend1(0.5).ka.gbar = 0.03
        self.dend1(0.5).km.gbar = 0  # // 0.0005
        self.dend1(0.5).k2.gbar = 0.002
        self.dend1(0.5).cal_thlms.gbar = 0.0005
        self.dend1(0.5).cat_thlms.gbar = 0.0005
        self.dend1(0.5).ar.gbar = 0.00025
        self.dend1(0.5).cad.beta = 0.02
        self.dend1(0.5).cad.phi = 52000.
        self.dend1(0.5).pas.g = 1 / 100
        self.dend1(0.5).pas.e = -70
        self.dend1.Ra = 175

        self.dend2(0.5).naf_tcr.gbar = 0.1
        self.dend2(0.5).napf_tcr.gbar = 0.0002
        self.dend2(0.5).kdr_thlms.gbar = 0.075
        self.dend2(0.5).kc.gbar = 0.012
        self.dend2(0.5).ka.gbar = 0.03
        self.dend2(0.5).km.gbar = 0  # // 0.0005
        self.dend2(0.5).k2.gbar = 0.002
        self.dend2(0.5).cal_thlms.gbar = 0.0005
        self.dend2(0.5).cat_thlms.gbar = 0.0005
        self.dend2(0.5).ar.gbar = 0.00025
        self.dend2(0.5).cad.beta = 0.02
        self.dend2(0.5).cad.phi = 52000.
        self.dend2(0.5).pas.g = 1 / 100
        self.dend2(0.5).pas.e = -70
        self.dend2.Ra = 175

        self.dend3(0.5).naf_tcr.gbar = 0.1
        self.dend3(0.5).napf_tcr.gbar = 0.0002
        self.dend3(0.5).kdr_thlms.gbar = 0.075
        self.dend3(0.5).kc.gbar = 0.012
        self.dend3(0.5).ka.gbar = 0.03
        self.dend3(0.5).km.gbar = 0  # // 0.0005
        self.dend3(0.5).k2.gbar = 0.002
        self.dend3(0.5).cal_thlms.gbar = 0.0005
        self.dend3(0.5).cat_thlms.gbar = 0.0005
        self.dend3(0.5).ar.gbar = 0.00025
        self.dend3(0.5).cad.beta = 0.02
        self.dend3(0.5).cad.phi = 52000.
        self.dend3(0.5).pas.g = 1 / 100
        self.dend3(0.5).pas.e = -70
        self.dend3.Ra = 175

        self.dend4(0.5).naf_tcr.gbar = 0.1
        self.dend4(0.5).napf_tcr.gbar = 0.0002
        self.dend4(0.5).kdr_thlms.gbar = 0.075
        self.dend4(0.5).kc.gbar = 0.012
        self.dend4(0.5).ka.gbar = 0.03
        self.dend4(0.5).km.gbar = 0  # // 0.0005
        self.dend4(0.5).k2.gbar = 0.002
        self.dend4(0.5).cal_thlms.gbar = 0.0005
        self.dend4(0.5).cat_thlms.gbar = 0.0005
        self.dend4(0.5).ar.gbar = 0.00025
        self.dend4(0.5).cad.beta = 0.02
        self.dend4(0.5).cad.phi = 52000.
        self.dend4(0.5).pas.g = 1 / 100
        self.dend4(0.5).pas.e = -70
        self.dend4.Ra = 175


        # ---------------axon----------------
        for mechanism_a in ['Nafin', 'kdrin', 'pas']:
            self.axon.insert(mechanism_a)
            # print(mechanism_a)

        self.axon(0.5).Nafin.gnafbar = 0.4
        self.axon(0.5).kdrin.gkdrbar = 0.001
        self.axon(0.5).pas.g = 0.005
        self.axon(0.5).pas.e = -70
        self.axon.Ra = 100
        #self.axon.cm = 1.2

        for sec in self.all:
            sec.cm = 0.9
            sec.ena = 50.
            sec.ek = -95
            # sec.cm = 4.65
            # sec.Ra = 65.22
            # sec.pas.e = -85.15087381998698

        self.k_vec = h.Vector().record(self.soma(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.soma(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.soma(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.soma(0.5)._ref_ki)
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_vext[0])
        self.cyt = rxd.Region(self.all, name='cyt', nrn_region='i', dx=1.0,
                              geometry=rxd.FractionalVolume(0.9, surface_fraction=1.0))
        self.na = rxd.Species([self.cyt], name='na', charge=1, d=1.0, initial=10)
        self.k = rxd.Species([self.cyt], name='k', charge=1, d=1.0, initial=148)
        self.k_i = self.k[self.cyt]
        self.ca = rxd.Species([self.cyt], d=0.08, name='ca', charge=2, initial=1.e-4, atolscale=1e-6)





class nRT(Cell):  #
    def __init__(self, x, y, z, num):
        super().__init__(x, y, z, num)
        self.id = 15
        self.Excitatory = -1
        self.name = 'nucleus reticularis'
        # self.soma.nseg = 1+2*int(somaR*2/40)

        # ---------------soma----------------
        for mechanism_s in ['extracellular', 'naf2', 'kdr_fs', 'ka', 'k2',
                            'pas']:
            self.soma.insert(mechanism_s)

        self.soma(0.5).naf2.gbar = 0.4
        self.soma(0.5).kdr_fs.gbar = 0.4
        self.soma(0.5).ka.gbar = 0.001
        self.soma(0.5).k2.gbar = 0.0005

        self.soma(0.5).pas.g = 3.78787879E-05
        self.soma(0.5).pas.e = -75
        self.soma.Ra = 250
        #self.soma(0.5).nap.gnapbar = 0.000018



        # ---------------dend----------------
        for mechanism_d in ['naf_tcr', 'naf2', 'napf', 'kdr_fs', 'ka', 'kc', 'km', 'k2', 'kahp_slower', 'cal_thlms', 'cat_a', 'ar', 'cad',  'pas']:
            self.dend.insert(mechanism_d)
            self.dend1.insert(mechanism_d)
            self.dend2.insert(mechanism_d)
            self.dend3.insert(mechanism_d)
            self.dend4.insert(mechanism_d)

            # print(mechanism_d)

        # self.dend(0.5).naf2.gbar =   0.2
        self.dend(0.5).naf2.gbar =   0.06
        self.dend(0.5).napf.gbar =   0.0006
        self.dend(0.5).kdr_fs.gbar =   0.06
        self.dend(0.5).kc.gbar =   0.01
        self.dend(0.5).ka.gbar =   0.005
        self.dend(0.5).km.gbar =    0.0005
        self.dend(0.5).k2.gbar =   0.0005
        self.dend(0.5).kahp_slower.gbar = 0.0001
        self.dend(0.5).cal_thlms.gbar =   0.0005
        self.dend(0.5).cat_a.gbar =   5.E-05
        self.dend(0.5).ar.gbar =   2.5E-05
        self.dend(0.5).cad.beta  =   0.02
        self.dend(0.5).cad.phi =   10400.
        self.dend(0.5).pas.g = 1 / 100
        self.dend(0.5).pas.e = -75
        self.dend.Ra = 250

        self.dend1(0.5).naf2.gbar = 0.06
        self.dend1(0.5).napf.gbar = 0.0006
        self.dend1(0.5).kdr_fs.gbar = 0.06
        self.dend1(0.5).kc.gbar = 0.01
        self.dend1(0.5).ka.gbar = 0.005
        self.dend1(0.5).km.gbar = 0.0005
        self.dend1(0.5).k2.gbar = 0.0005
        self.dend1(0.5).kahp_slower.gbar = 0.0001
        self.dend1(0.5).cal_thlms.gbar = 0.0005
        self.dend1(0.5).cat_a.gbar = 5.E-05
        self.dend1(0.5).ar.gbar = 2.5E-05
        self.dend1(0.5).cad.beta = 0.02
        self.dend1(0.5).cad.phi = 10400.
        self.dend1(0.5).pas.g = 1 / 100
        self.dend1(0.5).pas.e = -75
        self.dend1.Ra = 250

        self.dend2(0.5).naf2.gbar = 0.06
        self.dend2(0.5).napf.gbar = 0.0006
        self.dend2(0.5).kdr_fs.gbar = 0.06
        self.dend2(0.5).kc.gbar = 0.01
        self.dend2(0.5).ka.gbar = 0.005
        self.dend2(0.5).km.gbar = 0.0005
        self.dend2(0.5).k2.gbar = 0.0005
        self.dend2(0.5).kahp_slower.gbar = 0.0001
        self.dend2(0.5).cal_thlms.gbar = 0.0005
        self.dend2(0.5).cat_a.gbar = 5.E-05
        self.dend2(0.5).ar.gbar = 2.5E-05
        self.dend2(0.5).cad.beta = 0.02
        self.dend2(0.5).cad.phi = 10400.
        self.dend2(0.5).pas.g = 1 / 100
        self.dend2(0.5).pas.e = -75
        self.dend2.Ra = 250

        self.dend3(0.5).naf2.gbar = 0.06
        self.dend3(0.5).napf.gbar = 0.0006
        self.dend3(0.5).kdr_fs.gbar = 0.06
        self.dend3(0.5).kc.gbar = 0.01
        self.dend3(0.5).ka.gbar = 0.005
        self.dend3(0.5).km.gbar = 0.0005
        self.dend3(0.5).k2.gbar = 0.0005
        self.dend3(0.5).kahp_slower.gbar = 0.0001
        self.dend3(0.5).cal_thlms.gbar = 0.0005
        self.dend3(0.5).cat_a.gbar = 5.E-05
        self.dend3(0.5).ar.gbar = 2.5E-05
        self.dend3(0.5).cad.beta = 0.02
        self.dend3(0.5).cad.phi = 10400.
        self.dend3(0.5).pas.g = 1 / 100
        self.dend3(0.5).pas.e = -75
        self.dend3.Ra = 250

        self.dend4(0.5).naf2.gbar = 0.06
        self.dend4(0.5).napf.gbar = 0.0006
        self.dend4(0.5).kdr_fs.gbar = 0.06
        self.dend4(0.5).kc.gbar = 0.01
        self.dend4(0.5).ka.gbar = 0.005
        self.dend4(0.5).km.gbar = 0.0005
        self.dend4(0.5).k2.gbar = 0.0005
        self.dend4(0.5).kahp_slower.gbar = 0.0001
        self.dend4(0.5).cal_thlms.gbar = 0.0005
        self.dend4(0.5).cat_a.gbar = 5.E-05
        self.dend4(0.5).ar.gbar = 2.5E-05
        self.dend4(0.5).cad.beta = 0.02
        self.dend4(0.5).cad.phi = 10400.
        self.dend4(0.5).pas.g = 1 / 100
        self.dend4(0.5).pas.e = -75
        self.dend4.Ra = 250




        # ---------------axon----------------
        for mechanism_a in ['Nafin', 'kdrin', 'pas']:
            self.axon.insert(mechanism_a)
            # print(mechanism_a)

        self.axon(0.5).Nafin.gnafbar = 0.4
        self.axon(0.5).kdrin.gkdrbar = 0.001
        self.axon(0.5).pas.g = 0.0002
        self.axon(0.5).pas.e = -70
        self.axon.Ra = 100
        self.axon.cm = 1.2

        for sec in self.all:
            sec.cm = 0.9
            sec.ena = 50.
            sec.ek = -95
            # sec.cm = 4.65
            # sec.Ra = 65.22
            # sec.pas.e = -85.15087381998698

        self.k_vec = h.Vector().record(self.soma(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.soma(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.soma(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.soma(0.5)._ref_ki)
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_vext[0])
        self.cyt = rxd.Region(self.all, name='cyt', nrn_region='i', dx=1.0,
                              geometry=rxd.FractionalVolume(0.9, surface_fraction=1.0))
        self.na = rxd.Species([self.cyt], name='na', charge=1, d=1.0, initial=10)
        self.k = rxd.Species([self.cyt], name='k', charge=1, d=1.0, initial=148)
        self.k_i = self.k[self.cyt]
        self.ca = rxd.Species([self.cyt], d=0.08, name='ca', charge=2, initial=1.e-4, atolscale=1e-6)
