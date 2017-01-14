"""
    Purpose: methods that interacts with with network interfaces
    
    Usage : none, import it to your py and use it. (you may implement it)
    
    Author : anonymous (with the help of stackoverflow)

"""

# IMPORTS
import netifaces
import _winreg  # in case of python 3.0 use winreg.
import sys
from pprint import pprint

# CONSTANTS
UNKNOWN = '(unknown)'
# the key where all interfaces are..
INTERFACES_CLASS_KEY = r'SYSTEM\CurrentControlSet\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}'
INTERFACES_NETWORK_KEY = r'SYSTEM\CurrentControlSet\Control\Network\{4d36e972-e325-11ce-bfc1-08002be10318}'
CONNECTION_KEY = r'\Connection'
NAME_SUB_KEY = 'Name'
INSTANCE_ID_KEY = 'NetCfgInstanceId'
DRIVER_NAME_KEY = 'DriverDesc'
WINDOWS_ERROR_2 = 2
WINDOWS_ERROR_5 = 5
WINDOWS = "win32"


def _get_driver_name_linux():
    return netifaces.interfaces()


def _get_driver_name_windows():
    """
        Purpose : get interface (real) name for usage of many programs from their guid.

    :return tuple: (iface_list, tuple_iface_error_list) the first item is interfaces list, the other
     is a list which every item is a tuple, the guid and the error.
    """

    iface_guids = netifaces.interfaces()
    # a list that contains unknown until the corresponding iface will replace it (in case of errors..)
    iface_names = [UNKNOWN for i in range(len(iface_guids))]
    iface_errors = []

    hklm_key = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
    interfaces_class_key = _winreg.OpenKey(hklm_key, INTERFACES_CLASS_KEY)

    # QueryInfoKey returns a tuple , the first item is the number of sub_keys.
    # num_of_interfaces = _winreg.QueryInfoKey(interfaces_class_key)[0]
    num_of_interfaces = len(iface_guids)

    for index in range(num_of_interfaces):
        sub_key_name = _winreg.EnumKey(interfaces_class_key, index)
        try:
            reg_sub_key = _winreg.OpenKey(interfaces_class_key, sub_key_name)
            guid = _winreg.QueryValueEx(reg_sub_key, INSTANCE_ID_KEY)[0]
            try:
                guid_idx = iface_guids.index(guid)
                iface_names[guid_idx] = _winreg.QueryValueEx(reg_sub_key, DRIVER_NAME_KEY)[0]
            except ValueError as error:
                iface_errors.append((error, guid))
        except WindowsError as error:
            # cannot find the inerface in the registry which the guid corresponds to.
            if error.errno == WINDOWS_ERROR_2:
                iface_errors.append((error, guid))

            # doesn't have the access to the file (someone must be using it..)
            elif error.errno == WINDOWS_ERROR_5:
                iface_errors.append((error, guid))

    return iface_names, iface_errors


def _get_connection_name_from_guid():
    """
        Purpose: get connection name from guid
    :return tuple: (iface_connection_list, tuple_iface_connection_error_list) the first item is interfaces list, the other
     is a list which every item is a tuple, the guid and the error.
    """

    iface_guids = netifaces.interfaces()
    # a list that contains unknown until the corresponding iface will replace it (in case of errors..)
    iface_connection_names = [UNKNOWN for i in range(len(iface_guids))]
    iface_connection_errors = []

    reg = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
    reg_key = _winreg.OpenKey(reg, INTERFACES_NETWORK_KEY)

    for guid_idx in range(len(iface_guids)):
        try:
            reg_sub_key = _winreg.OpenKey(reg_key, iface_guids[guid_idx] + CONNECTION_KEY)
            iface_connection_names[guid_idx] = _winreg.QueryValueEx(reg_sub_key, NAME_SUB_KEY)[0]
        except WindowsError as error:
            iface_connection_errors.append((error, iface_guids[guid_idx]))

    return iface_connection_names, iface_connection_errors


def _interface_chooser(ifaces):
    # a space
    print ""
    for idx in range(len(ifaces)):
        print "%d - %s" % (idx, ifaces[idx])

    try:
        iface_number = int(raw_input("choose interface number : "))
    except ValueError:
        sys.exit("not an integer.. exiting..")

    print len(ifaces)
    if iface_number < 0 or iface_number >= len(ifaces):
        sys.exit("id does not exists, exiting..")
    iface = ifaces[iface_number]
    return iface


def get_requested_interface():
    platform_name = sys.platform

    if WINDOWS == platform_name:
        ifaces, iface_errors = _get_driver_name_windows()
    else:
        ifaces, iface_errors = _get_driver_name_linux()

    iface = _interface_chooser(ifaces)
    return iface


if __name__ == '__main__':
    interfaces_names, interfaces_errors = _get_driver_name_windows()
    # pretty print..
    pprint(interfaces_names)
