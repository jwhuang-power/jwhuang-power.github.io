# AI-Workload Predictive VRM Controller：项目评估

- **评估对象**：PPT《AI-Workload Predictive VRM controller》（Shuyu Zhang，BPEC，2026-11-02，19 页）
- **整理日期**：2026-11-05
- **内容**：理论核对、数值验证、文献与专利检索、价值与可发表性、可行性、IC 实现建议、推进路线
- **说明**：内部研究笔记，已在 `_config.yml` 中排除，不会发布到网站

---

## 0. 结论摘要

1. **理论成立。** `t_pre : t_post = 1 : √2` 在“理想集总模型 + 对称容差窗”下是 min-max 最优解。相对**理想的时间最优（TOC）反应式控制**，峰值偏差的理论改善上限是 `(1+√2)² ≈ 5.83×`。这是项目最硬的卖点；PPT 目前只和 PI 控制比较。
2. **概念不新，专利很密集。** 从 2005 年起就有大量专利；学术上 Berkeley 的 Peterchev & Sanders（TPEL 2006）做过负载电流前馈。本次检索**没有找到**同时做到“预告最优轨迹 + 变换器动态 + 误差鲁棒性 + IC 实现”的同行评审论文。这是可发表的空间，但需要在 IEEE Xplore 上再确认一次（见附录 B）。
3. **价值真实，但有前提。** 最大收益在**卸载（load release）**而不是加载。前提是能拿到时序精度足够的预告信号：加载侧约 `0.1·t_pre`（本文例子约 20 ns），卸载侧约 130 ns。确定性执行的推理芯片（Groq LPU 一类）满足这个前提，通用 GPU 不一定满足。
4. **可行性。** 仿真和板级验证容易（3–6 个月）。单独为这个控制算法流片不划算，除非结合电路层面的新东西。**建议与 fast-slow 架构结合**：预告驱动慢速主级，快速辅助级吸收预测误差。

---

## 1. PPT 内容概要

| 页 | 内容 |
|---|---|
| 3 | Primarion → Infineon（2005），US 6,909,265 B2：利用时钟使能、指令等提前信号，在加载前预充电、卸载前预放电输出电容；可通过辅助电荷转移电路或直接控制主 buck 实现 |
| 4 | NVIDIA（2008），US 7,441,137 B1：GPU 根据流水线活动、空闲周期、shader 标记预测负载变化，用单比特或多比特信号通知稳压器，提前抬高或降低 Vout |
| 5 | Marvell（2015），US 9,083,229 B1：思路与 NVIDIA 类似；PPT 指出其 Vout 波形有回弹，还有改进空间 |
| 6 | NVIDIA-Groq（2024），US 2024/0176406 A1：结构类似 load line，注入预测信号 V_PRED；包含“测残余 VCORE → 校准 V_PRED 波形（硬件或软件）”的流程 |
| 7–8 | NVIDIA Groq 3 LPX 技术博客：PEP 在电流到来前提前抬高电压，减小跌落；CPS 按周期调整时钟 |
| 9 | 专利的一般思路：电压码查找表 → DAC → 低通滤波生成校正信号，时序、幅度、形状可用测量结果校准（机器学习作为可选方案） |
| 10 | PPT 认为专利的局限：几乎不讨论电感电流和变换器动态（默认电源瞬间跟随 v_ref）；没有讲如何充分利用容差窗；几乎不涉及电路实现 |
| 12–13 | 核心方法：对称容差窗下 `t_pre : t_post = 1 : √2`，`t_pre = ΔI / [S(1+√2)]`；控制流程为“预测事件 → 电荷平衡定时 → 生成 Vout 参考” |
| 15–16 | PLECS 仿真（0 → 满载约 40 A 脉冲，假设提前 1 µs 已知负载）：跌落约 −3% → 约 −1.5%，过冲约 +5.5% → 约 +0.5% |
| 18 | 待定问题：单相还是多相；电流环是否用模拟；预告 IO 用数字还是模拟；v_ref 用 DAC 还是模拟；自适应调参；先做板级还是 IC；做混合信号多相控制器还是带功率级的单相单片 |

