namespace cpp SimpleReg

include "SimpleReg_Defs.thrift"

service SimpleRegLC { //下位机服务接口
    void HeartbeatToLC(1:i64 timeStamp);                  // 发送心跳到下位机
    i32 DistributeTask(1:SimpleReg_Defs.TaskInfo info);  // 发布任务
    SimpleReg_Defs.TaskInfo GetTaskInfo();               // 获取任务信息
    SimpleReg_Defs.DeviceInfo GetDeviceInfo();           // 获取设备信息
}



