"""COO 总成本报告 - 基于实际采购数据"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

print('='*65)
print('  /COO 总成本报告')
print('='*65)
print()

# ===== 原材料采购成本 (来自总开销Sheet) =====
raw_materials = [
    ('香精 1kg', 213.58, '1瓶', 'C相预溶固香', 1000, '150g/桶, 6桶=900g/批'),
    ('母料 500g x 52包', 383.82, '26kg', 'B相去污底座', 26000, '2000g/桶, 6桶=12kg/批'),
    ('防染片 5600片', 151.52, '7包', '非本配方，附属品', 0, 'N/A'),
    ('1250ml瓶 100个', 535.84, '100个', '容器', 100, '直接使用'),
    ('R.O水 76kg', 52.00, '8瓶(9.5kg/瓶)', 'A相水基底', 76000, '12000g/桶, 6桶=72kg/批'),
    ('Fragrance Booster 200g', 24.43, '2瓶', 'C相香爆发', 200, '30g/桶, 6桶=180g/批'),
    ('Fragrance Fixative 500g', 53.53, '1瓶', 'C相锚定', 500, '50g/桶, 6桶=300g/批'),
    ('PG 100g', 14.43, '1瓶', 'C相防浑浊', 100, '30g/桶, 6桶=180g/批'),
    ('DPG 500g', 23.53, '1瓶', 'C相包裹醇化', 500, '70g/桶, 6桶=420g/批'),
    ('PDV Salt 1.5kg', 9.43, '1包', 'A相增稠', 1500, '200g/桶, 6桶=1.2kg/批'),
    ('EDTA 200g', 8.43, '2包', 'A相软化水质', 200, '15g/桶, 6桶=90g/批'),
]

raw_total = sum(r[1] for r in raw_materials)

print('--- 原料采购 ---')
print(f' {"原料":<25} {"金额(RM)":<10} {"采购量":<12}')
print('-'*50)
for name, cost, qty, _, _, _ in raw_materials:
    print(f' {name:<25} RM {cost:>6.2f}  {qty:<12}')
print(f' {"":25} {"───────":>10}')
print(f' {"":25} RM {raw_total:>7.2f}')
print()

# ===== 设备工具 =====
equipment = [
    ('电子秤 10kg/1g + 500g/0.01g', 49.99),
    ('电子秤 30kg', 198.00),
    ('Silicon Spatula', 7.00),
    ('Electric Drill GSB600 Pro', 170.00),
    ('Paint mixer 2pcs', 5.24),
    ('PH Test Paper', 0.87),
    ('Glass container 30L', 17.50),
    ('Glass Beaker 500ml x2', 20.33),
]

eq_total = sum(e[1] for e in equipment)

print('--- 设备/工具 ---')
print(f' {"项目":<35} {"金额(RM)"}')
print('-'*48)
for name, cost in equipment:
    print(f' {name:<35} RM {cost:>6.2f}')
print(f' {"":35} {"───────":>10}')
print(f' {"":35} RM {eq_total:>7.2f}')
print()

# ===== 待定包装成本 =====
print('--- 待定包装成本 (未采购) ---')
print('  Boxes')
print('  Labelling Sticker (Small)')
print('  Labelling Sticker (Big)')
print('  Caution Sticker')
print('  Self standing bag')
print('  Bubble wrap (Pouch)')
print('  Bubble wrap (Small)')
print('  Caution Tape')
print('  Thermal Printer')
print()

# ===== 总投入 =====
grand_total = raw_total + eq_total
print('='*65)
print(f' 已确认总投入: RM {grand_total:.2f}')
print('='*65)
print()

# ===== 单瓶成本拆解 (基于66瓶)=====
print('--- 单瓶成本拆解 (按66瓶) ---')
bottles = 66

# 一次生产66瓶: 约1.1批 (6桶/批 = ~60-66瓶)
# 1批(6桶)用12kg母料+72kg水, 实得约60瓶
# 66瓶需约1.1批
batches_needed = 66 / 60  # ~1.1

# 原料: 所有原料采购总量可覆盖多批, 但按消耗比例算66瓶
# 母料: 12kg/批 x 1.1批 = 13.2kg, 总26kg, 够
# 香精: 900g/批 x 1.1批 = 990g, 总1000g, 刚好够
# DPG: 420g/批 x 1.1批 = 462g, 总500g, 刚好够
# PG: 180g/批 x 1.1批 = 198g, 总100g, 不够
# Fixative: 300g/批 x 1.1批 = 330g, 总500g, 够
# Booster: 180g/批 x 1.1批 = 198g, 总200g, 刚好够
# EDTA: 90g/批 x 1.1批 = 99g, 总200g, 够
# Salt: 1.2kg/批 x 1.1批 = 1.32kg, 总1.5kg, 刚好够
# 瓶子: 66个, 总100个, 够

# 按比例消耗的原料成本
consumed = {
    '香精': 213.58 * (990/1000),
    '母料': 383.82 * (13.2/26),
    '1250ml瓶': 535.84 * (66/100),
    'R.O水': 52.00 * (79.2/76) if False else 52.00,  # R.O水够用
    'Fragrance Booster': 24.43 * (198/200),
    'Fragrance Fixative': 53.53 * (330/500),
    'PG': 14.43 * (198/100),  # 不够, 需另购
    'DPG': 23.53 * (462/500),
    'PDV Salt': 9.43 * (1.32/1.5),
    'EDTA': 8.43 * (99/200),
}

# R.O水: 66瓶约需 79.2kg, 但已有76kg, 差3.2kg (~RM2)
water_cost = 52.00 + 2.00  # 追加一点

consumed['R.O水'] = water_cost
# PG不够, 需追加约98g, 约RM14.43再买一瓶
consumed['PG追加'] = 14.43

raw_consumed = sum(consumed.values())
eq_per_bottle = eq_total / bottles  # 设备摊分

print(f' 原料消耗(66瓶): RM {raw_consumed:.2f}')
print(f' 设备摊分: RM {eq_per_bottle:.2f}')
print(f' 未含包装: 待定')
print(f' ──────────────────────')
print(f' 66瓶总成本(不含包装): RM {raw_consumed + eq_per_bottle*bottles:.2f}')
print(f' 单瓶成本(不含包装): RM {(raw_consumed + eq_per_bottle*bottles)/bottles:.2f}')
print()

# 利润模拟
print('--- 利润模拟 (单瓶 RM25) ---')
revenue = 66 * 25
profit = revenue - raw_consumed - (eq_per_bottle * bottles)
print(f' 营收: 66 x RM25 = RM {revenue:.2f}')
print(f' 原料+设备: RM {raw_consumed + eq_per_bottle*bottles:.2f}')
print(f' 毛利: RM {profit:.2f}')
print(f' 毛利率: {profit/revenue*100:.1f}%')
print(f' 回本所需: RM {grand_total:.2f} ÷ RM {profit:.2f}/批 = {grand_total/profit:.1f} 批')
print()

# 注意事项
print('--- /COO 判断 ---')
print(' 1. 已确认投入 RM {:.2f}'.format(grand_total))
print(' 2. 原料: 母料够 ✅  但PG ⚠️ 只够约一半(100g, 需198g)')
print(' 3. 包装成本: 仍空白, 须你填价')
print(' 4. 建议: 先产1批(~60瓶)试跑, 确认市场反应后再扩产')
