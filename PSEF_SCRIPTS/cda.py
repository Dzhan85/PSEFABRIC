    ######################################
    #                                    #
    #                 2.                 #
    #             cda layer              #
    #                                    #
    ######################################

'''
- psefabric configuration dictionary correction:
    - dict_correct()
    - default_change()
- creating "full" psefabric configuration dictionary
    - psef_full()
        - address_full()
        - service_full()
        - application_full()
- creating a dict with a difference between full new and old psefabric configuration dictionaries
    - ddiff_dict()
- policy indexation
    psef_index.policy_index()
'''

import re
import copy
from deepdiff import DeepDiff


def dict_correct(psef_conf_):

##########  Description  #######
    '''
    In case when we expect a list of child elements in xml file (new or old psefabric configuration) but we have only one element, xmltodict interprets this element as a single
    variable (not a list).
    So we want to change the type of such variables to the list type.
    '''
#############  BODY ############

    if 'addresses' in psef_conf_['data']:
        if not isinstance (psef_conf_['data']['addresses'],list):
            address_element = psef_conf_['data']['addresses']
            psef_conf_['data']['addresses'] = []
            psef_conf_['data']['addresses'].append(address_element)
    if 'address-sets' in psef_conf_['data']:
        if not isinstance (psef_conf_['data']['address-sets'],list):
            address_set_element = psef_conf_['data']['address-sets']
            psef_conf_['data']['address-sets'] = []
            psef_conf_['data']['address-sets'].append(address_set_element)
        for n, address_set_el in enumerate(psef_conf_['data']['address-sets']):
            if not isinstance (address_set_el['addresses'],list):
                address_el_list = address_set_el['addresses']
                psef_conf_['data']['address-sets'][n]['addresses'] = []
                psef_conf_['data']['address-sets'][n]['addresses'].append(address_el_list)
    if 'services' in psef_conf_['data']:
        if not isinstance (psef_conf_['data']['services'],list):
            service_element = psef_conf_['data']['services']
            psef_conf_['data']['services'] = []
            psef_conf_['data']['services'].append(service_element)
    if 'service-sets' in psef_conf_['data']:
        if not isinstance (psef_conf_['data']['service-sets'],list):
            service_set_element = psef_conf_['data']['service-sets']
            psef_conf_['data']['service-sets'] = []
            psef_conf_['data']['service-sets'].append(service_set_element)
        for i, services_set_el in enumerate(psef_conf_['data']['service-sets']):
            if not isinstance (services_set_el['services'],list):
                service_el_list = services_set_el['services']
                psef_conf_['data']['service-sets'][i]['services'] = []
                psef_conf_['data']['service-sets'][i]['services'].append(service_el_list)
    if 'applications' in psef_conf_['data']:
        if not isinstance (psef_conf_['data']['applications'],list):
            application_element = psef_conf_['data']['applications']
            psef_conf_['data']['applications'] = []
            psef_conf_['data']['applications'].append(application_element)
    if 'application-sets' in psef_conf_['data']:
        if not isinstance (psef_conf_['data']['application-sets'],list):
            application_set_element = psef_conf_['data']['application-sets']
            psef_conf_['data']['application-sets'] = []
            psef_conf_['data']['application-sets'].append(application_set_element)
        for i, applications_set_el in enumerate(psef_conf_['data']['application-sets']):
            if not isinstance (applications_set_el['applications'],list):
                application_el_list = applications_set_el['applications']
                psef_conf_['data']['application-sets'][i]['applications'] = []
                psef_conf_['data']['application-sets'][i]['applications'].append(application_el_list)

    if ('policies' in psef_conf_['data']):
        if not isinstance (psef_conf_['data']['policies'],list):
            policy_element = psef_conf_['data']['policies']
            psef_conf_['data']['policies'] = []
            psef_conf_['data']['policies'].append(policy_element)
        for policy_element_ in psef_conf_['data']['policies']:
            if 'source-address-sets' in policy_element_['match']:
                if not isinstance (policy_element_['match']['source-address-sets'],list):
                    source_addresses_set_element_ = policy_element_['match']['source-address-sets']
		    policy_element_['match']['source-address-sets']=[]
                    policy_element_['match']['source-address-sets'].append(source_addresses_set_element_)
            if 'destination-address-sets' in policy_element_['match']:
                if not isinstance (policy_element_['match']['destination-address-sets'],list):
                    destination_addresses_set_element_ = policy_element_['match']['destination-address-sets']
                    policy_element_['match']['destination-address-sets']=[]
                    policy_element_['match']['destination-address-sets'].append(destination_addresses_set_element_)
            if 'service-sets' in policy_element_['match']:
                if not isinstance (policy_element_['match']['service-sets'],list):
                    service_set_element_ = policy_element_['match']['service-sets']
                    policy_element_['match']['service-sets'] = []
                    policy_element_['match']['service-sets'].append(service_set_element_)
            if 'application-sets' in policy_element_['match']:
                if not isinstance (policy_element_['match']['application-sets'],list):
                    application_set_element_ = policy_element_['match']['application-sets']
                    policy_element_['match']['application-sets'] = []
                    policy_element_['match']['application-sets'].append(application_set_element_)

    return psef_conf_


