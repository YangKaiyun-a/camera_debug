namespace cpp OverheadReg

include "OverheadReg_Defs.thrift"

service OverheadRegLC { //下位机服务接口
    void HeartbeatToLC(1:i64 timeStamp);                  // 发送心跳到下位机
    i32 DistributeTask(1:OverheadReg_Defs.TaskInfo info);  // 发布任务
    OverheadReg_Defs.TaskInfo GetTaskInfo();               // 获取任务信息
    OverheadReg_Defs.DeviceInfo GetDeviceInfo();           // 获取设备信息
}



