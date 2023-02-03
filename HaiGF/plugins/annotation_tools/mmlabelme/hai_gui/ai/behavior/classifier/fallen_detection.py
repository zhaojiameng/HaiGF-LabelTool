"""
1.	基于人体比例的检测，长宽比，上半身和下半身所在的区域比例。
2.	跌倒时速度较快，且有中心下降的趋势。
3.	跌倒后颈部关节点的纵坐标是否大于阈值、肩部和腰部关节点的相对位置。可能检测不到关键点啊。脚肩部的关节点的纵坐标差应该小于阈值。
"""
import os, sys
from collections import deque
import numpy as np
import time
from copy import deepcopy
# import ntplib
import warnings
import damei as dm


class NtpTime(object):
    def __init__(self, ntp_server_url=None):
        """
            通过ntp server获取网络时间
            :param ntp_server_url: 传入的服务器的地址
            :return: time.strftime()格式化后的时间和日期
            """
        self.ntp_server_url = ntp_server_url if ntp_server_url else 'ntp5.aliyun.com'
        self.ntp_client = ntplib.NTPClient()
        self.source = 'local'

    def __call__(self, format_time=False):
        if self.source == 'local':
            return time.time()
        else:
            return self.gettime_from_aliyun(format_time)

    def gettime_from_aliyun(self, format_time):
        ntp_stats = self.ntp_client.request(self.ntp_server_url)
        if format_time:
            fmt_time = time.strftime('%X', time.localtime(ntp_stats.tx_time))
            fmt_date = time.strftime('%Y-%m-%d', time.localtime(ntp_stats.tx_time))
            return fmt_time, fmt_date
        else:
            return ntp_stats.tx_time


