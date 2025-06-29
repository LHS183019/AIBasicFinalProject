# GlideHoop 用户手册 (English is not supported yet)

## 还在维护中！将尽快完善

* [演示&讲解视频](https://www.bilibili.com/video/BV1bvKrzwE2g/?share_source=copy_web&vd_source=128df80febd7972909ce93d6aa205f07)

## ADK WEB 的使用方式
+ 查看历史对话：点击左方panel中的 session tab
+ 汇出对话记录：
  + 透过右上角的export图标汇出（但暂时无法在gui中恢复）
  + 点击左方panel中的 eval tab -> 建立eval集 -> 将对话保存至eval集

## 影片分析功能使用指南

### 影片上传
```yaml
basketball_coach/   
├── resource/       
│   ├── videos/     <-- 在此目录上传您的视频（目录会自动创建）  
│   └── html/            
├── __init__.py        
└── agent.py                    
```

### 影片分析
在对话中，需要明确交代待分析的影片的档案名称。你可以透过提问如“目前我都上传了哪些影片”来让Agent返回档案名称。

我们支持三种分析：球队球员构成、得分、违例违规（如果没有指定的话，Agent会自动生成一个包含三样内容的概括性分析）

**注意：**目前的生成结果并不完全可靠，尤其容易混淆球员，需要人工检查。在判断得分时间戳上相对可靠。

## 战术生成功能使用指南

### 生成战术

#### 默认前置要求

需要您提供至少五位球员的基本信息（姓名、球号、位置），可以直接键入或来自球员数据库，否则Agent会辅助你完成资料的建立

#### 跳过前置要求

您可以向她明确说明“随机分配xx部分的内容”，来跳过资料设置的步骤


### 战术可视化

#### 启用可视化

在对话中，明确指出需要可视化即可

#### 结果保存
```yaml
basketball_coach/   
├── resource/       
│   ├── videos/         
│   └── html/       <-- 在此目录可以看到战术板生成结果（目录会自动创建）   
├── __init__.py        
└── agent.py                    
```



## 球员资料库维护指南

本指南将帮助您理解和维护本地存储的球员信息资料库。您的篮球教练 AI 助手能够与这个资料库交互，实现球员信息的查询、添加、更新和删除。

### 1. 资料库概览

您的球员资料库以 **JSON 文件** 的形式存储在本地文件系统中。这是一种轻量级、人类可读的数据格式，非常适合作为本地应用的数据存储。

#### 资料库文件路径：

您的球员资料库文件位于项目根目录下的 `data/` 文件夹内，文件名为 `players.json`。

例如：`your_project_folder/data/players.json`

```yaml
basketball_coach/   
├── data/       
│   └── players.json      <-- 您的资料库
├── __init__.py        
└── agent.py                    
```


### 2. 资料库结构与字段定义

`players.json` 文件是一个 JSON 数组，其中每个元素都是一个代表球员信息的 JSON 对象。每个球员对象包含以下字段：

- **player_name** (球员姓名): 字符串。这是唯一标识球员的关键字段，用于查询、更新和删除操作。请确保每个球员的姓名是唯一的。
- **player_position** (球员位置): 字符串 (例如："前锋", "中场", "后卫", "守门员")。
- **playing_style** (打球风格): 字符串 (例如："进攻型", "防守型", "组织核心", "全能型")。
- **jersey_number** (球衣号码): 整数。
- **team** (所属球队): 字符串。
- **age** (年龄): 整数。
- **nationality** (国籍): 字符串。
- **skill_rating** (技能评分): 整数或浮点数 (例如：1-100)。
- **notes** (备注): 字符串。用于记录任何额外的、灵活的球员信息，例如受伤情况、特殊成就等。

#### 示例 players.json 结构：

```json
[
    {
        "player_name": "Lionel Messi",
        "player_position": "Forward",
        "playing_style": "Playmaker",
        "jersey_number": 10,
        "team": "Inter Miami CF",
        "age": 37,
        "nationality": "Argentina",
        "skill_rating": 98,
        "notes": "Arguably the greatest player of all time."
    },
    {
        "player_name": "Cristiano Ronaldo",
        "player_position": "Forward",
        "playing_style": "Attacking",
        "jersey_number": 7,
        "team": "Al Nassr FC",
        "age": 39,
        "nationality": "Portugal",
        "skill_rating": 95,
        "notes": "Prolific goal scorer."
    }
]
```

### 3. 通过 AI 助手维护资料库（推荐方式）

强烈建议您通过与篮球教练 AI 助手进行对话来维护球员资料库。AI 助手会调用内置工具安全地执行操作，并提供友好的反馈。

#### 自然语言命令示例

##### 查询操作
- **查询所有球员**：
  - "列出所有球员"
  - "显示资料库中的所有球员"
  
- **查询特定球员**：
  - "查找 Lionel Messi 的信息"
  - "告诉我关于 Cristiano Ronaldo 的资料"

##### 添加操作
- **完整信息添加**：
  `"添加一个球员，他叫孙兴慜，位置是前锋，球衣号码7号，打球风格是进攻型，所属球队托特纳姆热刺，年龄32岁，国籍韩国，技能评分90。"`

- **不完整信息添加**（AI会引导补充）：
  `"我想添加一个新球员，名字叫李明，他是中场，年龄25岁。"`

##### 更新操作
- `"更新 Lionel Messi 的球队为巴黎圣日耳曼"`
- `"把 Cristiano Ronaldo 的年龄更新为40岁"`
- `"修改孙兴慜的备注为'亚洲足球的骄傲'"`

##### 删除操作
- `"删除球员 Cristiano Ronaldo"`
- `"从资料库中移除 Michael Jordan"`

#### 交互反馈机制
✅ **操作成功反馈**  
格式：`"[操作类型] '球员姓名' 已成功[动作]资料库。"`  
示例：`"添加 '孙兴慜' 已成功添加到资料库。"`

❌ **操作失败反馈**  
格式：`"错误: [失败原因]。[修正建议]"`  
示例：  
`"错误: 未找到球员'Cristiano Ronaldo'。请检查姓名是否正确。"`  
`"错误: 球员'李明'已存在。请使用更新操作或更改姓名。"`

---

## 待修复的问题
+ 本地球员资料库Agent的prompt及players.json键值对设置与其他功能适配性待修复
