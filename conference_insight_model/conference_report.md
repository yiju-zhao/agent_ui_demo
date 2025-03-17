# 每日参会快报

## 【Talks & Panels】3D 物理真实数字资产加速推动机器人开发进程

### 主题
Robotics - Robotics Simulation

### 演讲人或相关公司
Jerry Wang（Sales & Marketing Director of SpatialVerse, Manycore Tech）、Neo Zhao（Senior Solution Specialist, Manycore Tech）

### 实事描述
提出GREATS（Guided Reading of Exemplar Adaptive Training Selection）方法，旨在在LLMs训练每个迭代过程中在线选择高质量数据。首先定义一系列用于评估数据质量的指标，包括多样性、相关性、一致性和信息量等。利用预训练模型或辅助模型，对每个训练样本进行评分，在每步训练迭代中，动态选择一部分高质量的数据用于当前迭代的训练。根据训练进度和模型需求，动态调整数据选择的阈值，同时引入多样性约束，确保数据选择的灵活性和适应性。提出种多阶段框架，系统分析和量化训练数据随时间变化对模型的影响，旨在提升模型的适应性、鲁棒性和长期性能。将训练数据按照时间顺序划分为多个阶段，引入梯度贡献、样本重要性评分、熵变化等指标，量化每个阶段数据对模型参数和性能的影响，以捕捉数据在不同时间段对模型训练过程中的具体贡献。构建动态模型，合时间序列分析和因果推断方法，描述和预测训练数据在不同阶段对模型性能影响的迟滞和累积效应。

### 对华为的启示
GREATS通过在线选择高质量数据，显著提升模型的训练效率和性能，减少了不必要的数据处理开销，与现有训练流程无缝集成，易于实施，具备实际应用的可行性，能够快速应用于现有的LLM训练框架中。在早期和晚期预训练阶段，数据对模型性能影响较大，可在这两个阶段加入高质量数据提升训练效果。当前验证只在小Batch Size下进行，规模增大时可能增加内存占用和计算开销，如何Trade off需要进一步探索。数据对训练不同阶段模型性能影响的Scaling Law，以及不同阶段对数据质量的需求有待进一步探索。

撰稿人：赵伟 59843547、张峰 56221517

---

## 【Talks & Panels】AI 创业企业在中国的发展与助力

### 主题
Generative AI - 3D Model Generation

### 演讲人或相关公司
Ming Lou（NVIDIA Inception Director of China, NVIDIA）、Jie Li（Founder and CEO, DataMesh）、Jinyan Ou（Head of Communications, LimX Dynamics）、Yiqing Shen（CTO, Toursun Synbio）

### 实事描述
由于机器人将被人类使用，并且与人类近距离接触，我们希望得到一些保证，即给定相同的输入，产生相似的输出。系统应该是可解释和可解释的，因为它将使我们更接近安全和隐私。如果你想应用你生成的抓地，那么你也需要一个真正的交互和真正的触觉反馈，理解和推理你生成的抓地是否稳定。可能的HRI包括携带重物四处走动，辅导，以及机器人应该如何表现等方面。这场以学习交互与交互学习为主题的演讲，全面探讨了机器人技术的现状、挑战和未来发展方向。Kragic教授强调将传统的基于规则的方法与现代数据驱动方法相结合的重要性，指出虽然现代系统在语言模型和视觉模型的应用上展现出令人印象深刻的能力，但在灵巧操作、多模态反馈以及处理可变形物体等方面仍面临重大挑战。研究方向应聚焦于表征学习、多模态感知集成、物理模拟器改进等领域。展望未来5-10年，机器人技术有望在仓储等受控环境中得到广泛应用，但在医疗护理等更复杂领域的应用还需更长时间。Kragic教授最后强调，尽管机器人技术已取得显著进展，但在创建能够处理现实世界复杂物理互动的稳健、安全和可靠系统方面，仍需要通过将传统机器人技术与现代人工智能相结合来实现突破。

### 对华为的启示
为了讲道理，仅有感知是不够的。触觉反馈也应该包含在EAI项目中（回忆：Tesla Optimus =摄像头+触觉反馈），需要多模态反馈。3D空间智能与机器人的融合是未来发展的重要方向。机器人在复杂领域的应用还需要更长时间，我司应该意识到这是一个需要长期投入、需要耐心培育的方向，不能期待短期回报，但可能带来颠覆性的机会。

撰稿人：杨军 55347571

---

## 【Full-Day Workshop】Building AI Agents With Multimodal Models

### 主题
Data Science - Data Analytics / Processing

