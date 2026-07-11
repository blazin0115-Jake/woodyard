"""COO 总成本报告 - 基于总开销Sheet"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

print('=' * 65)
print('  /COO 总成本报告')
print('=' * 65)

# 原料价格（防染片单独标出）
raw = {
    '香精 1kg': 213.58,
    '母料 26kg': 383.82,
    '1250ml瓶 100个': 535.84,
    'R.O水 76kg': 52.00,
    'Frag Booster 200g': 24.43,
    'Frag Fixative 500g': 53.53,
    'PG 100g': 14.43,
    'DPG 500g': 23.53,
    'PDV Salt 1.5kg': 9.43,
    'EDTA 200g': 8.43,
}
anti_stain = 151.52  # 非本配方
raw_total = sum(raw.values())

print()
print('--- 原料采购 (本配方相关) ---')
for name, cost in raw.items():
    print(f'  {name:<25} RM {cost:>7.2f}')
print(f'  {"":25} {"───────":>10}')
print(f'  本配方原料合计: RM {raw_total:>7.2f}')
print(f'  (防染片RM {anti_stain:.2f}为附属品,未计入)')
print()

# 设备
eq = {
    '电子秤(10kg+0.01g)': 49.99,
    '电子秤(30kg)': 198.00,
    'Silicon Spatula': 7.00,
    'Electric Drill GSB600 Pro': 170.00,
    'Paint mixer 2pcs': 5.24,
    'PH Test Paper': 0.87,
    'Glass container 30L': 17.50,
    'Glass Beaker 500ml x2': 20.33,
}
eq_total = sum(eq.values())

print('--- 设备/工具 ---')
for name, cost in eq.items():
    print(f'  {name:<30} RM {cost:>7.2f}')
print(f'  {"":30} {"───────":>10}')
print(f'  设备合计: RM {eq_total:>7.2f}')
print()

# 总投入(不含包装)
grand = raw_total + eq_total
print('=' * 65)
print(f'  生产相关已确认总投入: RM {grand:.2f}')
print(f'  (不含防染片、不含包装、不含运费)')
print('=' * 65)
print()

# 66瓶原料消耗（精确按比例）
# 每批(6桶=87.45kg)约产60瓶
# 66瓶 = 1.1批
bottles = 66

# 母料: 12kg/批 x 1.1 = 13.2kg, 总26kg, 占50.77%
# 香精: 90g/桶 x 6桶=540g/批 x 1.1=594g... 不对
# 重新算: 单桶150g, 6桶/批=900g, 1.1批=990g, 总1000g
# PG: 单桶30g, 6桶=180g, 1.1批=198g, 总100g -> 需追加

print('--- 66瓶原料消耗成本 ---')
items = [
    ('母料(13.2kg)', 383.82 * 13.2/26),
    ('香精(990g)', 213.58 * 990/1000),
    ('1250ml瓶(66个)', 535.84 * 66/100),
    ('R.O水(79.2kg)', 54.00),      # 76kg=RM52, 缺3.2kg~RM2
    ('Frag Booster(198g)', 24.43 * 198/200),
    ('Frag Fixative(330g)', 53.53 * 330/500),
    ('PG(198g,追加1瓶)', 14.43 + 14.43),  # 100g不够, 再买1瓶
    ('DPG(462g)', 23.53 * 462/500),
    ('PDV Salt(1.32kg)', 9.43 * 1.32/1.5),
    ('EDTA(99g)', 8.43 * 99/200),
]

mat_cost = 0
for name, cost in items:
    print(f'  {name:<28} RM {cost:>7.2f}')
    mat_cost += cost

print(f'  {"":28} {"───────":>10}')
print(f'  66瓶原料消耗: RM {mat_cost:>7.2f}')
print(f'  设备摊分(66瓶): RM {eq_total:>7.2f}')
print(f'  {"":28} {"───────":>10}')
total_66 = mat_cost + eq_total
per_bottle = total_66 / bottles
print(f'  66瓶总成本: RM {total_66:>7.2f}')
print(f'  单瓶成本: RM {per_bottle:.2f}')
print()

# 利润模拟
print('--- 利润模拟 ---')
for price in [25, 30]:
    rev = bottles * price
    profit = rev - total_66
    margin = profit / rev * 100
    print(f'  定价 RM{price}/瓶:')
    print(f'    营收: RM {rev:.2f}')
    print(f'    成本: RM {total_66:.2f}')
    print(f'    毛利: RM {profit:.2f}')
    print(f'    毛利率: {margin:.1f}%')
    # 回本
    if profit > 0:
        batches_to_breakeven = grand / profit
        print(f'    回本需: {batches_to_breakeven:.1f}批 ({batches_to_breakeven*bottles:.0f}瓶)')
    print()

print('--- /COO 判断 ---')
print(' 1. 总投入: RM {:.2f}'.format(grand))
print(' 2. 原料库存: 够做~130瓶, 母料够')
print(' 3. PG: 现有100g不够198g, 需追加1瓶(RM14.43)')
print(' 4. 单瓶成本: RM {:.2f}(不含包装)'.format(per_bottle))
print(' 5. RM25毛利率仅{:.1f}%, 偏低'.format((1650-total_66)/1650*100))
print(' 6. 包装成本仍空白, 急需你填')
print()
print(' 建议: RM25只赚零头, 建议考虑RM30')
