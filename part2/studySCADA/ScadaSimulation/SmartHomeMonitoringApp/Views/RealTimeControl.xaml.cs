﻿using MahApps.Metro.Controls;
using Newtonsoft.Json;
using SmartHomeMonitoringApp.Logics;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using uPLibrary.Networking.M2Mqtt.Messages;

namespace SmartHomeMonitoringApp.Views
{
    /// <summary>
    /// RealTimeControl.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class RealTimeControl : UserControl
    {
        public RealTimeControl()
        {
            InitializeComponent();

            // 모든 차트의 최초 값을 0으로 초기화
            LvcLivingTemp.Value = LvcDiningTemp.Value = LvcBedTemp.Value = LvcBathTemp.Value=0;
            LvcLivingHumid.Value = LvcDiningHumid.Value = LvcBedHumid.Value = LvcBedHumid.Value = 0;
        }

        private void UserControl_Loaded(object sender, RoutedEventArgs e)
        {
            if (Commons.MQTT_CLIENT != null && Commons.MQTT_CLIENT.IsConnected)
            {   // DB 모니터링을 실행 한 뒤 실시간 모니터링으로 넘어왔다면
                Commons.MQTT_CLIENT.MqttMsgPublishReceived += MQTT_CLIENT_MqttMsgPublishReceived;
            }
            else // DB 모니터링을 실행하지 않고 바로 실시간 모니터링 메뉴를 클릭했으면
            {
                // Mqtt 브로커 생성
                Commons.MQTT_CLIENT = new uPLibrary.Networking.M2Mqtt.MqttClient(Commons.BROKERHOST);

                // Mqtt 접속
                Commons.MQTT_CLIENT.MqttMsgPublishReceived += MQTT_CLIENT_MqttMsgPublishReceived;
                Commons.MQTT_CLIENT.Connect("MONITOR"); // clientId = 모니터
                Commons.MQTT_CLIENT.Subscribe(new string[] { Commons.MQTTTOPIC },
                        new byte[] { MqttMsgBase.QOS_LEVEL_AT_LEAST_ONCE }); // QOS는 네트워크 통신에 옵
            }
        }
       

        // MQTTclient는 단독스레드 사용, UI스레드에 직접 접근이 안됨
        // this.INVOKE(); --> UI스레드 안에 있는 리소스 접근 가능
        private void MQTT_CLIENT_MqttMsgPublishReceived(object sender, MqttMsgPublishEventArgs e)
        {
            var msg = Encoding.UTF8.GetString(e.Message);
            Debug.WriteLine(msg);
            var currSensor = JsonConvert.DeserializeObject<Dictionary<string,string>>(msg);

            if (currSensor["Home_Id"] == "D101H703") // D101H703은 사용자 DB에서 동적으로 가져와야할 값
            {

                this.Invoke(() =>
                {
                    var dfValue = DateTime.Parse(currSensor["Sensing_DateTime"]).ToString("yyyy-MM-dd HH:mm:ss");
                    LblSensingDt.Content = $"Sensing DateTime : {dfValue}";
                });

                switch (currSensor["Room_Name"].ToUpper())
                {
                    case "LIVING":
                        this.Invoke(() =>
                        {
                        LvcLivingTemp.Value = Math.Round(Convert.ToDouble(currSensor["Temp"]), 1);
                        LvcLivingHumid.Value = Convert.ToDouble(currSensor["Humid"]);
                        });
                        break;

                    case "DINING":
                        this.Invoke(() =>
                        {
                            LvcDiningTemp.Value = Math.Round(Convert.ToDouble(currSensor["Temp"]),1);
                            LvcLivingHumid.Value = Convert.ToDouble(currSensor["Humid"]);
                        });
                        break;

                    case "BED":
                        this.Invoke(() =>
                        {
                            LvcBedTemp.Value = Math.Round(Convert.ToDouble(currSensor["Temp"]), 1);
                            LvcBedHumid.Value = Convert.ToDouble(currSensor["Humid"]);
                        });
                        break;

                    case "BATH":
                        this.Invoke(() =>
                        {
                            LvcBathTemp.Value = Math.Round(Convert.ToDouble(currSensor["Temp"]), 1);
                            LvcBathHumid.Value = Convert.ToDouble(currSensor["Humid"]);
                        });
                        break;

                    default:
                        break;
                }
            }
        }

    }
}
