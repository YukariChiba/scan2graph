import random

DATA_DIR = 'data/'

HONEYPOT_HOSTS_CNT = 4

DAYS = [
    "2022.09.28",
    "2022.10.08",
    "2022.10.09",
    "2022.10.10",
    "2022.10.11",
    "2022.10.12",
    "2022.10.13",
    "2022.10.14",
    "2022.10.15",
    "2022.10.16",
]


def generate_hosts():
    with open(f'{DATA_DIR}/dict/dict.txt', 'r') as f:
        last_line = f.readlines()[-1]
    max_cnt = int(last_line.strip().split(" ")[1]) + 1
    with open(f'{DATA_DIR}/dict/dict.txt', 'a') as f:
        f.writelines(
            [
                f"honeypot{i} {max_cnt+i}\n" for i in range(HONEYPOT_HOSTS_CNT)
            ]
        )
    return max_cnt

# def generate_routes():


def extract_max_attr():
    node_map = {}
    for day in DAYS:
        with open(f'{DATA_DIR}/port/port_onehot/{day}_onehot_data.csv', 'r') as f:
            lines = f.readlines()
            for line in lines[1:]:
                items = line.strip().split(",")
                ip_id = items[1]
                ip_attr = list(map(int, items[2:]))
                if ip_id in node_map.keys():
                    node_map[ip_id] = [sum(x)
                                       for x in zip(node_map[ip_id], ip_attr)]
                else:
                    node_map[ip_id] = ip_attr
    node_map_agg = []
    for node in node_map.keys():
        node_map_agg.append({
            "node": node,
            "attrs": node_map[node]
        })
    node_map_agg = sorted(
        node_map_agg, key=lambda x: max(x['attrs']), reverse=True)
    return node_map_agg[:HONEYPOT_HOSTS_CNT]


def copy_attr(nodes, cnt):
    node_days = []
    for i in range(HONEYPOT_HOSTS_CNT):
        node_days.append([])
        for copy_day in range(random.randint(len(DAYS)//3, len(DAYS)), len(DAYS)):
            node_days[i].append(copy_day)
            with open(f'{DATA_DIR}/port/port_onehot/{DAYS[copy_day]}_onehot_data.csv', 'a') as f:
                max_val = max(nodes[i]['attrs'])
                max_pos = nodes[i]['attrs'].index(max_val)
                attr = [
                    1 if j == max_pos else 0 for j in range(0, len(nodes[i]['attrs']))
                ]
                f.write(
                    f"honeypot{str(i)},{str(cnt+i)},{','.join(map(str, attr))}\n"
                )
    return node_days


def generate_routes(node_days, cnt):
    with open(f'{DATA_DIR}/route/path_data.csv', 'r') as f:
        lines = f.readlines()
    lines = [a for a in lines if (not a.strip().split(",")[0].startswith(
        "172.20.168")) or (not a.strip().split(",")[0].startswith("192.168.1"))]
    with open(f'{DATA_DIR}/route/path_data.csv', 'a') as rf:
        for i in range(HONEYPOT_HOSTS_CNT):
            nh = random.choice(lines)
            for j in node_days[i]:
                if random.random() > 0.8:
                    nh = random.choice(lines)
                nh_id = nh.strip().split(",")[1]
                nh_ip = nh.strip().split(",")[0]
                rf.write(
                    f"{nh_ip},{nh_id},honeypot{str(i)},{str(cnt+i)}\n"
                )


def main():
    #cnt = generate_hosts()
    #max_nodes = extract_max_attr()
    #node_days = copy_attr(max_nodes, cnt)
    # print(node_days)
    node_days = [[3, 4, 5, 6, 7, 8, 9], [8, 9], [7, 8, 9], [8, 9]]
    cnt = 26870
    generate_routes(node_days, cnt)


main()
