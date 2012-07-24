__author__ = 'szaydel'

import sys
sys.path.append('/racktop/rt-porkchop-plugins/kstat')

import kstat
from porkchop.plugin import PorkchopPlugin

#class Kobj():
#    def __init__(self,current,previous,delta):
#        self.current = current
#        self.previous = previous
#        self.delta = delta
#    pass

k = kstat.Kstat()

class KstatArcPDObj(object):

    def __init__(self,dd):
        self.demand_metadata_hits = dd['demand_metadata_hits']
        self.demand_metadata_misses = dd['demand_metadata_misses']
        self.prefetch_metadata_hits = dd['prefetch_metadata_hits']
        self.prefetch_metadata_misses = dd['prefetch_metadata_misses']

        self.demand_data_hits = dd['demand_data_hits']
        self.demand_data_misses = dd['demand_data_misses']
        self.prefetch_data_hits = dd['prefetch_data_hits']
        self.prefetch_data_misses = dd['prefetch_data_misses']

        self.prefetch_data_reads = self.prefetch_data_hits + self.prefetch_data_misses
        self.demand_data_reads = self.demand_data_hits + self.demand_data_misses

        self.demand_hits = self.demand_data_hits + self.demand_metadata_hits
        self.demand_misses = self.demand_data_misses + self.demand_metadata_misses
        self.prefetch_hits = self.prefetch_data_hits + self.prefetch_metadata_hits
        self.prefetch_misses = self.prefetch_data_misses + self.prefetch_metadata_misses
        self.demand_reads = self.demand_hits + self.demand_misses
        self.prefetch_reads = self.prefetch_hits + self.prefetch_misses
        self.demand_metadata_reads = self.demand_metadata_hits + self.demand_metadata_misses
        self.prefetch_metadata_reads = self.prefetch_metadata_hits + self.prefetch_metadata_misses
        self.total_reads = self.demand_reads + self.prefetch_reads
        self.demand_hit_percentage()
        self.demand_miss_percentage()
        self.prefetch_hit_percentage()
        self.prefetch_miss_percentage()
        self.demand_metadata_miss_percentage()
        self.demand_metadata_hit_percentage()
        self.demand_data_miss_percentage()
        self.demand_data_hit_percentage()
        self.prefetch_metadata_miss_percentage()
        self.prefetch_metadata_hit_percentage()
        self.prefetch_data_miss_percentage()
        self.prefetch_data_hit_percentage()

    def demand_to_prefetch_hit_percentage(self):
        #self.demand_reads = self.demand_hits + self.demand_misses
        if self.demand_reads > 0:
            return round(100 * float(self.demand_hits)
            / (float(self.demand_hits) +
               float(self.prefetch_hits)), 3)
        else:
            return None

    def demand_hit_percentage(self):
        #self.demand_reads = self.demand_hits + self.demand_misses
        if self.demand_reads > 0:
            return round(100 * float(self.demand_hits)
                                / float(self.demand_reads), 3)
        else:
            return None

    def demand_miss_percentage(self):
        #self.demand_reads = self.demand_hits + self.demand_misses
        if self.demand_reads > 0:
            return round(100 * float(self.demand_misses)
                                / float(self.demand_reads), 3)
        else:
            return None

    def prefetch_hit_percentage(self):
#        self.prefetch_reads = self.prefetch_hits + self.prefetch_misses
        if self.prefetch_reads > 0:
            return round(100 * float(self.prefetch_hits)
                          / float(self.prefetch_reads), 3)
        else:
            return None

    def prefetch_miss_percentage(self):
    #        self.prefetch_reads = self.prefetch_hits + self.prefetch_misses
        if self.prefetch_reads > 0:
            return round(100 * float(self.prefetch_misses)
            / float(self.prefetch_reads), 3)
        else:
            return None

    def demand_metadata_miss_percentage(self):
    #        self.prefetch_reads = self.prefetch_hits + self.prefetch_misses
        if self.demand_metadata_hits > 0:
            return round(100 * float(self.demand_metadata_misses)
            / float(self.demand_metadata_reads), 3)
        else:
            return None

    def demand_metadata_hit_percentage(self):
    #        self.prefetch_reads = self.prefetch_hits + self.prefetch_misses
        if self.demand_metadata_hits > 0:
            return round(100 * float(self.demand_metadata_hits)
            / float(self.demand_metadata_reads), 3)
        else:
            return None

    def demand_data_miss_percentage(self):
    #        self.prefetch_reads = self.prefetch_hits + self.prefetch_misses
        if self.demand_data_hits > 0:
            return round(100 * float(self.demand_data_misses)
            / float(self.demand_data_reads), 3)
        else:
            return None

    def demand_data_hit_percentage(self):
    #        self.prefetch_reads = self.prefetch_hits + self.prefetch_misses
        if self.demand_data_hits > 0:
            return round(100 * float(self.demand_data_hits)
            / float(self.demand_data_reads), 3)
        else:
            return None

    def prefetch_metadata_miss_percentage(self):
    #        self.prefetch_reads = self.prefetch_hits + self.prefetch_misses
        if self.prefetch_metadata_hits > 0:
            return round(100 * float(self.prefetch_metadata_misses)
            / float(self.prefetch_metadata_reads), 3)
        else:
            return None

    def prefetch_metadata_hit_percentage(self):
    #        self.prefetch_reads = self.prefetch_hits + self.prefetch_misses
        if self.prefetch_metadata_hits > 0:
            return round(100 * float(self.prefetch_metadata_hits)
            / float(self.prefetch_metadata_reads), 3)
        else:
            return None

    def prefetch_data_miss_percentage(self):
    #        self.prefetch_reads = self.prefetch_hits + self.prefetch_misses
        if self.prefetch_data_hits > 0:
            return round(100 * float(self.prefetch_data_misses)
            / float(self.prefetch_data_reads), 3)
        else:
            return None

    def prefetch_data_hit_percentage(self):
    #        self.prefetch_reads = self.prefetch_hits + self.prefetch_misses
        if self.prefetch_data_hits > 0:
            return round(100 * float(self.prefetch_data_hits)
            / float(self.prefetch_data_reads), 3)
        else:
            return None