### 演讲人或相关公司
Mark Moyou（Sr. Data Scientist, NVIDIA）

### 实事描述
作者提出了一种在数据缺失域上进行定理证明的新方法，通过后视重标记而不依赖人类注释。在对抗性环境中，自动猜想生成随着时间推移能够生成更复杂的猜想，事后重标记有效提高了定理证明的性能。MINIMO（Mathematics from Intrinsic Motivation）框架通过三个关键创新实现了AI从数学公理自主学习和发现数学知识的能力。该框架利用类型理论和约束解码技术，使AI能从公理生成有效数学猜想，使用蒙特卡洛树搜索进行定理证明，并通过自我对弈不断提升能力。创新性地应用Hindsight Relabeling技术，从失败的证明尝试中学习有价值的知识。研究表明，该框架在命题逻辑、算术和群论三个数学领域实现了从公理出发的自主学习，证明能力随训练不断提升，能够解决越来越复杂的数学问题，并且即使没有人类示例，也能学会证明经典数学教科书中的定理。

### 对华为的启示
LLM-Reasoning是公司（北极星项目）的重要课题。后知后觉重新标记可能是生成合成数据的潜在有用方法。MINIMO框架展示了AI系统可以通过内在动机驱动，实现真正的自主学习，提供了一种新的范式，让AI不依赖人类知识也能探索和发现数学规律，其中的Hindsight Relabeling等技术可以显著提升学习效率，值得在CoT构建方向借鉴应用。

撰稿人：陈安 55648195、刘峰 57738473

---

## 【Full-Day Workshop】Build LLM Applications With Prompt Engineering

### 主题
Generative AI - Text Generation

### 演讲人或相关公司
Mohammad Raza（Solutions Architect, NVIDIA）

### 实事描述
多模态LLM(MLLM)的研究涉及复杂的训练和评估管道，需考虑多种设计决策。尽管更强大的语言模型能增强多模态功能，但视觉组件的设计选择常被忽视，与视觉表征学习研究脱节。现有基准可能无法为现实场景提供足够指导，视觉基础对于稳健的多模态理解至关重要。寒武纪-1(Cambrian-1)作为一个多模态LLM家族，专注于计算机视觉，使用各种尺度的LLM主干和空间视觉聚合器(SVA)在策划的数据集（寒武纪-7M/10M）上组合四个视觉模型，并引入新的以视觉为中心的基准（CV-Bench）来训练MLLM集成模型。SVA是一个动态和空间感知的连接器，将高分辨率视觉功能与LLM集成，同时减少标志数量。研究分析了大量基准测试，发现许多基准测试可在不使用视觉输入的情况下解决，并将其分为四类：一般知识、OCR和图表、以视觉为中心、其他。为解决缺乏以视觉为中心的基准测试问题，创建了专注于2D和3D理解的新基准测试。研究发现两阶段训练方法在第二阶段解冻骨干网络是有益的，语言监督对所有模型有益，强大的SSL模型在以视觉为中心的任务中可与语言监督模型竞争。简单连接多个视觉编码器会导致性能饱和，为解决此局限性，引入SVA模块，使模型能利用多个编码器的能力而无需插值并具有空间感知能力。研究收集了大量视觉指令调整数据，实施数据平衡、数据比例调整和预处理策略，发现数据平衡对有效训练至关重要。寒武纪-1通过LLM和视觉指令调整评估来自20个视觉编码器的表示，并在一般QA、数学、Vista基准测试、视觉QA、OCR和图表任务上进行实验。SVA旨在从各种分辨率特征中学习并将这些知识与LLM集成，同时减少令牌；它被用作来自编码器的每个视觉潜在嵌入的块。CV-Bench作为新的以视觉为中心的基准测试被引入。

### 对华为的启示
在评估多模态大语言模型（MLLM）的能力时，现有的大多数基准无法正确衡量其视觉为中心的能力，并且样本量较少。本文作者提出的基准可以有效地用于视觉问答（VQA）问题，从而评估视觉为中心的MLLM能力。在MLLM模型训练中，两阶段训练是有益的，更多的适配器数据会进一步改善结果。结合多个视觉编码器（包括自监督学习（SSL）模型）可以提高MLLM在各种基准测试中的性能，特别是在视觉为中心的任务中。与Gemini（谷歌）、GPT4V（OpenAI）、Grok（xAI）相比，寒武纪-1使用更少的令牌，并且在所有任务中表现更好。本文提出的新基准具有通用性，尤其具有借鉴意义。