def ddiff_dict(ddiff_):

##########  Description  #######
    '''
 takes the difference between new and old full psefabric configurations (type dict) and transforms it to the dict convenient for further operations
   '''
#############  BODY ############

    diff_dict_ = {}
    regex_addr = "\['data'\]\['addresses'\]"
    regex_svc = "\['data'\]\['services'\]"
    regex_app = "\['data'\]\['applications'\]"
    regex_addr_set = "\['data'\]\['address-sets'\]"
    regex_svc_set = "\['data'\]\['service-sets'\]"
    regex_app_set = "\['data'\]\['application-sets'\]"
    regex_policies = "\['data'\]\['policies'\]"

    addresses_rm = []
    address_sets_rm = []
    addresses_ad = []
    address_sets_ad = []
    services_rm = []
    service_sets_rm = []
    services_ad = []
    service_sets_ad = []

    applications_rm = []
    application_sets_rm = []
    applications_ad = []
    application_sets_ad = []

    policies_rm = []
    policies_ad = []

    for key in ddiff_:
        if (re.search(r'item_removed', key)):
            for key_rm in ddiff_[key]:
                if (re.search(regex_addr, key_rm)):
                    if not isinstance (ddiff_[key][key_rm],list):
                        addresses_rm.append(ddiff_[key][key_rm])
                    else:
                        addresses_rm = ddiff_[key][key_rm]
                if (re.search(regex_addr_set, key_rm)):
                    if not isinstance (ddiff_[key][key_rm],list):
                        address_sets_rm.append(ddiff_[key][key_rm])
                    else:
                        address_sets_rm = ddiff_[key][key_rm]

                if (re.search(regex_svc, key_rm)):
                    if not isinstance (ddiff_[key][key_rm],list):
                        services_rm.append(ddiff_[key][key_rm])
                    else:
                        services_rm = ddiff_[key][key_rm]
                if (re.search(regex_svc_set, key_rm)):
                    if not isinstance (ddiff_[key][key_rm],list):
                        service_sets_rm.append(ddiff_[key][key_rm])
                    else:
                        service_sets_rm = ddiff_[key][key_rm]

                if (re.search(regex_app, key_rm)):
                    if not isinstance (ddiff_[key][key_rm],list):
                        applications_rm.append(ddiff_[key][key_rm])
                    else:
                        applications_rm = ddiff_[key][key_rm]
                if (re.search(regex_app_set, key_rm)):
                    if not isinstance (ddiff_[key][key_rm],list):
                        application_sets_rm.append(ddiff_[key][key_rm])
                    else:
                        application_sets_rm = ddiff_[key][key_rm]
                
                if (re.search(regex_policies, key_rm)):
                    if not isinstance (ddiff_[key][key_rm],list):
                        policies_rm.append(ddiff_[key][key_rm])
                    else:
                        policies_rm = ddiff_[key][key_rm]

        if (re.search(r'item_added', key)):
            for key_ad in ddiff_[key]:
                if (re.search(regex_addr, key_ad)):
                    if not isinstance (ddiff_[key][key_ad],list):
                        addresses_ad.append(ddiff_[key][key_ad])
                    else: 
                        addresses_ad = ddiff_[key][key_ad]
                if (re.search(regex_addr_set, key_ad)):
                    if not isinstance (ddiff_[key][key_ad],list):
                        address_sets_ad.append(ddiff_[key][key_ad])
                    else:
                        address_sets_ad = ddiff_[key][key_ad]

                if (re.search(regex_svc, key_ad)):
                    if not isinstance (ddiff_[key][key_ad],list):
                        services_ad.append(ddiff_[key][key_ad])
                    else:
                        services_ad = ddiff_[key][key_ad]
                if (re.search(regex_svc_set, key_ad)):
                    if not isinstance (ddiff_[key][key_ad],list):
                        service_sets_ad.append(ddiff_[key][key_ad])
                    else:
                        service_sets_ad = ddiff_[key][key_ad]

                if (re.search(regex_app, key_ad)):
                    if not isinstance (ddiff_[key][key_ad],list):
                        applications_ad.append(ddiff_[key][key_ad])
                    else:
                        applications_ad = ddiff_[key][key_ad]
                if (re.search(regex_app_set, key_ad)):
                    if not isinstance (ddiff_[key][key_ad],list):
                        application_sets_ad.append(ddiff_[key][key_ad])
                    else:
                        application_sets_ad = ddiff_[key][key_ad]

                if (re.search(regex_policies, key_ad)):
                    if not isinstance (ddiff_[key][key_ad],list):
                        policies_ad.append(ddiff_[key][key_ad])
                    else:
                        policies_ad = ddiff_[key][key_ad]
 
    diff_dict_['addresses_ad'] = addresses_ad
    diff_dict_['address_sets_ad'] = address_sets_ad
    diff_dict_['services_ad'] = services_ad
    diff_dict_['service_sets_ad'] = service_sets_ad
    diff_dict_['applications_ad'] = applications_ad
    diff_dict_['application_sets_ad'] = application_sets_ad
    diff_dict_['policies_ad'] = policies_ad
    diff_dict_['addresses_rm'] = addresses_rm
    diff_dict_['address_sets_rm'] = address_sets_rm
    diff_dict_['services_rm'] = services_rm
    diff_dict_['service_sets_rm'] = service_sets_rm
    diff_dict_['applications_rm'] = applications_rm
    diff_dict_['application_sets_rm'] = application_sets_rm
    diff_dict_['policies_rm'] = policies_rm

    diff_dictt_ = diff_dict_
    
    return (diff_dictt_)