#a = KstatArcObj(10,5,100,5)
#print a
#print a.demand_hit_percentage()
#print a.prefetch_hit_percentage()

class ArcstatsPlugin(PorkchopPlugin):
    refresh = 3

    def get_data(self):

        data = self.gendict()
        raw_data = k['zfs',0,'arcstats']

        raw_demand_and_prefetch_data ={}
        raw_demand_data = {}
        raw_prefetch_data = {}
#        demand_hits = (raw_data['demand_metadata_hits'] + raw_data['demand_data_hits'])
#        demand_misses = (raw_data['demand_metadata_misses'] + raw_data['demand_data_misses'])

        for key in raw_data.keys():
            if key.endswith('pre',0,3):
                raw_prefetch_data[key] = raw_data[key]
            elif key.endswith('dem',0,3):
                raw_demand_data[key] = raw_data[key]

        raw_demand_and_prefetch_data.update(raw_demand_data)
        raw_demand_and_prefetch_data.update(raw_prefetch_data)
        calc_prefetch_demand = KstatArcPDObj(raw_demand_and_prefetch_data)

#        print 'Demand Data Hit Pct: ',calc_prefetch_demand.demand_data_hit_percentage

        calculated_data = {

        'prefetch_hits' : calc_prefetch_demand.prefetch_hits,
        'prefetch_misses' : calc_prefetch_demand.prefetch_misses,
        'demand_hits' : calc_prefetch_demand.demand_hits,
        'demand_misses' : calc_prefetch_demand.demand_misses,
        '_%_pct': {
        'demand_hits_to_total_hits' : calc_prefetch_demand.demand_to_prefetch_hit_percentage(),
        'demand_hits' : calc_prefetch_demand.demand_hit_percentage(),
        'prefetch_hits' : calc_prefetch_demand.prefetch_hit_percentage(),
        'demand_misses' : calc_prefetch_demand.demand_miss_percentage(),
        'prefetch_misses' : calc_prefetch_demand.prefetch_miss_percentage(),
        'demand_metadata_misses' : calc_prefetch_demand.demand_metadata_miss_percentage(),
        'demand_metadata_hits' : calc_prefetch_demand.demand_metadata_hit_percentage(),
        'demand_data_misses' : calc_prefetch_demand.demand_data_miss_percentage(),
        'demand_data_hits' : calc_prefetch_demand.demand_data_hit_percentage(),
        'efficiency' : "%.1f" % (100 - (float(raw_data['misses']) /
                                               float( raw_data['hits'] + raw_data['misses'] ) * 100 )),
        'most_recently_used' : "%.1f" % (100 - (float(raw_data['mru_hits']) /
                                              (float(raw_data['mfu_hits']) + float(raw_data['mru_hits'])) * 100)),
        'most_frequently_used' : "%.1f" % (100 - (float(raw_data['mfu_hits']) /
                                              (float(raw_data['mfu_hits']) + float(raw_data['mru_hits'])) * 100)),
                        } ,
        'demand_reads' : calc_prefetch_demand.demand_reads,
        'prefetch_reads' : calc_prefetch_demand.prefetch_reads,
        'total_reads' : calc_prefetch_demand.total_reads,               ## Number of attempted reads from arc
        'total_hits' : raw_data['mru_hits'] + raw_data['mfu_hits'],  ## Number of successful reads from arc
        'total_misses' : calc_prefetch_demand.total_reads -
                          (raw_data['mru_hits'] +
                           raw_data['mfu_hits']),  ## Number of unsuccessful reads from arc
        }

        data['raw'] = raw_data
        data['calculated'] = calculated_data
        data['prefetch'] = raw_prefetch_data
        data['demand'] = raw_demand_data
        return data

    def format_data(self, data):
        result = {
            'calculated':{},
            'raw':{},
            'demand':{},
            'prefetch':{},
                }

        prev = self.prev_data
        for key in prev['raw'].keys():
            result['raw'][key] = data['raw'][key] - prev['raw'][key]
        result['calculated'].update(data['calculated'])
#        print data['demand']
#        print data['prefetch']
        for key in prev['demand'].keys():
            result['demand'][key] = data['demand'][key] - prev['demand'][key]

        for key in prev['prefetch'].keys():
            result['prefetch'][key] = data['prefetch'][key] - prev['prefetch'][key]

#        result['prefetch'].update(data['prefetch'])
        ## Calculate change of ARC size

        return result