---

## 2. 理论核对

### 2.1 推导

理想模型：电感电流斜率上限为 S，单个输出电容 C，没有 ESR/ESL，负载为理想阶跃，时刻 `t = 0`。

- 阶跃前 `t_pre` 内电容多充的电荷：`Q1 = S·t_pre²/2`，所以阶跃时刻的峰值为 `+ΔV = Q1/C`
- 阶跃后的电荷缺口：`Q2 = S·t_post²/2`，最低点为 `(Q1 − Q2)/C`
- 对称窗要求 `Q2 = 2·Q1`，因此 `t_post = √2·t_pre`；同时 `t_pre + t_post = ΔI/S` ✓
- 最优偏差：`ΔV* = [ΔI²/(2SC)] / (1+√2)²`

**最优性。** 设阶跃时刻电感电流为 `I_a`。要让 Q1 最小，应在阶跃前以最大斜率爬升，得到 `Q1 = I_a²/(2S)`；要让 Q2 最小，阶跃后也应以最大斜率爬升，得到 `Q2 = (ΔI − I_a)²/(2S)`。在 `I_a` 上最小化 `max(Q1, Q2 − Q1)`，最优点满足 `Q2 = 2Q1`。所以 PPT 的结果就是 min-max 最优解。

**相对理想 TOC 的改善。** 无预告时 `ΔV_TOC = ΔI²/(2SC)`，因此 `ΔV_TOC / ΔV* = (1+√2)² ≈ 5.83`。

**一般化（不对称窗口 `+V_hi / −V_lo`，例如有 AVP 时）：**

```
t_post / t_pre = √(1 + V_lo/V_hi)
```

`V_lo = V_hi` 时退化为 √2。GPU 的实际窗口几乎都不对称，论文应该给出这个一般式。

### 2.2 数值例子（VPD 量级）

参数：6 V → 0.8 V，40 相，每相 L = 100 nH，等效 C = 15 mF，ΔI = 1000 A。

| | S | t_pre | t_post | 理想 TOC 偏差 | 有预告的最优偏差 |
|---|---|---|---|---|---|
| 加载 | `N(Vin−Vo)/L` = 2080 A/µs | 199 ns | 282 ns | 16.0 mV | 2.7 mV |
| **卸载** | `N·Vo/L` = **320 A/µs** | **1.29 µs** | 1.83 µs | **104.2 mV** | 17.9 mV |

### 2.3 PPT 没写的三个推论

**推论一：S 必须按方向分开。** 低占空比时 `S_up/S_dn ≈ 6.5`（12 V 输入时约 14）。PPT 全程只用一个 S。另外，加载后 Q3 回补段走的是慢的下降斜率，实际 settling 比图上画的长得多。

**推论二：价值主要在卸载。** 卸载偏差是加载的 6.5 倍，本来就是决定 C_out 的那一项。卸载的 `t_pre` 约 1.3 µs，对预告时序精度的要求也宽松 6.5 倍。PLECS 结果与此一致：过冲的改善（约 +5.5% → 约 +0.5%）远大于跌落的改善（约 −3% → 约 −1.5%）。**建议把主打方向改为“预告卸载”。**

**推论三：对预测误差敏感，而且风险不对称。** 下表是加载情形，以 ΔV* 为单位。假设负载一旦到达（或 `t = 0` 时负载未到而 Vout 已高于标称值），立即交给理想的非线性（TOC）反馈。

| 误差 | 结果 |
|---|---|
| 负载提前 20 / 50 / 100 ns | 跌落 1.48 / 2.20 / 3.41 倍 ΔV*（仍好于无预告的 5.83 倍） |
| 负载推迟 20 / 50 / 100 ns | 过冲 1.20 / 1.49 / 1.96 倍 ΔV* |
| ΔI 低估 20% / 50% | 跌落 2.59 / 5.87 倍 ΔV* |
| ΔI 高估（负载到达即交接） | 基本无害（过冲 1.00 倍 ΔV*） |
| **误报：加载没有发生** | **过冲 7.5 倍 ΔV*（= 1 + S_up/S_dn）** |
| 误报：卸载没有发生 | 仅 1.15 倍（= 1 + S_dn/S_up） |

