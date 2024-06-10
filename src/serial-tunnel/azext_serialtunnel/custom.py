# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import threading
import websocket
import socket
import time
import os
from azure.cli.core._profile import Profile
from azext_serialtunnel._client_factory import cf_serial_port

# pylint: disable=too-few-public-methods
# pylint: disable=too-many-instance-attributes

socket_path = '/tmp/serialtunnel.sock'

class GlobalVariables:
    def __init__(self):
        self.websocket_instance = None
        self.serial_tunnel_instance = None
        self.localsocket_instance = None
        self.localsocket_connection = None
        self.loading = True
        self.first_message = True
        self.startup_sink = True
        self.lastmsg = 0
        self.websocketstate = 0
        self.sendcount = 0
        self.recvcount = 0


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

        th = threading.Thread(target=self.local_server, args=())
        th.start()
        time.sleep(5)

    def local_server(_):
        # create a socket in /tmp/serialtunnel.sock, if it already exists, remove it first
        try:
            os.unlink(socket_path)
        except OSError:
            if os.path.exists(socket_path):
                raise

        try:
            GV.localsocket_instance = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            GV.localsocket_instance.bind(socket_path)
            #GV.localsocket_instance.settimeout(10)
        except:  # pylint: disable=bare-except
            print("Failed to create local socket...")
            return
        
        GV.localsocket_instance.listen(1)

        print("Waiting for connection from unix socket...")
        while True:
            try:
                GV.localsocket_connection, _ = GV.localsocket_instance.accept()
                print("New local socket connection recieved. Replacing localsocket_connection...")
            except socket.timeout:
                pass

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
        print(f"Grabbed websocket URL: {self.websocket_url}")
        GV.websocketstate = 1
        return True

    def connect(self):
        def on_open(_):
            if self.new_auth_flow == "1":
                GV.websocket_instance.send(self.access_token)

        def on_message(_, message):
            GV.recvcount += 1
            if GV.first_message:
                if self.new_auth_flow == "1":
                    print("Sending Auth Flow on message!")
                    GV.websocket_instance.send(self.access_token)
                GV.first_message = False
                GV.loading = False
                return
            elif GV.startup_sink:
                cur = time.time()
                if GV.lastmsg == 0 or (cur - GV.lastmsg < 0.001):
                    print(f"Sinking Startup Message #{str(GV.recvcount)} Waited {str(cur - GV.lastmsg)} seconds since previous message ...")
                    GV.lastmsg = cur
                    return
                else:
                    GV.startup_sink = False
                    print("Startup Sink Finalized...")
            #print(f"==================== RECV # {str(GV.recvcount)} ====================")
            #print(message)
            #print("=================================================================")
            GV.localsocket_connection.sendall(message.encode())

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

        def recv_local():
            print("Entering recv local loop...")
            while True:
                try:
                    data = GV.localsocket_connection.recv(1024)
                    if not data:
                        continue
                    self.send(data.decode())
                except socket.timeout:
                    print("benign socket timeout in recv_local")
                    pass
            print("!!!!!!!!!!!!!!! recv_local exiting now !!!!!!!!!!!!!!!!!!!!!")

        GV.loading = True
        GV.first_message = True

        th = threading.Thread(target=connect_thread, args=())
        th.daemon = True
        th.start()

        th2 = threading.Thread(target=recv_local, args=())
        th2.start()

    def send(self, message):
        GV.sendcount += 1
        if GV.websocket_instance:
            if GV.first_message:
                print("Sending first message access token")
                GV.websocket_instance.send(self.access_token)
                GV.first_message = False
            #print(f"==================== SEND # {str(GV.sendcount)} ====================")
            #print(message)
            #print("=================================================================")
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
        while (GV.websocketstate == 0 and GV.first_message == True):
            print(f"Waiting for websocket to be ready ({str(seconds)} secs)...")
            time.sleep(5)
            seconds += 5
        if GV.websocketstate == 2:
            return False
        return True

    def heartbeat(_, duration):
        seconds = 0
        while (seconds < duration):
            #print(f"Heartbeat: {str(seconds)} secs")
            GV.serial_tunnel_instance.send(f"HB{str(float(int(seconds * 100)/100))} ")
            time.sleep(10)
            seconds += 10

def connect_serialtunnel(cmd, resource_group_name, vm_vmss_name, vmss_instanceid=None):
    print("Connecting to serial tunnel...")
    GV.serial_tunnel_instance = SerialTunnel(cmd, resource_group_name, vm_vmss_name, vmss_instanceid)
    GV.serial_tunnel_instance.connect()

    if not GV.serial_tunnel_instance.waitready():
        return False

    #GV.serial_tunnel_instance.heartbeat(3000)
    time.sleep(3000)
    GV.serial_tunnel_instance.close()
    GV.localsocket_connection.close()