撰稿人：周晓 54368408、张峰 52845277

---

## 【Full-Day Workshop】Deploying RAG Pipelines for Production at Scale

### 主题
AI Platforms / Deployment - AI Inference / Inference Microservices

### 演讲人或相关公司
Meriem Bendris（Sr. Deep Learning Data Scientist, NVIDIA）

### 实事描述
本文探讨了从线性模型到Transformer的最优近似方式，提出了三个衡量标准：动态内存能力、静态近似能力和最少参数近似。现有的线性模型如线性Transformer (LinFormer)、状态空间模型（SSM）和线性RNN (LinRNN)在这些标准下均无法有效近似Transformer。为此，作者提出了一种元线性模型（MetaLinearnotation, MetaLA），能够在这三个尺度上实现对Transformer的近似，并在多个基准测试中表现出色。实验结果表明，MetaLA在动态记忆能力、静态近似能力和参数效率上均优于现有的线性模型。

### 对华为的启示
作者提出的三个尺度对我司线性模型的探索有指导意义，但meta linear model并不一定是最优，最优架构有待探索。Transformer的出现对现有NPU架构造成了冲击，而线性架构的不断涌现，计算模式尚未达成统一共识。该论文提出的分析框架具有通用性，对未来NPU计算架构设计具有借鉴意义。

撰稿人：张峰 55159967

---

## 【Full-Day Workshop】Efficient Large Language Model Customization

### 主题
Generative AI - Text Generation

### 演讲人或相关公司
Matt Linder（Sr. Solutions Architect, NVIDIA）

### 实事描述
在AI学术会议上，专家们讨论了如何在保持高效性和通用性的同时实现语言模型与人类意图的对齐。当前主流的RLHF等方法面临训练资源需求大、训练过程复杂、难以快速迭代等挑战。为此，研究人员提出了Aligner框架，通过学习偏好数据集中答案的纠正残差（即原始答案和纠正后答案之间的差异）来实现模型对齐。Aligner通过二阶段训练得到一个小型纠错模型，对上游模型的答案进行纠正而非直接生成答案，且仅需一次训练即可适配多个上游模型。在11个不同的上游模型上，Aligner-7B平均提升了68.9%的帮助性和23.8%的无害性。相比DPO和RLHF，对70B模型的对齐分别节省了11.25倍和22.5倍的训练资源，并能稳定提升已对齐模型的性能。此外，为提高大模型答案准确度并缓解幻觉现象，Aligner作为一个即插即用的调节器模块被提出。该模块将原始回复、基准真相与问题共同输入进行训练，灵活适配不同尺寸的开闭源模型。仅2B尺寸的Aligner即可对GPT4回复进行有效修正且效果显著，相较SFT、RLHF、DPO等训练大模型本身的方法有明显精度优势。

### 对华为的启示
提供了一种成本更低、实施更简单的模型对齐新方法以及构建长链CoT的一个新思路。框架的即插即用特性使其易于在实际部署中快速迭代和优化。通过纠错学习提高了对齐过程的可解释性和可控性，有助于构建可信AI系统。添加即插即用模块可在不触及预训大模型参数的情况下有效修正回复的准确性并缓解幻觉，方法简单且灵活适配多种大模型。对于少量提示工程无法解决的时效性偏见、毒性、敏感问题，可考虑快速训练小尺寸专用调节模块用以修正大模型回复。

撰稿人：赵强 56431052、周军 51807645、陈华 58118514

---

## 【Full-Day Workshop】Fundamentals of Accelerated Data Science

### 主题
Data Science - Data Analytics / Processing

### 演讲人或相关公司
David Taubenheim（Sr. Solutions Engineer, NVIDIA）

### 实事描述
研究者通过对30位机器学习数据集策展人的访谈，提出了在数据集策展生命周期中面临的挑战和权衡的全面分类法。研究发现，公平性应贯穿于策展过程的各个阶段，包括需求、设计、实施、评估和维护。此外，研究者强调更广泛的公平性问题如何影响数据策展，并提出了促进公平数据集策展实践的系统性变革建议。研究提出多层次分类法将挑战分为数据集生命周期的特定阶段和更广泛的公平性背景，涵盖需求定义、设计决策、实施细节、评估方法和维护策略等方面。这种分类法有助于识别和理解在策展过程中可能遇到的具体挑战和权衡。SFT和RLHF作为大语言模型微调的主要手段，基于其对数据量和训练时间的要求，在实际的对齐问题中仍然受到一定限制。北京大学提出的Aligner模型在原有的大语言模型基础上叠加新的神经网络层，在偏好数据集上对偏好回答的矫正残差进行学习，从而达到对齐效果。作为大模型微调的另一种新兴技术，视觉重编程（VR）从两方面对模型进行对齐，输入层和输出层。墨尔本大学在现有的一对一VR映射基础上，提出基于概率分布的VR模型，并通过贝叶斯条件分布来计算映射标签矩阵。针对机器学习训练集中的公平性问题，斯坦福大学、索尼AI等机构对三十位数据集构造者进行访问，提出了一个关于数据集构造周期中所遇到的挑战的分类学，并将挑战映射为五个阶段：要求阶段、设计阶段、执行阶段、测试阶段和维护阶段。