class SmoothAndDuration(object):
    """对状态进行平滑，检测各个状态的持续时间"""
    def __init__(self, names, bs=1):
        """
        bs: batch_size 一次性检测多少张图
        names: 所有状态的名称
        """
        self.names = names
        self.ques = [deque(maxlen=100) for _ in range(bs)]  # bs个流，每个流最多能同时跟踪100人的tid
        self.topx = 2  # 转换波函数的时候，转换前topx个概率最大的类别
        self.ntp_time = NtpTime()

    def __call__(self, status_ret):

        ret14 = [None] * len(status_ret)
        for i in range(len(status_ret)):
            bs_que = self.ques[i]  # 第i个流对应的que
            exists_tids = [list(x.keys())[0] for x in self.ques[i]]  # """读取当前队列已经存在的tid"""

            single_ret = status_ret[i]  # [num_obj, 13]
            if single_ret is None:
                continue  # ret14本来就是None

            ctids, cstatus_idxes, cstatus_names, cstatus_scores = self.read_tid_status_score_for_single_ret(single_ret)

            # print(f'exists tids: {exists_tids}')
            # print(f'tids: {ctids}')
            # 对每个不存在的tid，就append一个，存在的就叠加
            """这一段是更新波函数，获取持续时间的代码"""
            for j, tid in enumerate(ctids):
                # 读取current psi: ndarray (len(names), )  概率最高前topx个状态对应的索引有值，其余为0
                cpsi = self.cstat2psi(cstatus_idxes[j], cstatus_names[j], cstatus_scores[j], topx=self.topx)
                if cpsi is None:  # 由于cpsi是None, 后续又用那啥处理，会导致遗漏的某帧的状态继承的前一帧的状态
                    continue
                cpsi = self.psi_normlize(cpsi)  # 波函数归一化
                if tid not in exists_tids:  # 添加新的嘛
                    if tid == 0:  #
                        continue
                    timee = self.ntp_time()
                    # 很奇怪，直接写成for循环取时间，时间会不对
                    # t0 = np.array([self.ntp_time() for _ in range(len(self.names))], dtype=np.float32)
                    t0 = np.array([timee]*len(self.names))
                    # print(f'初始化的t0: {timee} {t0[0]} {self.ntp_time()}')
                    duration = np.zeros_like(t0)
                    que_data = {tid: [cpsi, deepcopy(t0), duration]}
                    # self.ques[i].append([tid, cpsi, t0])
                    self.ques[i].append(que_data)
                else:  # tid存在, 波函数叠加
                    # print(f'xdd tid: {tid}: {len(self.ques[i])} {self.ques[i]}')
                    prev_psi, t0, pduration = self.read_from_que(self.ques[i], tid)
                    # TODO: previous psi含时相位因子还没加
                    # print(f'old_psi : {prev_psi}')
                    new_psi, new_t0 = self.superposition(cpsi, prev_psi, t0)
                    # print(f'new_psi : {new_psi}')
                    timee = self.ntp_time()
                    ctt = np.array([timee]*len(self.names))
                    duration = ctt - new_t0
                    # print(f'duration: {duration}\n')
                    new_que_data = {tid: [new_psi, deepcopy(new_t0), duration]}
                    # 根据当天tid获取到队列的索引
                    cque_idx = [iddx for iddx, x in enumerate(self.ques[i]) if tid in x.keys()]
                    # print(f'cque_idx: {cque_idx}')
                    assert len(cque_idx) == 1
                    self.ques[i][cque_idx[0]] = new_que_data

            """这一段是把根据当前的波函数更新ret的代码, [num_obj]"""
            duration_ret = np.zeros((len(single_ret), 1), dtype=object)  # [num_obj, 1]
            for j, target in enumerate(single_ret):
                tid = single_ret[j, 5]
                psi, _, duration = self.read_from_que(self.ques[i], tid)
                if psi is not None:  # 不更新
                    status_idx, status_name, status_score, duration = self.psi2status(psi, duration)  # 读取并重新排序
                    single_ret[j, 10] = status_idx
                    single_ret[j, 11] = status_name
                    single_ret[j, 12] = status_score
                else:
                    duration = np.zeros(len(self.names))
                # print(f'psi: {psi} \ndur: {duration}')
                duration_ret[j, 0] = duration
            # print(duration_ret.shape)

            concated_ret = np.concatenate((single_ret, duration_ret), axis=1)
            ret14[i] = concated_ret
            # time.sleep(2)
            # print(ret14[i])
        return ret14

    def superposition(self, cpsi, ppsi, pt0):
        r"""叠加 \psi=Norm(c1*\phi_0+c2*\phi_1)
        cpsi: current psi, ndarray [len(names, )]
        ppsi: previous psi, ndarray [len(names, )]
        pt0: previous t0
        :return
            new psi
        """
        ppsi[cpsi == 0] = 0  # 熔断
        new_cpsi = cpsi + ppsi  # 叠加
        new_cpsi = self.psi_normlize(new_cpsi)  # 归一化

        # 更新时间
        new_t0 = deepcopy(pt0)
        new_t0[cpsi == 0] = self.ntp_time()  # 时间重置

        return new_cpsi, new_t0

    def psi_normlize(self, psi):
        """传入波函数，归一化: 模方的和为1"""
        norm = np.power(psi, 2)  # 模方
        norm_normed = norm / np.sum(norm)
        psi = np.sqrt(norm_normed)
        return psi

    def read_from_que(self, que, tid):
        """从队列中，根据tid，读取psi和t0"""
        # print(que)
        flag = 0
        for x in que:  # x是dict, 如果队列是空或者没找到
            if tid in x.keys():
                flag = 1
                psi, t0, duration = x[tid]
                return psi, t0, duration
        if flag == 0:
            warnings.warn(f'从que中未读取到psi, t0和duration')
        return None, None, None

    def psi2status(self, psi, duration):
        """根据波函数返回status"""
        status_idx = np.argsort(psi)[::-1]  # 从大到小
        status_name = np.array([self.names[x] for x in status_idx])
        status_score = np.array([psi[x] for x in status_idx])
        new_duration = np.array([duration[x] for x in status_idx])
        # print(psi)
        # print(status_idx, status_name, status_score)
        return status_idx, status_name, status_score, new_duration

    def cstat2psi(self, cstatus_idx, cstatus_name, cstatus_score, topx, use_score=True):
        """current status转换为波函数，波函数是离散的，长度与状态类别长度相等"""
        # 现在的实现的不使用分数，直接对topx进行排序，按照y=kx+b采样其的分
        # TODO: 如果分类分数可靠，采用分数转换psi更合
        psi = np.zeros(len(self.names), dtype=np.float32)
        # print(cstatus_idx, cstatus_name, cstatus_score)
        if cstatus_idx is None:
            return None
        idx_topx = cstatus_idx[:topx]
        if use_score:
            psi[idx_topx] = cstatus_score[:topx]
        else:
            pt1, pt2 = [0, 1], [topx, 0]
            k = (pt2[1]-pt1[1]) / (pt2[0]-pt1[0])  # (y2-y1)/(x1-x2)
            b = 1
            score_topx = [k*x+b for x in range(topx)]  # 按y=-kx+b直线来取的分数
            psi[idx_topx] = score_topx
        # print(cstatus_name[0:2], cstatus_idx, cstatus_score, psi)
        # psi = np.zeros()
        return psi

    def read_tid_status_score_for_single_ret(self, single_ret):
        """单图的结果，读取所有tid，所有状态的idx names和分数"""
        l = len(single_ret)
        ctids = [None] * l
        cstatus_idxes = [None] * l
        csatus_names = [None] * l
        cstatus_scores = [None] * l
        for i, ret in enumerate(single_ret):
            ctids[i] = ret[5]
            cstatus_idxes[i] = ret[10]
            csatus_names[i] = ret[11]
            cstatus_scores[i] = ret[12]
        return ctids, cstatus_idxes, csatus_names, cstatus_scores

    # def get_time(self):
        # return strftime('%X', localtime(ntp_stats.tx_time))