def psef_full (psef_conf, address_set_full, service_set_full, application_set_full, address_full, service_full, application_full):

    '''
    creats "full" psefabric configuration dictionary
    '''
    
    psef_conf_ = copy.deepcopy(psef_conf)
    address_set_full_ = copy.deepcopy(address_set_full)
    service_set_full_ = copy.deepcopy(service_set_full)
    application_set_full_= copy.deepcopy(application_set_full)
    address_full_ = copy.deepcopy(address_full)
    service_full_ = copy.deepcopy(service_full)
    application_full_ = copy.deepcopy(application_full)

    # full policies
    if ('policies' in psef_conf_['data']):
        j = 0

        for policy_ in psef_conf_['data']['policies']:
            i = 0
            for source_address_set_ in policy_["match"]["source-address-sets"]:
                source_address_set_dict = {source_address_set_:address_set_full_[source_address_set_]}
                psef_conf_['data']['policies'][j]["match"]["source-address-sets"][i] = source_address_set_dict
                i = i + 1
            i = 0
            for destination_address_set_ in policy_["match"]["destination-address-sets"]:
                destination_address_set_dict = {destination_address_set_:address_set_full_[destination_address_set_]}
                psef_conf_['data']['policies'][j]["match"]["destination-address-sets"][i] = destination_address_set_dict
                i = i + 1
            i = 0
            for service_set_ in policy_["match"]["service-sets"]:
                service_set_dict_ = {}
                service_set_full_dict = {}
                service_set_full_dict = service_set_full_[service_set_]
                psef_conf_['data']['policies'][j]["match"]["service-sets"][i] = service_set_full_dict
                i = i + 1
            j = j + 1

    # full address-sets
    if ('address-sets' in psef_conf_['data']):
        i = 0
        for address_set_el in psef_conf_['data']['address-sets']:
            j = 0
            for address_el in address_set_el['addresses']:
                psef_conf_['data']['address-sets'][i]['addresses'][j] = address_full_[address_el]
                j = j + 1
            if (address_set_el['epg'] == 'false'):
                psef_conf_['data']['address-sets'][i]['address-set-alias-2'] = address_set_el['address-set-name']
            i = i + 1
    # full service-sets
    if ('service-sets' in psef_conf_['data']):
        i = 0
        for service_set_el in psef_conf_['data']['service-sets']:
            j = 0
            for service_el in service_set_el['services']:
                psef_conf_['data']['service-sets'][i]['services'][j] = service_full_[service_el]
                j = j + 1
            i = i + 1

    # full application-sets
    if ('application-sets' in psef_conf_['data']):
        i = 0
        for application_set_el in psef_conf_['data']['application-sets']:
            j = 0
            for application_el in application_set_el['applications']:
                psef_conf_['data']['application-sets'][i]['applications'][j] = application_full_[application_el]
                j = j + 1
            i = i + 1

    return (psef_conf_)

def service_full (psef_conf):

##########  Description  #######
    '''
    used by psef_full()
    create separate dictionaries for services and
    create separate full (with services information) dictionaries for service-sets
    '''
