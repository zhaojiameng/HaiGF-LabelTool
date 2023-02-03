import torch
import torch.nn as nn


class RtoS_NN(nn.Module):
    def __init__(self):
        super(RtoS_NN, self).__init__()
        self.layer1 = nn.Sequential(
            nn.Linear(4, 40),
            nn.LeakyReLU()
            )
        self.layer2 = nn.Sequential(
            nn.Linear(40, 40),
            nn.LeakyReLU()
            )
        self.layer3 = nn.Sequential(
            nn.Linear(40, 40),
            nn.LeakyReLU()
            )
        self.layer4 = nn.Sequential(
            nn.Linear(40, 4)
            )

    def forward(self, x):
        x = self.layer1(x)
        x_tmp = x
        x = self.layer2(x)
        x = self.layer3(x)
        x = x + x_tmp
        output = self.layer4(x)
        return output
# test = RtoS_NN()
# print(test)