class AuxiliaryDetection(object):
    """辅助检测器，调用跌倒检测，躺着检测，起床检测算法进行检测"""
    def __init__(self, cfg):
        """cfg是与resnet50共用的cfg"""
        self.cfg = cfg
        self.que = deque(maxlen=2)

        self.sitting_model = SittingDetection()
        self.fallen_model = FallenDetection()
        self.lying_model = LyingDetection(self.cfg.bed_area, self.cfg.lying_iou_thresh)
        self.getup_model = GetUpDetection()

        self.que = deque(maxlen=2)

    def fallen_det(self, bs, bbox, tid, trace, kps, kp_score):
        last_rets = self.que[0]
        return self.fallen_model(bs, bbox, tid, trace, kps, kp_score, last_rets)

    def lying_det(self, bs, target_info, is_fallen=False):
        is_lying, meta = self.lying_model.a_bed_under_person(target_info, is_fallen)
        # iou, dis, person_on_bed, ben_name, bed_bbox = meta
        return is_lying, meta

    def getup_det(self, bs, target_info, is_lying=False, lying_meta=None):
        is_getup, meta = self.getup_model.iou_reduced(bs, target_info, is_lying, lying_meta, last_rets=self.que[0])
        return is_getup, meta

    def sitting_det(self, bs, target_info, way='sitting2sitting'):
        if way == 'sitting2sitting':
            is_sitting, meta = self.sitting_model.second_judge_sitting(bs, target_info)
        elif way == 'jumping2sitting':
            is_sitting, meta = self.sitting_model.jumping2sitting(bs, target_info)
        else:
            raise NotImplementedError(f'way: {way}')
        return is_sitting, meta

    def push(self, rets):
        """
        rets: list len bs, 每个元素是[n, 13], n个目标，
        13: xyxy, cls, tid, trace, kps, kpss, pro_s, status_idx, status_name, status_score
        """
        # print('\nxxx push')
        self.que.append(rets)


class BaseClass(object):
    """基础类，各种函数"""
    def __init__(self, print_info=True):
        self.ntp_time = NtpTime()
        self.print_info = print_info

    def read_target_info(self, rets, bs, tid):
        """从rets中根据bs和tid读取目标的信息"""
        ret = rets[bs]
        target = [x for x in ret if x[5] == tid]
        assert len(target) == 1, f'根据bs: {bs}和tid: {tid} 读取到多条信息: {target}'
        target = target[0]
        return target

    def bbox1_on_bbox2(self, bbox1, bbox2):
        """bbox1在bbox2之上，注意y轴是越向下越大
        - by1 min 小于 by2 max
        - by1 max 在   by2 min和by2 max之间
        """
        by1min = bbox1[1]
        by1max = bbox1[3]
        by2min = bbox2[1]
        by2max = bbox2[3]
        if by1min < by2max and (by2min < by1max < by2max):
            return True
        return False

    def bbox_distance(self, bbox1, bbox2):
        bbox1 = dm.general.xyxy2xywh(bbox1)
        bbox2 = dm.general.xyxy2xywh(bbox2)
        return np.linalg.norm(bbox2[:2]-bbox1[:1])

    def get_kp_xy_scores(self, kps, kp_score, idx):
        """根据idx取关键点的xy和分数"""
        x, y = int(kps[idx][0]), int(kps[idx][1])
        score = float(f'{kp_score[idx][0]:.4f}')
        if score < 0.02:
            return None
        return [x, y, score]

    def vector_angle(self, v1, v2):
        """两个矢量的夹角，0~180度"""
        cos_angle = np.dot(v1, v2)/(np.linalg.norm(v1)*np.linalg.norm(v2))
        angle = np.arccos(cos_angle)
        angle_in_du = angle*180/np.pi
        return angle_in_du


