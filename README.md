# Scale-OSPO

**Article:** Zijian Zhao, Sen Li*, "[OSPO: One-step policy optimization for real-time order assignment on ride-sharing platforms with autonomous vehicles](https://www.sciencedirect.com/science/article/abs/pii/S0968090X26006157?dgcid=rss_sd_all)", Transportation Research Part C: Emerging Technologies, 2026



## 1. Workflow

<img src="./img/main.png" style="zoom:50%;" />

<img src="./img/network.png" style="zoom:48%;" />



## 2. Simulator

Please refer to [RS2002/OSPO: Official Repository for The Paper, One Step is Enough: Multi-Agent Reinforcement Learning based on One-Step Policy Optimization for Order Dispatch on Ride-Sharing Platforms](https://github.com/RS2002/OSPO).



## 3. How to Run

### 3.1 Pre-train

Execute the following command in the `./OSPO/pretrain` directory:

```
python train.py
```



### 3.2 Fine-tune

Execute the following command in the `./OSPO/finetune` directory:

```
python train.py --model_path <path_to_trained_model_from_pretraining>
```



## 4. Reference

```
@article{ZHAO2027106130,
title = {OSPO: One-step policy optimization for real-time order assignment on ride-sharing platforms with autonomous vehicles},
journal = {Transportation Research Part C: Emerging Technologies},
volume = {195},
pages = {106130},
year = {2027},
issn = {0968-090X},
doi = {https://doi.org/10.1016/j.trc.2026.106130},
url = {https://www.sciencedirect.com/science/article/pii/S0968090X26006157},
author = {Zijian Zhao and Sen Li},
}
```

