namespace cpp OverheadReg

include "OverheadReg_Defs.thrift"

service OverheadRegUC { // 上位机服务接口
    void HeartbeatToUC(1:i64 timeStamp);                      // 发送心跳到上位机
    i32 DeviceInfoChanged(1:OverheadReg_Defs.DeviceInfo info); // 设备信息已改变
    i32 TaskInfoChanged(1:OverheadReg_Defs.TaskInfo info);     // 任务信息已改变
}
