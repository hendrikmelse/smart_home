using System.Text.Json;

namespace ServerManager
{
    abstract class Packet
    {
    }

    abstract class SentPacket : Packet
    {
        public string target { get; set; }

        abstract public string Serialize();
    }

    class ServerResponsePacket : Packet
    {
        public bool success { get; set; }
        public string response { get; set; }
        public string error_message { get; set; }

        public static ServerResponsePacket Deserialize(string serial)
        {
            return JsonSerializer.Deserialize<ServerResponsePacket>(serial);
        }
    }

    class GetDevicesPacket : SentPacket
    {
        public class GetDevicesPayload
        {
            public string command { get; set; } = "get_devices";
        }

        public GetDevicesPayload payload { get; set; } = new GetDevicesPayload();

        public GetDevicesPacket()
        {
            this.target = "server";
        }

        public override string Serialize()
        {
            return JsonSerializer.Serialize(this);
        }
    }

    class GetDevicesResponsePacket : ServerResponsePacket
    {
        public new string[] response { get; set; }

        public static GetDevicesResponsePacket Deserialize(string serial)
        {
            return JsonSerializer.Deserialize<GetDevicesResponsePacket>(serial);
        }
    }

    class RegisterDevicePacket : SentPacket
    {
        public class RegisterDevicePayload
        {
            public string command { get; set; } = "register";
            public string device_name { get; set; }
            public string description { get; set; }
            public string version { get; set; }
            public string @interface { get; set; }
            public bool force { get; set; }
        }

        public RegisterDevicePayload payload { get; set; } = new RegisterDevicePayload();

        public RegisterDevicePacket(string device_name, string description, string version, string @interface, bool force)
        {
            this.target = "server";
            this.payload.device_name = device_name;
            this.payload.description = description;
            this.payload.version = version;
            this.payload.@interface = @interface;
            this.payload.force = force;
        }

        public override string Serialize()
        {
            JsonSerializerOptions options = new JsonSerializerOptions
            {
                IgnoreNullValues = true
            };

            return JsonSerializer.Serialize(this, options);
        }
    }

    class RegisterDeviceResponsePacket : ServerResponsePacket
    {
        public static RegisterDeviceResponsePacket Deserialize(string serial)
        {
            return JsonSerializer.Deserialize<RegisterDeviceResponsePacket>(serial);
        }
    }

    class UnregisterDevicePacket : SentPacket
    {
        public class UnregisterDevicePayload
        {
            public string command { get; set; } = "unregister";
        }

        public UnregisterDevicePayload payload { get; set; } = new UnregisterDevicePayload();

        public UnregisterDevicePacket()
        {
            this.target = "server";
        }

        public override string Serialize()
        {
            return JsonSerializer.Serialize(this);
        }
    }

    class UnregisterDeviceResponsePacket : ServerResponsePacket
    {
        public static UnregisterDeviceResponsePacket Deserialize(string serial)
        {
            return JsonSerializer.Deserialize<UnregisterDeviceResponsePacket>(serial);
        }
    }

    class GetDeviceInfoPacket : SentPacket
    {
        public class GetDeviceInfoPayload
        {
            public string command { get; set; } = "get_device_info";
            public string device_name { get; set; }
        }

        public GetDeviceInfoPayload payload { get; set; } = new GetDeviceInfoPayload();

        public GetDeviceInfoPacket(string deviceName)
        {
            this.target = "server";
            this.payload.device_name = deviceName;
        }

        public override string Serialize()
        {
            return JsonSerializer.Serialize(this);
        }
    }

    class GetDeviceInfoResponsePacket : ServerResponsePacket
    {
        public class GetDeviceInfoResponse
        {
            public string name { get; set; }
            public string description { get; set; }
            public string version { get; set; }
            public string @interface { get; set; }
        }

        public new GetDeviceInfoResponse response { get; set; }

        public static GetDeviceInfoResponsePacket Deserialize(string serial)
        {
            return JsonSerializer.Deserialize<GetDeviceInfoResponsePacket>(serial);
        }
    }

    class SendPayloadPacket : SentPacket
    {
        public string payload { get; set; }

        public SendPayloadPacket(string target, string payload)
        {
            this.target = target;
            this.payload = payload;
        }

        public override string Serialize()
        {
            return JsonSerializer.Serialize(this);
        }
    }

    class ReceivePayloadPacket
    {
        public string sender { get; set; }
        public object payload { get; set; }

        public static bool IsReceivePayloadPacket(string serial)
        {
            ReceivePayloadPacket packet = Deserialize(serial);
            return packet.sender != null;
        }

        public static ReceivePayloadPacket Deserialize(string serial)
        {
            return JsonSerializer.Deserialize<ReceivePayloadPacket>(serial);
        }
    }
}
