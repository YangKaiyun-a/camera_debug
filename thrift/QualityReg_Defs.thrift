namespace cpp QualityReg

enum TubeHatColor // 样本管帽信息
{
    Red     = 0; // 红色
    Blue    = 1; // 蓝色
    Black   = 2; // 黑色
    Green   = 3; // 绿色
    Purple  = 4; // 紫色
    Gray    = 5; // 灰色
    Orange  = 6; // 橙色
    Yellow  = 7; // 黄色
    White   = 8; // 白色
    Unknown = 9; // 未知
}   

struct TubeHatHSV // 样本管管帽颜色HSV值
{
    1: i32 H;
    2: i32 S;
    3: i32 V;
}

struct TubeHatInfo // 样本管管帽信息
{
    1: bool                  hasHat; // 管帽有无
    2: optional TubeHatColor color;  // 颜色
    3: optional TubeHatHSV   hsv;    // hsv值
}

enum TubeType // 样本管种类
{
    HitachiMicro    = 0; // 日立微量杯
    Unknown         = 1; // 无法识别类型
    QualityControl  = 3; // 质控品管
    HitachiStandard = 2; // 日立标准杯
    BloodCollection = 4; // 采血管
    Blank           = 5; // 空白
}

struct TubeSpec // 样本管规格
{
    1: i32 width;  // 样本管宽度，单位mm
    2: i32 height; // 样本管长度，单位mm
    3: i32 top;    // 样本管上部到样本管架的距离，单位mm
}

struct TubeInfo // 样本管基本信息
{
    1: TubeHatInfo hatInfo; // 管帽信息
    2: TubeType    type;    // 类型
    3: TubeSpec    spec;    // 规格
}

struct SerumIndex // 血清指数
{
    1: i32    hemolysisLevel;  // 溶血等级
    2: i32    icterusLevel;    // 黄疸等级
    3: i32    lipemiaLevel;    // 脂血等级
}

struct SampleHeight // 离心后样本分层高度,高度是指该层距离样本管底的高度(/mm)
{
    1: double serumHeight;     // 血清层高度
    2: double gelHeight;       // 凝胶层高度
    3: double cellsHeight;     // 红细胞高度
    4: double allSampleHeight; // 整体样本的高度
}

struct SampleVolume // 离心后样本分层体积
{
    1: double serumVolume;     // 血清层体积
    2: double gelVolume;       // 凝胶层体积 
    3: double cellsVolume;     // 红细胞体积
    4: double allSampleVolume; // 整体样本的体积
}

struct SampleSizeInfo // 样本量信息
{
    1: SampleHeight height; // 高度
    2: SampleVolume volume; // 体积
}

struct ImageInfo // GBR图像信息
{
    1: i32    width;  // 图像宽度
    2: i32    height; // 图像高度
    3: binary data;   // 图像数据
}

struct TubeRecgInfo // 样本管识别信息
{
    1: optional string           barcode;      // 样本管条码
    2: optional TubeInfo         tube;         // 样本管信息
    3: optional SerumIndex       index;        // 血清指数
    4: optional SampleSizeInfo   sample;       // 样本管中样本分层信息
    5: optional bool             centrifuged;  // 是否离心充分:true-是，false-否
    6: optional ImageInfo        liqImage;     // 最佳液面样本管图像
    7: optional ImageInfo        barImage;     // 最佳二维码样本管图像
    8: optional list<ImageInfo>  image;        // 样本管图像信息列表
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
    ScripperFault = 2; // 抓手异常
    UnknownFault  = 3; // 未知异常
}

struct TaskInfo // 任务信息
{
    1: string                taskId;    // 任务ID
    2: i32                   gripperId; // 抓手号
    3: TaskState             state;     // 任务状态
    4: optional TaskResult   result;    // 任务结果
    5: optional TubeRecgInfo info;      // 试管识别信息
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

