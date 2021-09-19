
namespace ServerManager
{
    partial class Form1
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.richTextBoxMonitor = new System.Windows.Forms.RichTextBox();
            this.labelMonitor = new System.Windows.Forms.Label();
            this.labelDeviceList = new System.Windows.Forms.Label();
            this.buttonRefreshDevicesList = new System.Windows.Forms.Button();
            this.buttonRegister = new System.Windows.Forms.Button();
            this.textBoxDeviceName = new System.Windows.Forms.TextBox();
            this.labelDeviceName = new System.Windows.Forms.Label();
            this.buttonUnregister = new System.Windows.Forms.Button();
            this.listBoxRegisteredDevices = new System.Windows.Forms.ListBox();
            this.richTextBoxOutput = new System.Windows.Forms.RichTextBox();
            this.labelOutput = new System.Windows.Forms.Label();
            this.buttonGetInfo = new System.Windows.Forms.Button();
            this.checkBoxForceRegister = new System.Windows.Forms.CheckBox();
            this.textBoxSendPayload = new System.Windows.Forms.TextBox();
            this.buttonSendPayload = new System.Windows.Forms.Button();
            this.label1 = new System.Windows.Forms.Label();
            this.buttonCheckForPayloads = new System.Windows.Forms.Button();
            this.buttonConnect = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // richTextBoxMonitor
            // 
            this.richTextBoxMonitor.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.richTextBoxMonitor.HideSelection = false;
            this.richTextBoxMonitor.Location = new System.Drawing.Point(12, 305);
            this.richTextBoxMonitor.Name = "richTextBoxMonitor";
            this.richTextBoxMonitor.ReadOnly = true;
            this.richTextBoxMonitor.Size = new System.Drawing.Size(804, 115);
            this.richTextBoxMonitor.TabIndex = 0;
            this.richTextBoxMonitor.Text = "";
            this.richTextBoxMonitor.TextChanged += new System.EventHandler(this.richTextBoxMonitor_TextChanged);
            // 
            // labelMonitor
            // 
            this.labelMonitor.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left)));
            this.labelMonitor.AutoSize = true;
            this.labelMonitor.Location = new System.Drawing.Point(12, 287);
            this.labelMonitor.Name = "labelMonitor";
            this.labelMonitor.Size = new System.Drawing.Size(50, 15);
            this.labelMonitor.TabIndex = 1;
            this.labelMonitor.Text = "Monitor";
            // 
            // labelDeviceList
            // 
            this.labelDeviceList.AutoSize = true;
            this.labelDeviceList.Location = new System.Drawing.Point(218, 9);
            this.labelDeviceList.Name = "labelDeviceList";
            this.labelDeviceList.Size = new System.Drawing.Size(105, 15);
            this.labelDeviceList.TabIndex = 2;
            this.labelDeviceList.Text = "Registered Devices";
            // 
            // buttonRefreshDevicesList
            // 
            this.buttonRefreshDevicesList.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left)));
            this.buttonRefreshDevicesList.Location = new System.Drawing.Point(218, 232);
            this.buttonRefreshDevicesList.Name = "buttonRefreshDevicesList";
            this.buttonRefreshDevicesList.Size = new System.Drawing.Size(200, 23);
            this.buttonRefreshDevicesList.TabIndex = 4;
            this.buttonRefreshDevicesList.Text = "Refresh";
            this.buttonRefreshDevicesList.UseVisualStyleBackColor = true;
            this.buttonRefreshDevicesList.Click += new System.EventHandler(this.buttonRefreshDevicesList_Click);
            // 
            // buttonRegister
            // 
            this.buttonRegister.Location = new System.Drawing.Point(12, 85);
            this.buttonRegister.Name = "buttonRegister";
            this.buttonRegister.Size = new System.Drawing.Size(200, 23);
            this.buttonRegister.TabIndex = 5;
            this.buttonRegister.Text = "Register";
            this.buttonRegister.UseVisualStyleBackColor = true;
            this.buttonRegister.Click += new System.EventHandler(this.buttonRegister_Click);
            // 
            // textBoxDeviceName
            // 
            this.textBoxDeviceName.Location = new System.Drawing.Point(12, 56);
            this.textBoxDeviceName.Name = "textBoxDeviceName";
            this.textBoxDeviceName.Size = new System.Drawing.Size(200, 23);
            this.textBoxDeviceName.TabIndex = 6;
            this.textBoxDeviceName.Text = "server_manager";
            // 
            // labelDeviceName
            // 
            this.labelDeviceName.AutoSize = true;
            this.labelDeviceName.Location = new System.Drawing.Point(12, 38);
            this.labelDeviceName.Name = "labelDeviceName";
            this.labelDeviceName.Size = new System.Drawing.Size(77, 15);
            this.labelDeviceName.TabIndex = 7;
            this.labelDeviceName.Text = "Device Name";
            // 
            // buttonUnregister
            // 
            this.buttonUnregister.Location = new System.Drawing.Point(12, 139);
            this.buttonUnregister.Name = "buttonUnregister";
            this.buttonUnregister.Size = new System.Drawing.Size(200, 23);
            this.buttonUnregister.TabIndex = 8;
            this.buttonUnregister.Text = "Unregister";
            this.buttonUnregister.UseVisualStyleBackColor = true;
            this.buttonUnregister.Click += new System.EventHandler(this.buttonUnregister_Click);
            // 
            // listBoxRegisteredDevices
            // 
            this.listBoxRegisteredDevices.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left)));
            this.listBoxRegisteredDevices.FormattingEnabled = true;
            this.listBoxRegisteredDevices.ItemHeight = 15;
            this.listBoxRegisteredDevices.Location = new System.Drawing.Point(218, 27);
            this.listBoxRegisteredDevices.Name = "listBoxRegisteredDevices";
            this.listBoxRegisteredDevices.Size = new System.Drawing.Size(200, 199);
            this.listBoxRegisteredDevices.TabIndex = 9;
            // 
            // richTextBoxOutput
            // 
            this.richTextBoxOutput.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.richTextBoxOutput.Location = new System.Drawing.Point(424, 27);
            this.richTextBoxOutput.Name = "richTextBoxOutput";
            this.richTextBoxOutput.ReadOnly = true;
            this.richTextBoxOutput.Size = new System.Drawing.Size(392, 228);
            this.richTextBoxOutput.TabIndex = 10;
            this.richTextBoxOutput.Text = "";
            // 
            // labelOutput
            // 
            this.labelOutput.AutoSize = true;
            this.labelOutput.Location = new System.Drawing.Point(424, 9);
            this.labelOutput.Name = "labelOutput";
            this.labelOutput.Size = new System.Drawing.Size(45, 15);
            this.labelOutput.TabIndex = 11;
            this.labelOutput.Text = "Output";
            // 
            // buttonGetInfo
            // 
            this.buttonGetInfo.Location = new System.Drawing.Point(12, 168);
            this.buttonGetInfo.Name = "buttonGetInfo";
            this.buttonGetInfo.Size = new System.Drawing.Size(200, 23);
            this.buttonGetInfo.TabIndex = 12;
            this.buttonGetInfo.Text = "Get Device Info";
            this.buttonGetInfo.UseVisualStyleBackColor = true;
            this.buttonGetInfo.Click += new System.EventHandler(this.buttonGetInfo_Click);
            // 
            // checkBoxForceRegister
            // 
            this.checkBoxForceRegister.AutoSize = true;
            this.checkBoxForceRegister.Location = new System.Drawing.Point(12, 114);
            this.checkBoxForceRegister.Name = "checkBoxForceRegister";
            this.checkBoxForceRegister.Size = new System.Drawing.Size(100, 19);
            this.checkBoxForceRegister.TabIndex = 13;
            this.checkBoxForceRegister.Text = "Force Register";
            this.checkBoxForceRegister.UseVisualStyleBackColor = true;
            // 
            // textBoxSendPayload
            // 
            this.textBoxSendPayload.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.textBoxSendPayload.Location = new System.Drawing.Point(12, 261);
            this.textBoxSendPayload.Name = "textBoxSendPayload";
            this.textBoxSendPayload.Size = new System.Drawing.Size(738, 23);
            this.textBoxSendPayload.TabIndex = 14;
            this.textBoxSendPayload.KeyUp += new System.Windows.Forms.KeyEventHandler(this.textBoxSendPayload_KeyUp);
            // 
            // buttonSendPayload
            // 
            this.buttonSendPayload.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Right)));
            this.buttonSendPayload.Location = new System.Drawing.Point(756, 261);
            this.buttonSendPayload.Name = "buttonSendPayload";
            this.buttonSendPayload.Size = new System.Drawing.Size(60, 23);
            this.buttonSendPayload.TabIndex = 15;
            this.buttonSendPayload.Text = "Send";
            this.buttonSendPayload.UseVisualStyleBackColor = true;
            this.buttonSendPayload.Click += new System.EventHandler(this.buttonSendPayload_Click);
            // 
            // label1
            // 
            this.label1.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left)));
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(12, 240);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(78, 15);
            this.label1.TabIndex = 16;
            this.label1.Text = "Send Payload";
            // 
            // buttonCheckForPayloads
            // 
            this.buttonCheckForPayloads.Location = new System.Drawing.Point(12, 197);
            this.buttonCheckForPayloads.Name = "buttonCheckForPayloads";
            this.buttonCheckForPayloads.Size = new System.Drawing.Size(200, 23);
            this.buttonCheckForPayloads.TabIndex = 17;
            this.buttonCheckForPayloads.Text = "Check For Payloads";
            this.buttonCheckForPayloads.UseVisualStyleBackColor = true;
            this.buttonCheckForPayloads.Click += new System.EventHandler(this.buttonCheckForPayloads_Click);
            // 
            // buttonConnect
            // 
            this.buttonConnect.Location = new System.Drawing.Point(12, 12);
            this.buttonConnect.Name = "buttonConnect";
            this.buttonConnect.Size = new System.Drawing.Size(200, 23);
            this.buttonConnect.TabIndex = 18;
            this.buttonConnect.Text = "Connect";
            this.buttonConnect.UseVisualStyleBackColor = true;
            this.buttonConnect.Click += new System.EventHandler(this.buttonConnect_Click);
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 15F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(828, 432);
            this.Controls.Add(this.buttonConnect);
            this.Controls.Add(this.buttonCheckForPayloads);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.buttonSendPayload);
            this.Controls.Add(this.textBoxSendPayload);
            this.Controls.Add(this.checkBoxForceRegister);
            this.Controls.Add(this.buttonGetInfo);
            this.Controls.Add(this.labelOutput);
            this.Controls.Add(this.richTextBoxOutput);
            this.Controls.Add(this.listBoxRegisteredDevices);
            this.Controls.Add(this.buttonUnregister);
            this.Controls.Add(this.labelDeviceName);
            this.Controls.Add(this.textBoxDeviceName);
            this.Controls.Add(this.buttonRegister);
            this.Controls.Add(this.buttonRefreshDevicesList);
            this.Controls.Add(this.labelDeviceList);
            this.Controls.Add(this.labelMonitor);
            this.Controls.Add(this.richTextBoxMonitor);
            this.Name = "Form1";
            this.Text = "Form1";
            this.Load += new System.EventHandler(this.Form1_Load);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.RichTextBox richTextBoxMonitor;
        private System.Windows.Forms.Label labelMonitor;
        private System.Windows.Forms.Label labelDeviceList;
        private System.Windows.Forms.Button buttonRefreshDevicesList;
        private System.Windows.Forms.Button buttonRegister;
        private System.Windows.Forms.TextBox textBoxDeviceName;
        private System.Windows.Forms.Label labelDeviceName;
        private System.Windows.Forms.Button buttonUnregister;
        private System.Windows.Forms.ListBox listBoxRegisteredDevices;
        private System.Windows.Forms.RichTextBox richTextBoxOutput;
        private System.Windows.Forms.Label labelOutput;
        private System.Windows.Forms.Button buttonGetInfo;
        private System.Windows.Forms.CheckBox checkBoxForceRegister;
        private System.Windows.Forms.TextBox textBoxSendPayload;
        private System.Windows.Forms.Button buttonSendPayload;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Button buttonCheckForPayloads;
        private System.Windows.Forms.Button buttonConnect;
    }
}