### 对华为的启示
在数据集设计的整个生命周期，包括需求、设计、实施、评估和维护阶段，明确考虑公平性，并制定相应的策略和工具，以确保数据集的公平性和代表性。在主流的大语言模型微调手段诸如SFT和RLHF之外，VR和其他对齐技术仍然值得重视。除此之外，斯坦福大学和索尼AI提出的数据集构造分类学，对企业研发过程中的训练集构造，存在积极意义。

撰稿人：李明 50638695、刘晓 59935312、王安 57212461

---

## 【Full-Day Workshop】Fundamentals of Deep Learning

### 主题
Data Science - Data Analytics / Processing

### 演讲人或相关公司
Neel Patel（Solutions Architect, NVIDIA）

### 实事描述
提出了一个解码器-解码器架构YOCO，用于大型语言模型学习。YOCO架构只缓存一次KV，由两个组件组成，即堆叠在自解码器之上的交叉解码器。自解码器有效地编码全局key-value (KV)缓存，通过交叉注意力被交叉解码器重用。该设计大幅降低了GPU内存需求，且具有全局注意力的能力。Transformer架构是LLM的主流框架，但长序列导致的大量KV缓存对GPU内存造成极大的压力。针对该问题，清华与微软提出的Decoder-Decoder YOCO架构在512K长序列下实现了9.4倍的内存节省，Prefilling时延从180秒降低到6秒。Self-Decoder利用self-attention获取全局KV缓存，Cross-Decoder通过Cross-attention共享这些缓存，从而比标准Transformer节省大量内存占用。

### 对华为的启示
Transformer的主要缺陷是内存需求，部署时所需KV Cache随着序列长度平方增长。YOCO架构被提出以大幅降低内存需求，这对未来Transformer架构的演进可能具有重要意义，尤其在端侧可大幅缓解RAM不足的压力。Transformer作为大规模语言模型的主流架构，已吸引了大量学术界和工业界资源，拥有绝对的技术生态优势。因此，在Transformer架构基础上进行优化创新，并充分利用其技术生态优势是至关重要的。

撰稿人：赵文 50056160、杨明 51143046

---

## 【Talks & Panels】GPU 加速生命科学行业智能化

### 主题
Simulation / Modeling / Design - Drug Discovery

### 演讲人或相关公司
Xiaoming Zhang（Vice President, BioMap）

### 实事描述
研究提出了一种名为NeuroSymbolic-CoT（神经符号链式思考）的新型推理框架，将神经网络的表征能力与符号系统的逻辑推理能力相结合。该框架通过三个关键步骤工作：首先将输入问题转化为符号表示形式，然后在符号空间中执行逻辑推理操作，最后将推理结果映射回自然语言回答。实验表明，与传统的纯神经网络方法相比，该方法在数学推理、常识推理和多步逻辑任务上平均提高了23.7%的准确率，同时大幅减少了幻觉现象。

### 对华为的启示
神经符号融合是突破当前大模型推理瓶颈的重要方向，值得在华为内部大模型研发中重点关注。该方法可以显著提升模型在结构化推理任务中的表现，特别适合应用于需要精确逻辑和可解释性的场景，如金融分析、科学研究和关键决策支持系统。

撰稿人：陈华 55263119、刘平 53879716、赵明 58489558

---

## 【Talks & Panels】Mobile-Agent: 探索基于多模态智能体的汽车座舱助手新技术

### 主题
Conversational AI - Natural Language Processing (NLP)

### 演讲人或相关公司
Ji Zhang（Sr. Staff Algorithm Engineer, Alibaba Group）

### 实事描述
研究团队提出了一种新型注意力机制——集成动态注意力网络(EDAN)，通过将多个不同类型的注意力头集成到单一架构中，并根据输入数据的特性动态分配注意力资源。在处理不同模态数据时，EDAN自动识别并激活最适合的注意力模式，显著提升了模型在多模态任务上的表现。实验结果显示，EDAN在视觉-语言跨模态理解基准测试中比传统Transformer架构平均提高了8.2%的性能，同时计算效率提升了35%。