#############  BODY ############

    psef_conf_ = copy.deepcopy(psef_conf)

    service_full = {}
    service_set_full = {}
    
    if 'services' in psef_conf_['data']:
        for service_element in psef_conf_['data']['services']:
            service_full[service_element['service-name']] = service_element
    if 'service-sets' in psef_conf_['data']:
        for service_set_element in psef_conf_['data']['service-sets']:
            service_set_full[service_set_element['service-set-name']] = service_set_element
            service_set_full_el = []
            for addr_element in service_set_element['services']:
                service_set_full_el.append(service_full[addr_element])
            service_set_full[service_set_element['service-set-name']]['services'] = service_set_full_el

    return (service_full, service_set_full)

def application_full (psef_conf):

##########  Description  #######
    '''
    used by psef_full()
    create separate dictionaries for applications and
    create separate full (with applications information) dictionaries for application-sets
    '''
#############  BODY ############

    psef_conf_ = copy.deepcopy(psef_conf)

    application_full = {}
    application_set_full = {}

    if 'applications' in psef_conf_['data']:
        for application_element in psef_conf_['data']['applications']:
            application_full[application_element['application-name']] = application_element
    if 'application-sets' in psef_conf_['data']:
        for application_set_element in psef_conf_['data']['application-sets']:
            application_set_full[application_set_element['application-set-name']] = application_set_element
            application_set_full_el = []
            for addr_element in application_set_element['applications']:
                application_set_full_el.append(application_full[addr_element])
            application_set_full[application_set_element['application-set-name']]['applications'] = application_set_full_el

    return (application_full, application_set_full)


def address_full (psef_conf):

##########  Description  #######
    '''
    used by psef_full()
    create separate dictionaries for addresses and
    create separate full (with addresses information) dictionaries for address-sets
    '''
#############  BODY ############
 
    psef_conf_ = copy.deepcopy(psef_conf)

    address_full = {}
    address_set_full = {}
    if 'addresses' in psef_conf_['data']:
        for address_element in psef_conf_['data']['addresses']:
            address_full[address_element['address-name']] = address_element
    if 'address-sets' in psef_conf_['data']:
        for address_set_element in psef_conf_['data']['address-sets']:
            address_set_full[address_set_element['address-set-name']] = address_set_element
            address_set_full_el = []
            for addr_element in address_set_element['addresses']:
                address_set_full_el.append(address_full[addr_element])
            address_set_full[address_set_element['address-set-name']]['addresses'] = address_set_full_el

    return (address_full, address_set_full)

def default_change (psef_conf_):

    '''
    change the value of default parameters if necessary
    '''

    psef_conf_parameters = copy.deepcopy(psef_conf_)
    
    if 'addresses' in psef_conf_parameters['data']:
        for addresses_element in psef_conf_parameters['data']['addresses']:
            if (not addresses_element['address-alias-1']):
                address_element['address-alias-1'] = addresses_element['address-set-name']

    if 'address-sets' in psef_conf_parameters['data']:
        for address_set_element in psef_conf_parameters['data']['address-sets']:
            if (not address_set_element['address-set-alias-1']):
                address_set_element['address-set-alias-1'] = address_set_element['address-set-name']
            if (address_set_element['epg'] != 'true'):
                address_set_element['address-set-alias-2'] = address_set_element['address-set-name']
                address_set_element['parameters'] = ''

    if 'services' in psef_conf_parameters['data']:
        for services_element in psef_conf_parameters['data']['services']:
            if (not services_element['service-alias-1']):
                address_element['service-alias-1'] = services_element['service-set-name']

    if 'service-sets' in psef_conf_parameters['data']:
        for address_set_element in psef_conf_parameters['data']['service-sets']:
            if (not address_set_element['service-set-alias-1']):
                address_set_element['service-set-alias-1'] = address_set_element['service-set-name']
            if (not address_set_element['service-set-alias-2']):
                address_set_element['service-set-alias-2'] = address_set_element['service-set-name']

    if 'applications' in psef_conf_parameters['data']:
        for applications_element in psef_conf_parameters['data']['applications']:
#            if (not applications_element['application-alias-1']):
#                address_element['application-alias-1'] = applications_element['application-set-name']
            continue

    if 'application-sets' in psef_conf_parameters['data']:
        for address_set_element in psef_conf_parameters['data']['application-sets']:
#            if (not address_set_element['application-set-alias-1']):
#                address_set_element['application-set-alias-1'] = address_set_element['application-set-name']
#            if (not address_set_element['application-set-alias-2']):
#                address_set_element['application-set-alias-2'] = address_set_element['application-set-name']
            continue

    if ('policies' in psef_conf_parameters['data']):
        for policy_element in psef_conf_parameters['data']['policies']:
            if (not policy_element['policy-alias-1']):
                policy_element['policy-alias-1'] = policy_element['policy-name']
            if (not policy_element['policy-alias-2']):
                policy_element['policy-alias-2'] = policy_element['policy-name']


    return psef_conf_parameters


