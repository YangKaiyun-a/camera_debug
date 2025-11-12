namespace cpp OverheadReg

enum ClassID // 孔位类型ID
{
    Unknown   = -1; // 未知状态
    NoTube    = 0;  // 无试管
    NoHatTube = 1;  // 无帽试管
    HatTube   = 2;  // 有帽试管
}   

struct Bbox // 目标包围框
{
    1: i32 x = 0;
    2: i32 y = 0;
    3: i32 w = 0;
    4: i32 h = 0;
}

struct DetectionC // 目标信息
{
    1: ClassID class_id = ClassID.Unknown; // 孔位类型ID
    2: double cla_score = 0.0;             // 位置置信度得分
    3: Bbox box;                           // 目标包围框信息
}

struct ImageInfo // GBR图像信息
{
    1: i32    width;  // 图像宽度
    2: i32    height; // 图像高度
    3: binary data;   // 图像数据
}

typedef list<DetectionC> DetectionList;

struct HolesRecgInfo // 样本管孔位识别信息
{
    1: optional DetectionList holes;     // 视场范围的样本管孔位信息
    2: optional ImageInfo     image;     // 原始图像信息
    3: optional ImageInfo     imageMark; // 标记后的图像信息
}

enum TaskState // 任务状态
{
    NoneState   = 0; // 无进展
    Issued      = 1; // 已下发
    Identifying = 2; // 识别中
    Finished    = 3; // 已完成
}

enum TaskResult // 任务结果
{
    Success       = 0; // 成功
    CameraFault   = 1; // 相机异常
    UnknownFault  = 3; // 未知异常
}

struct TaskInfo // 任务信息
{
    1: string                 taskId;    // 任务ID
    2: TaskState              state;     // 任务状态
    3: optional TaskResult    result;    // 任务结果
    4: optional HolesRecgInfo info;      // 试管识别信息
}

enum RunningState // 运行状态
{
    Ready    = 0; // 就绪
    Reseting = 1; // 复位中
    Stop     = 2; // 停机
    Fault    = 3; // 错误
}

struct DeviceInfo // 设备信息
{
    1: RunningState runningState; // 运行状态
}

