# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import threading
import websocket
import time
from azure.cli.core._profile import Profile
from azext_serialtunnel._client_factory import cf_serial_port

# pylint: disable=too-few-public-methods
# pylint: disable=too-many-instance-attributes
class GlobalVariables:
    def __init__(self):
        self.websocket_instance = None
        self.serial_tunnel_instance = None
        self.loading = True
        self.first_message = True
        self.websocketstate = 0

GV = GlobalVariables()

class SerialTunnel:
    def __init__(self, cmd, resource_group_name, vm_vmss_name, vmss_instanceid):
        client = cf_serial_port(cmd.cli_ctx, )
        if vmss_instanceid is None:
            self.connect_func = lambda: client.connect(
                resource_group_name=resource_group_name,
                resource_provider_namespace="Microsoft.Compute",
                parent_resource_type="virtualMachines",
                parent_resource=vm_vmss_name,
                serial_port="0").connection_string
        else:
            self.connect_func = lambda: client.connect(
                resource_group_name=resource_group_name,
                resource_provider_namespace="Microsoft.Compute",
                parent_resource_type="virtualMachineScaleSets",
                parent_resource=f"{vm_vmss_name}/virtualMachines/{vmss_instanceid}",
                serial_port="0").connection_string
        self.websocket_url = None
        self.access_token = None
        self.new_auth_flow = "1"

    def load_websocket_url(self):
        print("Loading websocket URL...")
        token_info, _, _ = Profile().get_raw_token()
        self.access_token = token_info[1]
        try:
            self.websocket_url = self.connect_func()
        except:  # pylint: disable=bare-except
            print("Failed to grab websocket URL...")
            GV.websocketstate = 2
            return False
        print("Grabbed websocket URL: " + self.websocket_url)
        GV.websocketstate = 1
        return True

    def connect(self):
        def on_open(_):
            if self.new_auth_flow == "1":
                GV.websocket_instance.send(self.access_token)

        def on_message(_, message):
            if GV.first_message:
                if self.new_auth_flow == "1":
                    GV.websocket_instance.send(self.access_token)
                GV.first_message = False
                GV.loading = False
            else:
                print(message)

        def on_error(*_):
            pass

        def on_close(_):
            GV.loading = False

        def connect_thread():
            if self.load_websocket_url():
                GV.websocket_instance = websocket.WebSocketApp(
                    self.websocket_url + "?authorization=" + self.access_token + "&new=" + self.new_auth_flow,
                    on_open=on_open,
                    on_message=on_message,
                    on_error=on_error,
                    on_close=on_close)
                GV.websocket_instance.run_forever(skip_utf8_validation=True)
            else:
                GV.loading = False
                print("Could not establish connection to VM or VMSS ☹")

        GV.loading = True
        GV.first_message = True

        th = threading.Thread(target=connect_thread, args=())
        th.daemon = True
        th.start()

    def send(self, message):
        if GV.websocket_instance:
            if GV.first_message:
                GV.websocket_instance.send(self.access_token)
                GV.first_message = False
            GV.websocket_instance.send(message)
        else:
            print("No websocket connection established")

    def close(_):
        if GV.websocket_instance:
            GV.websocket_instance.close()
        else:
            print("No websocket connection established")

    def waitready(_):
        seconds = 0
        while GV.websocketstate == 0:
            print("Waiting for websocket to be ready (" + str(seconds) + " secs)...")
            time.sleep(5)
            seconds += 5
        if GV.websocketstate == 2:
            return False
        return True

def connect_serialtunnel(cmd, resource_group_name, vm_vmss_name, vmss_instanceid=None):
    print("Connecting to serial tunnel...")
    GV.serial_tunnel_instance = SerialTunnel(cmd, resource_group_name, vm_vmss_name, vmss_instanceid)
    GV.serial_tunnel_instance.connect()

    if not GV.serial_tunnel_instance.waitready():
        return False
    GV.serial_tunnel_instance.send("aaaa")
    time.sleep(10)
    GV.serial_tunnel_instance.close()