**设计准则：** 加载侧的时序宁可偏晚、幅度宁可偏高；卸载侧可以激进。即使提前 100 ns，结果仍好于无预告，前提是负载到达后能立刻交给非线性反馈。这张表本身就可以成为论文的一节。

---

## 3. PPT 需要补强的地方（审稿人一定会问）

1. **对照基线太弱。** 和 PI 加电流环比较，改善被夸大了。应该和 TOC/电容电荷平衡控制、minimum-deviation 控制、商用控制器的全相导通瞬态模式、TLVR 比较。建议报告归一化指标 `η = ΔV / [ΔI²/(2SC)]`：TOC 对应 1，有预告的理论最优对应 0.172。
2. **通过 v_ref 注入是间接控制。** v_ref 阶跃要先经过 PI 才变成电流指令，iL 不会走最大斜率轨迹，积分器还会和前馈互相干扰；Marvell 波形的回弹很可能就是这个原因。应该做**二自由度（2-DOF）控制**：同时给出前馈电流 `i_ff(t)`（或直接给出相位导通时序）和与之一致的参考轨迹 `v_ref(t)`，反馈环只负责修正误差。
3. **只用一个 C 建模。** 没有 ESR/ESL，也没有封装、板级的多级 PDN。µs 尺度上 VRM 能“看到”的有效电容比标称值小。第一跌落（die 与封装谐振，约 100 MHz 量级）VRM 管不到，只能靠提前抬高的那 +ΔV 作为余量。需要在 PDN 模型上验证。
4. **没有和 AVP/load-line 比较。** AI GPU 的 VR 基本都带 load line，load line 本身就在利用容差窗。必须证明预告控制在 AVP 之上还有增量。
5. **“提前 1 µs 知道”只是假设。** 需要交代预告信号的来源和链路延迟。SVID/AVSBus/PMBus 太慢，抖动也大。加载侧需要约 `0.1·t_pre` 的时序精度。
6. **第 18 页的“自适应调参”已被专利覆盖。** Groq 专利（第 6 页）写了“测残余 VCORE → 校准 V_PRED（硬件或软件）”，第 9 页还提到机器学习。要做自适应，必须讲清楚具体机制和收敛性，并与现有专利区分。
7. **小错误。** 第 5 页 “Marvel” 应为 “Marvell”，“US 9,083.229” 应为 “US 9,083,229”。先前技术部分漏掉了第 4 节列出的多篇专利。

---

## 4. 文献与专利检索

### 4.1 专利（概念层面基本已被占据）

PPT 已列出：

| 专利 | 申请人 / 年份 | 要点 |
|---|---|---|
| US 6,909,265 B2 | Primarion → Infineon，2005 | 预充电 / 预放电输出电容 |
| US 7,441,137 B1 | NVIDIA，2008 | GPU 预告，提前调整 Vout |
| US 9,083,229 B1 | Marvell，2015 | 瞬态预测与补偿 |
| US 2024/0176406 A1 | NVIDIA-Groq，2024 | V_PRED 注入 + 校准 |

本次检索补充（PPT 未列出）：