class FallenDetection(object):
    """跌倒检测"""
    def __init__(self):
        self.upper_body = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 17, 18, 19]  # 14个
        self.lower_body = [11, 12, 13, 14, 15, 16, 19, 20, 21, 22, 23, 24, 25]  # 13个
        self.angle_thesh_lo_and_up = 70  # 下半身区域指向上半身区域的与x的夹角，小于70度，是摔倒

    def __call__(self, bs, bbox, tid, trace, kps, kp_score, last_rets):
        """
        进行跌倒检测
        返回值：True of False,
            meta: 元信息，如跌倒会返回likely in bed
        """

        """
        1.一帧也可以检测
        """
        is_fallen = self.upper_body_and_lower_body(kps, kp_score)
        if is_fallen:
            return True, 'might be lying'

        # 一帧检测不到，需要用多帧了，填充队列
        if tid == 0:  # 第1帧
            return False, None
        # last_rets = self.que[0]  # 这就是scan
        last_ret = last_rets[bs]  # 该batch, ndarray, [n, 13], 13: xyxy, cls, tid, trace
        if last_ret is None:
            return False, None
        last_tids = last_ret[:, 5]
        idx = np.argwhere(last_ret[:, 5] == tid).reshape(-1)  # [m, 1]
        if len(idx) == 0:  # 在上一帧没有匹配到目标
            return False, None
        assert len(idx) == 1, f'current_tid: {tid}, 在上一帧找到多个匹配的tid: {last_tids}'

        last_info = last_ret[idx, :]  # 上一帧tid相同的这个人的所有信息

        # 判断是否跌倒
        # print(f'current_tid: {tid} idx: {idx} {idx.shape}, last_tids: {last_tids}')

        # print(len(self.que))
        return False, None

    def velocity(self, trace):
        """使用速度大小和方向判断"""
        trace = np.array(trace)  # [n, 2]
        vector = trace[-1, :] - trace[-2, :]
        theta = self.vector2theta(vector)

        print(f'trace theta: {theta}')
        return False

    def upper_body_and_lower_body(self, kps, kpss, thresh=0.02):
        """根据上下半身区域比例判断是否跌倒"""
        if kps is None:
            return False

        ub_pts = [kps[ub] for ub in self.upper_body if kpss[ub][0] > thresh]
        lb_pts = [kps[lb] for lb in self.lower_body if kpss[lb][0] > thresh]
        ub_pts = np.array(ub_pts)
        lb_pts = np.array(lb_pts)
        if len(ub_pts) <= 3 or len(lb_pts) <= 3:  # 上半身或下半身不全，当然无法判断是否是跌倒
            return False

        ub_center = np.mean(ub_pts, axis=0)
        lb_center = np.mean(lb_pts, axis=0)
        vector = lb_center - ub_center  # 上半身指向下半身

        # print(f'ubs: {ub_pts.shape} lbs: {lb_pts.shape}')
        # print(f'ubc: {ub_center} lbc: {lb_center} vector:  {vector}')
        theta = self.vector2theta(vector)
        # print(f'angle: {theta}')
        if np.abs(theta) < self.angle_thesh_lo_and_up:
            return True
        else:
            return False

    def vector2theta(self, vector):
        """二元素的vector计算角度"""
        assert len(vector) == 2
        theta = np.arctan2(vector[1], vector[0])  # y/x
        theta = int(theta * 180 / np.pi)
        return np.abs(theta)


