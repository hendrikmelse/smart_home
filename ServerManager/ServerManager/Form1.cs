using System;
using System.Linq;
using System.Windows.Forms;

namespace ServerManager
{
    public partial class Form1 : Form
    {
        ServerInterface server;
        public Form1()
        {
            InitializeComponent();
            this.server = new ServerInterface();
        }

        private void Log(string message)
        {
            this.richTextBoxMonitor.Text += $"{message}\n";
        }

        private void RefreshRegisteredDevices()
        {
            this.listBoxRegisteredDevices.Items.Clear();
            var response = this.server.GetDevices();

            if (response == null)
            {
                this.Log("Not connected");
                return;
            }

            if (!response.success)
                this.Log($"Get devices failed: {response.error_message}");
            else
                this.listBoxRegisteredDevices.Items.AddRange(response.response);
        }

        private void SentPayloadToDevice()
        {
            string target = (string)this.listBoxRegisteredDevices.SelectedItem;
            if (target == null)
            {
                this.Log("Must select device to send message to");
                return;
            }

            var response = this.server.SendRawPayload(target, this.textBoxSendPayload.Text);

            if (response == null)
            {
                this.Log("Not connected");
                return;
            }

            if (!response.success)
                this.Log($"Failed to send payload: {response.error_message}");
            else
                this.Log("Sent payload");
        }

        private void Form1_Load(object sender, EventArgs e)
        {
        }

        private void buttonConnect_Click(object sender, EventArgs e)
        {
            if (this.server.Connect())
            {
                this.Log("Connected to server");
            }
            else
            {
                this.Log("Could not connect to server");
            }
        }

        private void buttonRefreshDevicesList_Click(object sender, EventArgs e)
        {
            this.RefreshRegisteredDevices();
        }

        private void buttonRegister_Click(object sender, EventArgs e)
        {
            var response = this.server.Register(
                this.textBoxDeviceName.Text,
                "A tool for interfacing with the server.",
                null,
                null,
                this.checkBoxForceRegister.Checked
            );

            if (response == null)
            {
                this.Log("Not connected");
                return;
            }

            if (!response.success)
                this.Log($"Error registering device: {response.error_message}");
            else
                this.Log($"Registered device: {this.textBoxDeviceName.Text}");

            this.RefreshRegisteredDevices();
        }

        private void buttonUnregister_Click(object sender, EventArgs e)
        {
            var response = this.server.Unregister();

            if (response == null)
            {
                this.Log("Not connected");
                return;
            }

            if (!response.success)
                this.Log($"Error unregistering device: {response.error_message}");
            else
                this.Log($"Unregistered device");

            this.RefreshRegisteredDevices();
        }

        private void buttonGetInfo_Click(object sender, EventArgs e)
        {
            string selectedDevice = (string)this.listBoxRegisteredDevices.SelectedItem;

            if (selectedDevice == null)
            {
                this.Log("No device selected");
                return;
            }

            var response = this.server.GetDeviceInfo(selectedDevice);
            this.richTextBoxOutput.Text = $"Name: {response.response.name}\n";
            this.richTextBoxOutput.Text += $"Description: {response.response.description}\n";
            this.richTextBoxOutput.Text += $"Version: {response.response.version}\n";
            this.richTextBoxOutput.Text += $"Interface: {response.response.@interface}\n";
        }
        private void buttonSendPayload_Click(object sender, EventArgs e)
        {
            this.SentPayloadToDevice();
        }

        private void textBoxSendPayload_KeyUp(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.Enter)
            {
                this.SentPayloadToDevice();
            }
        }

        private void buttonCheckForPayloads_Click(object sender, EventArgs e)
        {
            var packets = this.server.IncomingPayloads;

            if (packets.Count() == 0)
            {
                this.richTextBoxOutput.Text = "No incoming payloads";
                return;
            }

            this.richTextBoxOutput.Clear();

            foreach (var packet in packets)
            {
                this.richTextBoxOutput.Text += $"From: {packet.sender}\n\tPayload: {packet.payload}\n";
            }
        }

        private void richTextBoxMonitor_TextChanged(object sender, EventArgs e)
        {
            // Make the monitor box scroll with added text
            this.richTextBoxMonitor.SelectionStart = this.richTextBoxMonitor.Text.Length;
            this.richTextBoxMonitor.ScrollToCaret();
        }
    }
}
