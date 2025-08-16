import torch
import torch.nn as nn
import torch.nn.functional as F
from mercantile import feature


class MLP(nn.Module):
    def __init__(self, layer_sizes=[64,64,64,1], arl=False, dropout=0.0, bias = True):
        super().__init__()
        self.arl = arl
        if self.arl:
            self.attention = nn.Sequential(
                nn.Linear(layer_sizes[0],layer_sizes[0]),
                nn.ReLU(),
                nn.Dropout(dropout),
                nn.Linear(layer_sizes[0],layer_sizes[0])
            )

        self.layer_sizes = layer_sizes
        if len(layer_sizes) < 2:
            raise ValueError()
        self.layers = nn.ModuleList()
        self.act = nn.LeakyReLU(negative_slope=0.01, inplace=True)
        self.dropout = nn.Dropout(dropout)
        for i in range(len(layer_sizes) - 1):
            self.layers.append(nn.Linear(layer_sizes[i], layer_sizes[i + 1], bias = bias))

    def forward(self, x):
        if self.arl:
            x = x * self.attention(x)
        for layer in self.layers[:-1]:
            x = self.dropout(self.act(layer(x)))
        x = self.layers[-1](x)
        return x

class SelfAttention(nn.Module):
    def __init__(self, input_dim, da, r):
        super().__init__()
        self.ws1 = nn.Linear(input_dim, da, bias=False)
        self.ws2 = nn.Linear(da, r, bias=False)

    def forward(self, h):
        attn_mat = F.softmax(self.ws2(torch.tanh(self.ws1(h))), dim=1)
        attn_mat = attn_mat.permute(0, 2, 1)
        return attn_mat


class Sequence_Classifier(nn.Module):
    def __init__(self, class_num=1, hs=128, da=128, r=4):
        super().__init__()
        self.attention = SelfAttention(hs, da, r)
        self.classifier = MLP([hs * r, (hs * r + class_num)// 2, class_num])

    def forward(self, x):
        attn_mat = self.attention(x)
        m = torch.bmm(attn_mat, x)
        flatten = m.view(m.size()[0], -1)
        res = self.classifier(flatten)
        return res

class Vanilla(nn.Module):
    def __init__(self,state_space=26):
        super().__init__()
        self.mlp = MLP([state_space, 128, 128])
        self.softmax = nn.Softmax(dim=-1)
        self.relu = nn.LeakyReLU(negative_slope=0.01, inplace=True)
        self.actor = MLP([128,1])
        self.controller = Sequence_Classifier(1,128,128,4)
        self.softplus = nn.Softplus()



    def forward(self, order, x_state, x_order):
        order, x_state, x_order = order.float(), x_state.float(), x_order.float()
        x_order = x_order.view(x_order.shape[0],-1)
        worker = torch.concat([x_state,x_order],dim=-1)

        worker_expanded = worker.unsqueeze(1).expand(-1, order.shape[0], -1)
        order_expanded = order.unsqueeze(0).expand(x_state.shape[0], -1, -1)
        combined = torch.cat((worker_expanded, order_expanded), dim=2)
        result = combined.view(-1, combined.shape[-1])

        feature = self.mlp(result)
        q_vector = self.actor(self.relu(feature))
        q_matrix = q_vector.view(x_state.shape[0],order.shape[0])

        return self.softmax(q_matrix) + 1e-8