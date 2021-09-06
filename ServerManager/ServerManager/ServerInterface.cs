using System;
using System.Collections;
using System.Collections.Generic;
using System.Net;
using System.Net.Sockets;
using System.Text;

namespace ServerManager
{
    class ServerInterface
    {
        Socket sock;
        List<ReceivePayloadPacket> packets;

        public ServerInterface()
        {
            IPAddress remoteIP = IPAddress.Parse("192.168.1.33");

            this.sock = new Socket(remoteIP.AddressFamily, SocketType.Stream, ProtocolType.Tcp);
            this.sock.Connect(new IPEndPoint(remoteIP, 42069));

            this.packets = new List<ReceivePayloadPacket>();
        }

        public List<ReceivePayloadPacket> IncomingPayloads
        {
            get
            {
                while (this.sock.Available > 0)
                {
                    this.packets.Add(ReceivePayloadPacket.Deserialize(this.Receive()));
                }
                var packets = this.packets;
                this.packets = new List<ReceivePayloadPacket>();
                return packets;
            }
        }

        public GetDevicesResponsePacket GetDevices()
        {
            this.Send(new GetDevicesPacket());

            return GetDevicesResponsePacket.Deserialize(this.GetServerResponse());
        }

        public RegisterDeviceResponsePacket Register(string name, string description, string version, string @interface, bool force)
        {
            this.Send(new RegisterDevicePacket(name, description, version, @interface, force));

            return RegisterDeviceResponsePacket.Deserialize(this.GetServerResponse());
        }

        public UnregisterDeviceResponsePacket Unregister()
        {
            this.Send(new UnregisterDevicePacket());

            return UnregisterDeviceResponsePacket.Deserialize(this.GetServerResponse());
        }

        public GetDeviceInfoResponsePacket GetDeviceInfo(string deviceName)
        {
            this.Send(new GetDeviceInfoPacket(deviceName));

            return GetDeviceInfoResponsePacket.Deserialize(this.GetServerResponse());
        }

        public ServerResponsePacket SendPayload(string target, string payload)
        {
            this.Send(new SendPayloadPacket(target, payload));

            return ServerResponsePacket.Deserialize(GetServerResponse());
        }

        private void Send(SentPacket packet)
        {
            this.sock.Send(Encoding.ASCII.GetBytes(packet.Serialize()));
        }

        private string GetServerResponse()
        {
            while (true)
            {
                string packet = Receive();
                if (ReceivePayloadPacket.IsReceivePayloadPacket(packet))
                    this.packets.Add(ReceivePayloadPacket.Deserialize(packet));
                else
                    return packet;
            }
        }

        private string Receive()
        {
            byte[] buffer = new byte[1024];
            this.sock.Receive(buffer);
            return Encoding.ASCII.GetString(buffer).Trim('\0');
        }
    }
}