class LyingDetection(BaseClass):
    def __init__(self, bed_area, lying_iou_thresh):
        super(LyingDetection, self).__init__()
        self.bed_area = self.init_bed_area(bed_area)  # None or dict
        self.lying_iou_threash = lying_iou_thresh  # 人和床的iou阈值

    def init_bed_area(self, bed_area):
        """bed area需要处理满足两种方式的输入"""
        if isinstance(bed_area, str):
            if bed_area == 'None':
                return None
            else:
                raise NameError(f'config file error, bed area must be None or dict. {bed_area} {type(bed_area)}')
        return bed_area

    def __call__(self, target_info, is_fallen):
        """target_info: 该目标的信息，13个值"""
        is_lying = False
        if self.a_bed_under_person(target_info, is_fallen):
            is_lying = True
        return is_lying

    def a_bed_under_person(self, target_info, is_fallen):
        """根据身下有床判断lying:
        是Fallen状态
        """
        bed_area = self.bed_area
        if is_fallen:
            if bed_area is None:
                return False, None
            bed_names = list(bed_area.keys())
            bbox_xyxy = np.array(target_info[:4], dtype=np.int32)
            tid = target_info[5]
            # last_target_info = self.read_target_info(last_ret, bs, tid)
            for bed_name in bed_names:
                bed = bed_area[bed_name]
                bed = np.array(bed)
                assert bed.ndim == 2  # [n, 2]  n个点，2列代表x和y坐标
                bed_bbox = dm.general.pts2bbox(bed)
                # print(bbox_xyxy, bed_bbox, bbox_xyxy.dtype, bed_bbox.dtype)
                iou = dm.general.bbox_iou(bbox_xyxy, bed_bbox)
                dis = self.bbox_distance(bbox_xyxy, bed_bbox)  # 像素值没用
                b1_on_b2 = self.bbox1_on_bbox2(bbox_xyxy, bed_bbox)
                # print(f'人与床{bed_name}的iou: {iou:.4f} b2onb1: {b1_on_b2}')
                if iou > self.lying_iou_threash and b1_on_b2:
                    return True, (iou, dis, b1_on_b2, bed_name, bed_bbox, self.ntp_time())
            return False, None

        else:
            raise NotADirectoryError(f'不知道是不是已经跌倒，需要判断跌倒，未实现')


class GetUpDetection(BaseClass):
    def __init__(self, getup_iou_ratio=-5.0):
        super(GetUpDetection, self).__init__()
        self.getup_iou_ratio = getup_iou_ratio  # 起床的iou变化率，-5.0%
        pass

    def iou_reduced(self, bs, target_info, is_lying, lying_meta, last_rets):
        iou, dis, person_on_bed, bed_name, bed_bbox, last_time = lying_meta
        # bbox_xyxy = np.array(target_info[:4], dtype=np.int32)
        tid = target_info[5]
        lats_target_info = self.read_target_info(last_rets, bs, tid)
        last_bbox = np.array(lats_target_info[:4], dtype=np.int32)

        last_iou = dm.general.bbox_iou(last_bbox, bed_bbox)
        # current_time = self.ntp_time()
        # assert current_time > last_time
        # diff_time = current_time-last_time
        iou_grad = 100*(iou-last_iou)/iou  # iou变化率
        is_getup = True if iou_grad < self.getup_iou_ratio else False
        if self.print_info:
            print(f'iou: {iou:.2f} last_iou: {last_iou:.5f} iou_grad: {iou_grad:.2f}% is_getup: {is_getup}')
        return is_getup, (iou_grad)