| 专利 | 要点 |
|---|---|
| [US 7,421,604](https://patents.google.com/patent/US7421604) | 利用前馈负载信息的电压调节，处理器提前告警，可减小负载电容 |
| [US 9,645,626](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9645626) | 基于瞬态负载预测的供电电压控制 |
| [US 10,496,115](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10496115) | 带预测性加载的快速瞬态稳压器（提前用电流沉拉载） |
| [US 11,204,766](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11204766) | 主动式 di/dt 跌落抑制 |
| [US 11,557,967](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11557967) | 针对周期性负载的自适应前馈补偿（与本项目“自适应调参”最接近） |
| [US 12,308,740](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12308740) | 提前几十 ns 预测负载，提升 VR 响应（VR turbo） |
| [US 12,547,236](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12547236) | 按工作负载调整 VR 的 load line、设定电压、相数 |

### 4.2 学术论文

- **最接近：** A. V. Peterchev, S. R. Sanders, *Load-line regulation with estimated load-current feedforward: application to microprocessor voltage regulation modules*, IEEE TPEL, 2006（[链接](https://scholars.duke.edu/publication/792978)）。用的是估计出来的负载电流而不是预告，但审稿人一定会拿它来比较。同组还有 PESC 2004 的陶瓷电容 VRM 负载电流前馈工作。
- **反应式最优控制：** 电容电荷平衡 / 最短时间控制（[Meyer, Zhang, Liu, *A Practical Minimum Time Control Method for Buck Converters Based on Capacitor Charge Balance*](https://ieeexplore.ieee.org/document/4522693/)）；多相最短时间控制（[UPM, 2014](https://oa.upm.es/26227/1/INVE_MEM_2014_163030.pdf)）；Prodić 组的 minimum-deviation 控制。`1:√2` 正是这类方法加上“预告”的自然推广，需要引用并说明差异。
- **体系结构侧（改造负载本身，与本项目互补）：** [SparseDroop, JLPEA 2026](https://doi.org/10.3390/jlpea16010002)（DNN 加速器上的电流整形）；Reddi 等 HPCA 2009（voltage emergency prediction）、Leng 等 HPCA 2015（GPU voltage noise）——这两篇凭记忆列出，本次未核实。
- **AI 负载特性：** [AI Load Dynamics — A Power Electronics Perspective, arXiv 2502.01647](https://arxiv.org/abs/2502.01647)。提出可用 GPU 调度信号做预测控制，但没有实现。
- **LDO 方向：** [Hash-based predictive digital-assisted LDO, JSSC 2020](https://www.researchgate.net/publication/343806446_A_Fast-Transient_500-mA_Digitally_Assisted_Analog_LDO_With_30-mu_VmA_Load_Regulation_and_00073-ps_FoM_in_65-nm_CMOS)。预测基于输出电压历史，而不是负载侧的预告。

### 4.3 结论与局限

- 本次检索**没有找到**同时做到“有预告时的最优轨迹 + 变换器动态 + 误差鲁棒性 + IC 实现”的同行评审论文。
- 检索局限：没有 IEEE Xplore 全文检索权限；NVIDIA LPX 博客在当时的会话网络中无法访问，PEP 细节以 PPT 截图为准；部分论文凭记忆列出（已标注）。

---

## 5. 价值与可发表性

**价值杠杆：** 偏差规格不变时，理想情况下可以：

- 把 C_out 减到约 1/5.8（偏差与 C 成反比），对背面放不下大电容的 VPD 尤其有意义；
- 或者把 L 增大约 5.8 倍（纹波更小、开关频率更低、效率更高）；
- 或者把省下的偏差换成更低的 Vmin 余量：电压降 1% 大约省 2% 动态功耗。

一句话：**用预告时间换 L·C。**

**前提：** 必须有高质量的预告信号。确定性执行的推理芯片（Groq LPU）、编译期静态调度的加速器、集合通信和层边界这类可预测事件满足前提；通用 GPU 的细粒度负载存疑。学术组拿不到真实芯片的预告信号，因此应该用真实 AI 负载电流波形，加上统计误差模型（时序抖动 σ、幅度误差、漏报率、误报率），画出“性能随预告质量变化”的曲线。这比“假设完美预告”有说服力得多。

**投稿方向：**

- 理论 + 板级实验：APEC / ECCE → TPEL / JESTPE。可行性最高。
- ISSCC / JSSC / CICC / VLSI：需要电路层面的新意。“控制算法跑在普通 buck 上”很难进。

---

## 6. 可行性与工作量

| 阶段 | 内容 | 难度与周期 |
|---|---|---|
| 理论与仿真 | 不对称斜率与窗口、PDN 模型、误差界、与 TOC 基线对比 | 低，1–2 个月 |
| 板级验证 | FPGA + 4–8 相 DrMOS + 快速可编程负载 | 中，3–6 个月 |
| IC | 见第 7 节 | 高，12–18 个月 |

**板级陷阱：** 负载和预告如果由同一个 FPGA 产生，时序天然完美，结果会“好得不真实”。必须主动注入预告误差（时序、幅度、误报、漏报）。

---

## 7. IC 实现建议

### 7.1 要不要做 IC

控制律本身用数字多相控制器的固件或 RTL 就能实现（商用数字多相控制器就是这样做的）。做 IC 的理由必须来自电路层面：

- ns 级时序对齐；
- 允许全相同时导通的调制器；
- 快速残差检测（用于交接和自适应）；
- 低延迟、确定性的预告接口。

### 7.2 架构

```
AI 芯片 ──数字预告 {ΔI 码, 方向, 事件 ID, 发生时刻 T_evt} + 共享参考时钟──► 接收与时间基准（高速计数器 / DLL）
                                                                              │
   Vin, Vo, 工作相数 N, L 估计值 ──► 查表算出 t_pre / t_post / T_delay ◄────────┘
                                          │
   时域执行器：在 T_evt − t_pre 强制全相导通，t_post 后交还 ──┐
   前馈 i_ff(t)（电流 DAC 注入 i_ref）+ 一致的参考 v_ref(t) ─┴─► 模拟电流内环（允许相位重叠）──► N 相功率级
   实际负载检测（dv/dt 或电容电流比较器）──► 立即交给非线性反馈 + 记录误差 ──► 迭代学习修正表（按事件 ID）
   安全：取消（abort）引脚、加载误报时的 OVP 钳位
```

### 7.3 逐条回答第 18 页的问题

1. **单相还是多相：多相，至少 4 相。** 最优轨迹依赖全相同时导通；pre-slew 期间的多相均流本身也是新问题。单相在 40 A 下体现不出这些核心物理。
2. **电流环：同意用模拟。** 但调制器必须允许相位重叠，可以用 COT 或带瞬态强制导通的峰值电流模式。否则 S 达不到 `N(Vin−Vo)/L`，整套理论的前提就不成立。
3. **预告接口：数字，带时间戳，与芯片共享参考时钟。** 只要消息提前送达，链路延迟就不影响时序精度，精度只取决于共享时钟。Groq 的 plesiosynchronous 时钟起的正是这个作用。模拟 V_PRED 注入（Groq 专利的做法）可以作为对照组。
4. **v_ref 用 DAC 还是模拟：两者都不是首选。** 建议用时域执行：由计数器直接决定强制全相导通和交还的时刻，再用一个小电流 DAC 往 i_ref 注入前馈（2-DOF）。DAC → LPF 的方案会把 `t_pre` 量级（约 200 ns）的边沿吃掉。如果一定要用 DAC，需要电流舵型、建立时间 < 10 ns。
5. **自适应：迭代学习控制（ILC）。** AI 负载高度重复（每层、每个 token 跑同样的 kernel 序列），天然适合 ILC。按事件 ID 维护一张修正表，用两个快速窗口比较器（或小型 flash ADC）测残余峰值，用 sign-sign LMS 更新时序偏移、ΔI 增益和 S 估计。这比“机器学习”更容易证明收敛，面积也更小，但要与 US 11,557,967 讲清楚区别。
6. **安全机制：** abort/cancel 引脚；加载误报时的 OVP 钳位（误报代价为 7.5 倍 ΔV*）；实际负载到达即交给非线性反馈。
7. **先板级还是先 IC：先板级。** 用 3–6 个月验证理论和鲁棒性，产出 APEC 论文或 TPEL letter，再决定是否流片。
8. **带功率级的单片，还是混合信号控制器：** 学术上推荐 **4 相集成功率级 + 片上可编程负载 + 预告端口**，工艺用 180nm BCD。片上负载可以做出 ns 级边沿，并精确注入预告误差，这是板级做不到、也是 ISSCC 类测量需要的。纯控制器 IC（驱动外部 DrMOS）的工业相关性更高，但电路新意少，数字部分工作量大。

### 7.4 最推荐的差异化方向：与 fast-slow 架构结合

- 预告驱动**慢速多相主级**走最优轨迹，弥补慢级带宽不足；
- **快速辅助级**只负责吸收预测误差和第一、第二跌落。

第 2.3 节说明，这个方案的弱点正是对预测误差敏感，而快速级恰好补上这一块。这个组合在已知专利里没有见到，电路层面的故事也立得住。

---

## 8. 推进路线与决策点

1. **2 周内：** 在 IEEE Xplore 上查新（关键词见附录 B），补全先前技术；把 PPT 的核心主张改为“5.83 倍最优界 + 鲁棒性 + 实现”。
2. **1–2 个月：** 完成理论推导（不对称斜率与窗口、PDN、误差界），做与 TOC 基线对比的仿真。
3. **3–6 个月：** 板级验证（含误差注入），产出 APEC 论文或 TPEL letter。
4. **决策点：** 在真实误差模型下，如果相对 TOC 的改善**不到 2 倍**，不流片；达到 **2–3 倍以上**，再推进 IC，并与 fast-slow 架构结合。

---

## 附录 A：数值验证脚本

理想集总模型：iL 斜率受限（S_up / S_dn），单个 C，无 ESR/ESL，理想负载阶跃。按计划以 S_up 提前爬升；负载一旦到达（或 `t = 0` 时负载未到而 Vout 已高于标称值），交给理想的时间最优（bang-bang、不对称斜率）反馈。

```python
import numpy as np

def sim(dI, S_up, S_dn, C, t_pre, delta=0.0, dI_true=None, dt=2e-10, T=6e-6):
    dI_true = dI if dI_true is None else dI_true
    iL = v = 0.0; vmax = vmin = 0.0; mode = 'pre'
    for tk in np.arange(-t_pre, T, dt):
        i_load = dI_true if tk >= delta else 0.0
        if mode == 'pre' and (tk >= delta or iL >= dI or (tk > 0 and v > 0)):
            mode = 'fb'
        if mode == 'pre':
            diL = S_up * dt
        else:  # time-optimal switching surface
            e = iL - i_load
            if e > 0:
                diL = -S_dn * dt if v + e**2 / (2 * S_dn) / C > 0 else S_up * dt
            else:
                diL = S_up * dt if v - e**2 / (2 * S_up) / C < 0 else -S_dn * dt
        iL += diL; v += (iL - i_load) * dt / C
        vmax, vmin = max(vmax, v), min(vmin, v)
    return vmax, vmin

Vin, Vo, L, N, C, dI = 6.0, 0.8, 100e-9, 40, 15e-3, 1000.0
S_up, S_dn = N * (Vin - Vo) / L, N * Vo / L
g = (1 + np.sqrt(2))**2
print(f"S_up={S_up/1e6:.0f} A/us, S_dn={S_dn/1e6:.0f} A/us, S_up/S_dn={S_up/S_dn:.1f}, gain={g:.2f}x")
for name, S in [('step-up  ', S_up), ('step-down', S_dn)]:
    tr = dI / S; tp = tr / (1 + np.sqrt(2)); dv0 = dI**2 / (2 * S * C)
    print(f"{name}: t_pre={tp*1e9:5.0f} ns  t_post={np.sqrt(2)*tp*1e9:5.0f} ns  "
          f"dV_TOC={dv0*1e3:6.1f} mV  dV_preview={dv0/g*1e3:5.1f} mV")

tp = dI / S_up / (1 + np.sqrt(2)); dvs = dI**2 / (2 * S_up * C) / g
print("\nStep-up sensitivity (units of optimal dV*):")
for f in [-0.5, -0.25, -0.1, 0, 0.1, 0.25, 0.5]:
    a, b = sim(dI, S_up, S_dn, C, tp, delta=f * tp)
    print(f"  timing {f:+.2f}*t_pre ({f*tp*1e9:+4.0f} ns): Vmax={a/dvs:5.2f}  Vmin={b/dvs:6.2f}")
for k in [0.5, 0.8, 1.2, 1.5]:
    a, b = sim(dI, S_up, S_dn, C, tp, dI_true=k * dI)
    print(f"  amplitude dI_true={k:.1f}*dI_pred: Vmax={a/dvs:5.2f}  Vmin={b/dvs:6.2f}")
a, b = sim(dI, S_up, S_dn, C, tp, delta=1.0)
print(f"  false positive (no load): Vmax={a/dvs:5.2f}  (theory 1+S_up/S_dn={1+S_up/S_dn:.2f})")
print(f"  step-down false positive (theory): {1+S_dn/S_up:.2f} x dV*_down")
```

运行输出：

```
S_up=2080 A/us, S_dn=320 A/us, S_up/S_dn=6.5, gain=5.83x
step-up  : t_pre=  199 ns  t_post=  282 ns  dV_TOC=  16.0 mV  dV_preview=  2.7 mV
step-down: t_pre= 1294 ns  t_post= 1831 ns  dV_TOC= 104.2 mV  dV_preview= 17.9 mV

Step-up sensitivity (units of optimal dV*):
  timing -0.50*t_pre (-100 ns): Vmax= 0.25  Vmin= -3.41
  timing -0.25*t_pre ( -50 ns): Vmax= 0.56  Vmin= -2.20
  timing -0.10*t_pre ( -20 ns): Vmax= 0.81  Vmin= -1.48
  timing +0.00*t_pre (  +0 ns): Vmax= 1.00  Vmin= -1.00
  timing +0.10*t_pre ( +20 ns): Vmax= 1.20  Vmin= -0.84
  timing +0.25*t_pre ( +50 ns): Vmax= 1.49  Vmin= -0.62
  timing +0.50*t_pre (+100 ns): Vmax= 1.96  Vmin= -0.26
  amplitude dI_true=0.5*dI_pred: Vmax= 1.00  Vmin= -0.00
  amplitude dI_true=0.8*dI_pred: Vmax= 1.00  Vmin= -0.00
  amplitude dI_true=1.2*dI_pred: Vmax= 1.00  Vmin= -2.59
  amplitude dI_true=1.5*dI_pred: Vmax= 1.00  Vmin= -5.87
  false positive (no load): Vmax= 7.50  (theory 1+S_up/S_dn=7.50)
  step-down false positive (theory): 1.15 x dV*_down
```

**模型局限：** 没有 ESR/ESL 和多级 PDN；假设开关频率无限高（每相可随时导通）；负载为理想阶跃；交接后的反馈是理想 TOC。实际结果会比表中差，需要在 PLECS 中用完整 PDN 模型复核。

---

## 附录 B：待核实事项

1. **IEEE Xplore 查新**，范围 APEC / ECCE / TPEL / JESTPE / JSSC / ISSCC / CICC / VLSI，2023–2026。建议关键词：
   - "load current feedforward" + "voltage regulator"
   - "preview control" + "buck converter"
   - "load step anticipation" / "load transient prediction"
   - "workload-aware voltage regulator"
   - "pre-charge" / "pre-positioning" + "charge balance"
2. **NVIDIA Groq 3 LPX 博客**（[链接](https://developer.nvidia.com/blog/how-nvidia-groq-3-lpx-deterministic-execution-drives-power-efficient-high-interactivity-inference-on-nvidia-vera-rubin)）：确认 PEP 的提前量、电压校正幅度、VR 位置（片上还是片外）和 guardband 收益数字。
3. **凭记忆列出、尚未核实的论文**：Reddi et al., HPCA 2009；Leng et al., HPCA 2015；Prodić 组的 minimum-deviation 控制器。
4. **专利细节**：上表专利只读了标题和摘要级信息，引用前需读权利要求，特别是 US 11,557,967 和 US 2024/0176406 A1 与自适应校准的重叠范围。
