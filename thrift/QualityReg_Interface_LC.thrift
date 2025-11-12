namespace cpp QualityReg

include "QualityReg_Defs.thrift"

service QualityRegLC { //下位机服务接口
    void HeartbeatToLC(1:i64 timeStamp);                   // 发送心跳到下位机
    i32 DistributeTask(1:QualityReg_Defs.TaskInfo info);  // 发布任务
    QualityReg_Defs.TaskInfo GetTaskInfo();               // 获取任务信息
    QualityReg_Defs.DeviceInfo GetDeviceInfo();           // 获取设备信息
}