class SittingDetection(BaseClass):
    def __init__(self):
        super(SittingDetection, self).__init__()
        self.angle_thresh_of_mid2anck_and_mid2neck = 165  # 夹角阈值，臀部到脚踝和臀部到颈部的矢量夹角

    def jumping2sitting(self, bs, target_info):
        """如果状态是jumping，二次检测坐着
        依据：臀部到颈部和臀部到膝盖夹角 70~110度 且 膝盖到臀部和膝盖到脚踝夹角70~120度
        """
        tid = target_info[5]
        bbox = np.array(target_info[:4], dtype=np.int32)
        kps = target_info[7]
        kp_score = target_info[8]
        if kps is None:
            return None, None
        assert len(kps) == 136
        rret = self.get_angles_of_mid_neck_knee_anckle(kps, kp_score)
        if rret is None:
            return None, None
        angle1, angle2 = rret

        if (70<angle1<130) and (70<angle2<120):
            is_sitting = True
        else:
            is_sitting = False
        if self.print_info:
            print(f'触发jumping2sitting判断：is sitting: {is_sitting} angle1: {angle1} angle2: {angle2}')
        return is_sitting, (angle1, angle2)

    def get_angles_of_mid_neck_knee_anckle(self, kps, kp_score):
        mid2neck = self.get_vector(kps, kp_score, 19, 18)
        mid2knee = self.get_vector(kps, kp_score, 19, [13, 14])
        knee2mid = self.get_vector(kps, kp_score, [13, 14], 19)
        knee2anck = self.get_vector(kps, kp_score, [13, 14], [15, 16])
        if mid2knee is None or mid2neck is None or knee2anck is None or knee2mid is None:
            return None
        angle1 = self.vector_angle(v1=mid2neck, v2=mid2knee)
        angle2 = self.vector_angle(v1=knee2mid, v2=knee2anck)
        return angle1, angle2

    def second_judge_sitting(self, bs, target_info):
        """
        Sitting，如果骨盆关键点到脚踝的y坐标与骨盆到颈椎的y坐标相差不大，则不是sitting
        相差不大是指m2a在0.7~1.3倍
        """
        tid = target_info[5]
        bbox = np.array(target_info[:4], dtype=np.int32)
        kps = target_info[7]
        kp_score = target_info[8]
        # bbox, kps, kp_score = 0, 0, 0
        if kps is None:
            return None, None
        assert len(kps) == 136, f'二次判断坐着：keypoints数目不是136，索引会错误'

        bw, bh = bbox[2] - bbox[0], bbox[3] - bbox[1]

        # middle = self.get_kp_xy_score(kps, kp_score, 19)
        rret = self.get_ratio_and_angle_of_mid2anckle_and_mid2neck(kps, kp_score)
        if rret is None:
            return None, None
        ratio, angle = rret
        if 0.8 < ratio < 1.2 and angle > self.angle_thresh_of_mid2anck_and_mid2neck:
            is_sitting = False
        else:
            is_sitting = True
        if self.print_info:
            print(
                f'触发sitting二次检测：tid: {tid} is sitting: {is_sitting} ratio: {ratio} angle: {angle}')

        return is_sitting, ('',)

    def get_ratio_and_angle_of_mid2anckle_and_mid2neck(self, kps, kp_score):
        """臀部关键点到颈部和臀部到脚踝，两个矢量的y轴比例和夹角"""
        mid2neck = self.get_vector(kps, kp_score, 19, 18)
        mid2anck = self.get_vector(kps, kp_score, 19, end_kp_idx=[15, 16])
        if mid2neck is None or mid2anck is None:
            return None
        ydiff_mid2neck = mid2neck[1]
        ydiff_mid2anck = mid2anck[1]
        ratio = np.abs(ydiff_mid2anck) / np.abs(ydiff_mid2neck)
        angle = self.vector_angle(v1=mid2anck, v2=mid2neck)
        return ratio, angle

    def get_vector(self, kps, kp_score, start_kp_idx, end_kp_idx):
        """获取矢量
        索引：19：臀部 10：颈部，15左脚踝 16：右脚踝
        """
        if isinstance(start_kp_idx, int):
            start_kp_idx = [start_kp_idx]
        if isinstance(end_kp_idx, int):
            end_kp_idx = [end_kp_idx]

        start_pts_scores = [self.get_kp_xy_scores(kps, kp_score, x) for x in start_kp_idx]  # 多个点，[n, 3]
        start_pts_scores = np.array([x for x in start_pts_scores if x is not None])
        end_pts_scores = [self.get_kp_xy_scores(kps, kp_score, x) for x in end_kp_idx]
        end_pts_scores = np.array([x for x in end_pts_scores if x is not None])
        if len(start_pts_scores) == 0 or len(end_pts_scores) == 0:
            return
        # print(f'statr: {start_pts_scores} end: {end_pts_scores}')
        start_pt_score = np.mean(start_pts_scores, axis=0)[:2]  # 分数就不要了
        end_pt_score = np.mean(end_pts_scores, axis=0)[:2]
        vector = end_pt_score - start_pt_score
        return vector







