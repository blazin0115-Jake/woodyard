"""扫描总开销Sheet - A至E列"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

# 原材料 A-E列 (Row 1-12)
print('=== 原材料 (A列至E列) ===')
print()
print(' A列(原材料)     B(重量/容量)   C(数量)    D(总重量)   E(总价值)')
print('-'*65)
raw = [
    ('香精',       '1kg',    '1瓶',   '1kg',       'RM 213.58'),
    ('母料',       '500g',   '52包',  '26kg',      'RM 383.82'),
    ('防染片',     '800片',  '7包',   '5600片',    'RM 151.52'),  # 非本配方
    ('1250ml瓶',   '1250ml', '100个', '100个',     'RM 535.84'),
    ('R.O水',      '9.5kg',  '8瓶',   '76kg',      'RM 52.00'),
    ('Frag Booster', '100g','2瓶',   '200g',      'RM 24.43'),
    ('Frag Fixative', '500g','1瓶',  '500g',      'RM 53.53'),
    ('PG',         '100g',   '1瓶',   '100g',      'RM 14.43'),
    ('DPG',        '500g',   '1瓶',   '500g',      'RM 23.53'),
    ('PDV Salt',   '1.5kg',  '1包',   '1.5kg',     'RM 9.43'),
    ('EDTA',       '100g',   '2包',   '200g',      'RM 8.43'),
]
for r in raw:
    # 过滤运费voucher列
    print(f' {r[0]:<15} {r[1]:<10} {r[2]:<8} {r[3]:<10} {r[4]}')

# 价格提取（剔除防染片）
raw_prices = {
    '香精': 213.58,
    '母料': 383.82,
    '瓶子': 535.84,
    'R.O水': 52.00,
    'Booster': 24.43,
    'Fixative': 53.53,
    'PG': 14.43,
    'DPG': 23.53,
    'Salt': 9.43,
    'EDTA': 8.43,
}
raw_total = sum(raw_prices.values())
anti_stain = 151.52

print()
print(f' 本配方相关原料合计: RM {raw_total:.2f}')
print(f'   (其中防染片RM 151.52用于附属品, 非本配方)')
print()

# 设备/工具/包装 A列-E列 (Row 16开始)
print('=== 设备/工具/包装 (A列至E列) ===')
print()
print(' A列              B              C       D           E(总价值)')
print('-'*55)
equip = [
    ('电子秤(10kg+500g)', '10kg+0.01g', '1pc', '', 'RM 49.99'),
    ('电子秤(30kg)',      '30kg',       '1pc', '', 'RM 198.00'),
    ('Silicon Spatula',   'Food Grade', '1pc', '', 'RM 7.00'),
    ('Electric Drill',    'GSB600 Pro', '1pc', '', 'RM 170.00'),
    ('Paint mixer',       '2pcs',       '2pcs','', 'RM 5.24'),
    ('PH Test Paper',     '80strips',   '1个',  '', 'RM 0.87'),
    ('Glass container',   '30L',        '1个',  '', 'RM 17.50'),
    ('Glass Beaker',      '500ml',      '2个',  '', 'RM 20.33'),
]
for e in equip:
    print(f' {e[0]:<20} {e[1]:<15} {e[2]:<6} {e[3]:<6} {e[4]}')

eq_prices = [49.99, 198.00, 7.00, 170.00, 5.24, 0.87, 17.50, 20.33]
eq_total = sum(eq_prices)

print()
print(f' 设备/工具合计: RM {eq_total:.2f}')
print()
print('--- 包装类(待定) ---')
print(' Boxes - 暂未定')
print(' Labelling Sticker - 暂未定')
print(' Caution Sticker - 暂未定')
print(' Self standing bag - 暂未定')
print(' Bubble wrap - 暂未定')
print(' Caution Tape - 暂未定')
print(' Thermal Printer - 暂未定')
print()

grand = raw_total + eq_total
print('='*45)
print(f' 生产相关总投入: RM {grand:.2f}')
print(f'   (不含防染片 RM {anti_stain:.2f})')
print(f'   (不含包装)')
print('='*45)
print()

# 66瓶成本
print('--- 66瓶成本拆解 ---')
bottles = 66
# 母料: 66瓶需约13.2kg, 总26kg, 使用率50.8%
mother_cost = 383.82 * (13.2/26)  # ~RM 194.94
# 香精: 66瓶需990g, 总1000g, 使用率99%
frag_cost = 213.58 * 0.99
# 瓶子: 66个, 总100个, 使用率66%
bottle_cost = 535.84 * 0.66
# R.O水: 66瓶需79.2kg, 总76kg, 差3.2kg ~额外RM2
water_cost = 52.00 + 2.00
# 其他按消耗比例
booster_cost = 24.43 * (198/200)
fixative_cost = 53.53 * (330/500)
pg_cost = 14.43 * (198/100)  # 不够, 需再买一瓶PG
dpg_cost = 23.53 * (462/500)
salt_cost = 9.43 * (1.32/1.5)
edta_cost = 8.43 * (99/200)
pg_add = 14.43  # 追加一瓶PG

materials_66 = [
    ('母料(13.2kg)', mother_cost),
    ('香精(990g)', frag_cost),
    ('瓶子(66个)', bottle_cost),
    ('R.O水(79.2kg)', water_cost),
    ('Booster(198g)', booster_cost),
    ('Fixative(330g)', fixative_cost),
    ('PG(198g,需追加)', pg_cost + pg_add),
    ('DPG(462g)', dpg_cost),
    ('PDV Salt(1.32kg)', salt_cost),
    ('EDTA(99g)', edta_cost),
]

mat_total = sum(m[1] for m in materials_66)
eq_amort = eq_total / bottles

print(f' {\"项目\":<22} {\"金额\"}')
print('-'*35)
for name, cost in materials_66:
    print(f' {name:<22} RM {cost:>6.2f}')
print(f' {"":22} {"───────"}')
print(f' 原料合计: RM {mat_total:<7.2f}')
print(f' 设备摊分: RM {eq_amort*66:<7.2f}')
print(f' {"───────"}')
print(f' 总成本: RM {mat_total + eq_total:<7.2f}')
print(f' 单瓶成本: RM {(mat_total + eq_total)/66:<7.2f}')
print()

# 利润
print('--- 利润模拟 ---')
print(f' 方案A: RM25/瓶')
rev_a = 66 * 25
print(f'  营收: RM {rev_a:.2f}')
print(f'  成本: RM {mat_total + eq_total:.2f}')
print(f'  毛利: RM {rev_a - (mat_total + eq_total):.2f}')
print(f'  毛利率: {(rev_a - (mat_total + eq_total))/rev_a*100:.1f}%')
print()
print(f' 方案B: RM30/瓶')
rev_b = 66 * 30
print(f'  营收: RM {rev_b:.2f}')
print(f'  成本: RM {mat_total + eq_total:.2f}')
print(f'  毛利: RM {rev_b - (mat_total + eq_total):.2f}')
print(f'  毛利率: {(rev_b - (mat_total + eq_total))/rev_b*100:.1f}%')
print()

# /COO判断
print('--- /COO 判断 ---')
print(f' 生产相关总投入: RM {grand:.2f}')
print(f' 物料库存: 足够产~130瓶 ✅')
print(f' PG要追: 现有100g, 需198g ⚠️')
print(f' 包装成本: 仍待定')
print(f' RM25毛利率偏低, 建议考虑RM30')