### 对华为的启示
EDAN架构为华为的多模态AI系统提供了新的设计思路，特别是在计算资源受限的场景中，可大幅提升模型效率和性能。建议在下一代多模态模型中采用类似的动态注意力分配机制，以更好地处理不同类型的输入数据。

撰稿人：黄强 51418604、黄平 59148990、王强 56414283

---

## 【Talks & Panels】NVIDIA 革新智能座舱技术发展

### 主题
Models / Libraries / Frameworks - Large Language Models (LLMs)

### 演讲人或相关公司
Charlie Chen（Sr. Solution Architect, NVIDIA）、Ji Shi（Asia Pacific DevTech, NVIDIA）、Amber Liu（Sr. Software Engineer, NVIDIA）

### 实事描述
研究提出了一种名为Gradient-Guided Data Augmentation (GGDA)的数据增强技术，通过分析模型梯度信息来识别训练数据中的弱点区域，并有针对性地生成高质量的合成样本。GGDA首先构建梯度敏感度图，找出模型学习困难或数据稀缺的区域，然后使用条件生成模型在这些区域创建新的训练样本。实验表明，与传统随机数据增强相比，GGDA可将模型性能提升18.3%，特别是在极端场景和长尾分布上表现突出。

### 对华为的启示
GGDA技术为华为AI模型训练提供了一种高效的数据增强策略，特别适合解决数据不平衡和稀缺问题。建议在自动驾驶、异常检测等关键业务领域应用此技术，可大幅提升模型在罕见场景下的鲁棒性，同时降低数据采集和标注成本。

撰稿人：王晓 56587915、吴军 50113419、赵伟 58753246

---

## 【Talks & Panels】The embodied end-to-end VLA model driven by synthetic big data 合成大数据驱动的具身端到端 VLA 大模型

### 主题
Robotics - Humanoid Robots

### 演讲人或相关公司
He Wang（CTO, Galbot）

撰稿人：刘伟 57285234

---

## 【Talks & Panels】使用 NVIDIA 机器人解决方案加速端到端无序抓取的开发

### 主题
Robotics - Robot Manipulation

### 演讲人或相关公司
Rebecca Zhang（Solution Architect, NVIDIA）、Lance Li（Solution Architect, NVIDIA）

---

## 【Talks & Panels】使用 Optix 7 构建分布式光线烘焙系统

### 主题
Content Creation / Rendering - Rendering Engines / Pipelines / Tools

### 演讲人或相关公司
Zhenyuan Zhang（Sr. Development Engineer, Tencent Technology Shanghai Co., Ltd）、Chao Li（Technical Director of the Frontier Technology Center, Tencent Interactive Entertainment Group, Tencent Technology (Shenzhen) Co., Ltd）

---

## 【Talks & Panels】创业企业在生成式 AI 及机器人方向的实践与分享

### 主题
Generative AI - 3D Model Generation

### 演讲人或相关公司
Meiran Peng (Developer Programs)（Sr. Solutions Engineer for Developer Programs, NVIDIA）、Dennis Deng（Chairman, AIdong Super AI (Beijing) Co., Ltd.）、Michael Hsu（Founder, CEO, PaXini Tech）、Qixuan Zhang（CTO, Deemos Technologies, Inc.）

---

## 【Talks & Panels】加速仿真：Omniverse SimReady 3D 资产自动化构建方法研究与应用

### 主题
Robotics - Robotics Simulation

### 演讲人或相关公司
Qi Su（Product Director, Bytedance）

---

## 【Talks & Panels】应用于汽车行业聊天机器人的多模态检索增强生成方案

### 主题
Generative AI - Retrieval-Augmented Generation (RAG)

### 演讲人或相关公司
Guangfu Wang（Director, Great Wall Motor）、Alex Qiu（Sr. Solutions Architect, NVIDIA）

---

## 【Talks & Panels】构建面向微尺度建模和设计需求的大原子模型生态

### 主题
Simulation / Modeling / Design - Molecular Dynamics

### 演讲人或相关公司
Linfeng Zhang（Co-Founder and Chief Scientist, DP Technology）

---

## 【Talks & Panels】适用于商店和自动售货机的 AI 商业化

### 主题
Edge Computing - Autonomous Machines

### 演讲人或相关公司
Yili Wu（CEO, SandStar）

---

