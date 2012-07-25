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

KstatObj = kstat.Kstat()

def get_ether_info (cmd):
    '''
    Function is used to collect network interface information, specifically
    names with id numbers of all interfaces on the machine. We have to selectively
    build by passing different driver names and instance numbers to the Kstat object.
    '''
    stdout,stderr = None,None
    from subprocess import Popen, PIPE
    try:
        process = Popen(cmd, stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()

        ## We expect to return a list with minimum of one element
        ## describing all network interfaces available on the machine.
        if not stdout == None: return stdout.split()
        else: return None

    except OSError as ose:
        print ose, stderr

phys_link_names = get_ether_info(['/usr/sbin/dladm', 'show-phys', '-p', '-o','Link'])

class NetstatsPlugin(PorkchopPlugin):
    refresh = 3

    def get_data(self):

        def normalize_attrib_names(linkid):
            '''
            We are using this function to normalize the names of the key names, removing spaces
            underscores and such.
            '''
            for key in kstat_nics_dict[linkid].keys():
                if key == ' ' or key == '':
                    kstat_nics_dict[linkid].pop(key)

                res = { '{0}'.format(k.replace(' ','').replace('-','_')):v
                        for k,v in kstat_nics_dict[linkid].iteritems() }
                res = { k.lower():v for k,v in res.iteritems() }

            return res

        data = self.gendict()
        kstat_nics_dict = {}
        final_kstat_nics_dict = {}

        if phys_link_names:
            for key in phys_link_names:
        #    print type(key),type(key[-1:])
                kstat_nics_dict[key] = KstatObj[key[:-1],int(key[-1:]),'statistics']
            #    print kstat_nics_dict

        ## Final dictionary should look something like this:
        ## {'interface name' : {interface data}, 'interface name' : {interface data} }

        for linkn in phys_link_names:
            final_kstat_nics_dict[linkn] = normalize_attrib_names(linkn)

        data.update(final_kstat_nics_dict)

        return data
#
    def format_data(self, data):

        prev = self.prev_data
        result = {}

        for linkn in phys_link_names:
            result[linkn] = {}
            result[linkn]['raw'] = {}
            result[linkn]['calculated'] = {}
            for key in prev[linkn].keys():
                result[linkn]['raw'][key] = data[linkn][key] - prev[linkn][key]

#        result['calculated'].update(data['calculated'])
#        print data['demand']
#        print data['prefetch']
#        for key in prev['demand'].keys():
#            result['demand'][key] = data['demand'][key] - prev['demand'][key]
#
#        for key in prev['prefetch'].keys():
#            result['prefetch'][key] = data['prefetch'][key] - prev['prefetch'][key]

#        result['prefetch'].update(data['prefetch'])
        ## Calculate change of ARC size

        return result
